from abc import ABC, abstractmethod
from solid import *
from solid.utils import *  # Not required, but the utils module is useful

class Item(ABC):
  """base class of all items that need to be placed in the trailer"""
  def __init__(self, dim):
    self.dim = dim
    self.children = []

  def getDim(self):
    return self.dim

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
    return s.render() # TODO: add call to unionall with rendered children.

  @staticmethod
  def swap(a,b):
    return (b,a)

  def place(s, item, rel_to='BL', rotation='', offset=None):
    """places a child item inside this item.
       rel_to: BL, FL, BR, FR corresponding to Bottom/Front Left/Right
       rotation: L,R,180 to rotate item 90,-90,180 before placing (rot around Z-Axis)
       offset: (x,y,z) offset to apply to item after rotation
       Note: the placement takes the w,l,h of child item when placing.  if child item is placed on the right side of this item,
       then the offset is from the right side of the child item.
    """
    (pw,pl,ph) = s.getDim()
    (w,l,h) = item.getDim()
    out = item.render_all()

    if rotation == 'L':
      out = translate([l,0,0])(rotate(90)(out))
      (w,l) = Item.swap(w,l)
    if rotation == 'R':
      out = translate([0,w,0])(rotate(-90)(out))
      (w,l) = Item.swap(w,l)
    if rotation == 180:
      out = translate([w,l,0])(rotate(180)(out))

    if rel_to == 'FL':
      out = translate([0,pl-l,0])(out)
    if rel_to == 'FR':
      out = translate([pw-w,pl-l,0])(out)
    if rel_to == 'BR':
      out = translate([pw-w,0,0])(out)
      
    if offset:
      out = translate(offset)(out)

    self.children.append(out)

    return out
