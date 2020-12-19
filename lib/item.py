from abc import ABC, abstractmethod
from solid import *
from solid.utils import *  # Not required, but the utils module is useful

class Item(ABC):
  """base class of all items that need to be placed in the trailer"""
  def __init__(self, dim):
    self.dim = dim
    self.children = []

  def getDim(s):
    return s.dim

  def getW(s):
    return s.getDim()[0]

  def getL(s):
    return s.getDim()[1]

  def getH(s):
    return s.getDim()[2]

  def c(s, cv, item):
    """apply color vector to given item and return the colored item"""
    return color([c/255.0 for c in cv])(item)

  def t(s, tv, item):
    """apply translation vector to given item"""
    return translate(tv)(item)

  def r(s, a, item):
    """apply rotation to given item"""
    return rotate(a)(item)

  @abstractmethod
  def render(s):
    pass

  def render_all(s):
    """render this item plus render_all of it's children"""
    me_and_children = [s.render()] + s.children
    return union()([x for x in me_and_children if x])

  @staticmethod
  def swap(a,b):
    return (b,a)

  def place(s, item, rel_to='BL', rotation='', offset=None):
    """places a child item inside this item.
       rel_to: BL, FL, BR, FR corresponding to BAck/Front Left/Right
               TBL, TFL, TBR, TFR same as above but relative to top of parent item
       rotation: L,R,180 to rotate item 90,-90,180 before placing (rot around Z-Axis)
                YL to rotate item 90 along y-axis to vertical
       offset: (x,y,z) offset to apply to item after rotation
       Note: the placement takes the w,l,h of child item when placing.  if child item is placed on the right side of this item,
       then the offset is from the right side of the child item.
    """
    (pw,pl,ph) = s.getDim()
    (w,l,h) = item.getDim()
    out = item.render_all()

    # print("placing", s.getDim(), item.getDim(), rel_to, rotation, offset)
    if rotation == 'L':
      out = translate([l,0,0])(rotate(90)(out))
      (w,l) = Item.swap(w,l)
    if rotation == 'R':
      out = translate([0,w,0])(rotate(-90)(out))
      (w,l) = Item.swap(w,l)
    if rotation == 180:
      out = translate([w,l,0])(rotate(180)(out))
    if rotation == 'YL':
      out = translate([h,0,0])(rotate([0,-90,0])(out))
      (w,h) = Item.swap(w,h)

    if rel_to in ('FL', 'TFL'):
      out = translate([0,pl-l,0])(out)
    if rel_to in ('FR', 'TFR'):
      out = translate([pw-w,pl-l,0])(out)
    if rel_to in ('BR', 'TBR'):
      out = translate([pw-w,0,0])(out)
    if rel_to[0] == 'T':
      out = up(ph-h)(out)

    if offset:
      out = translate(offset)(out)

    s.children.append(out)

    return out
