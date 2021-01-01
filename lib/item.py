from abc import ABC, abstractmethod
from solid import *
from solid.utils import *  # Not required, but the utils module is useful

class BillOfMaterial(object):
  def __init__(self, item):
    self.item = item
    self.c_items = []

  def add_child(s, child):
    s.c_items.append(child)

  def _group_children(s):
    """group similar children and maintain count to avoid repeated bom output"""
    gc = {}
    for c in s.c_items:
      cd = c.desc()
      if cd in gc:
        gc[cd][0] += 1
      else:
        gc[cd] = [1,c]
    return gc

  def print(s, indent='', count=1):
    print("{0}{1} X {2}".format(indent, count, s.item.desc()))
    for [count, c] in s._group_children().values():
      c.bom.print(indent + '  ', count)


class Item(ABC):
  """base class of all items that need to be placed in the trailer"""
  def __init__(self, dim):
    self.dim = [int(d) if int(d)==float(d) else d for d in dim]
    self.r_children = [] # rendered children
    self._render_cache = 'not-rendered' # can't use None as marker as it is a valid render result
    self.bom = BillOfMaterial(self)

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

  def dimStr3D(s):
    (w,l,h) = s.getDim()
    return "{0}x{1}x{2}".format(w,l,h)

  def dimStr2D(s):
    (w,l,h) = s.getDim()
    return "{0}x{1}".format(w,l)

  def desc(s):
    """one line description of what this item is"""
    return type(s).__name__ + ': ' + s.dimStr3D()

  @abstractmethod
  def render(s):
    pass

  def _render(s):
    """use cached render to avoid calling `render` twice when same item
       is placed twice inside parent"""
    if s._render_cache == 'not-rendered':
      s._render_cache = s.render()
    return s._render_cache

  def render_all(s):
    """render this item plus render_all of it's children"""
    me_and_children = [s._render()] + s.r_children
    return union()([x for x in me_and_children if x])

  def print_bom(s):
    s.render_all()
    s.bom.print()

  def place(s, item, rel_to='BL', rotation='', offset=None):
    """places a child item inside this item.
       rel_to: BL, FL, BR, FR corresponding to BAck/Front Left/Right
               TBL, TFL, TBR, TFR same as above but relative to top of parent item
       rotation: L,R,180 to rotate item 90,-90,180 before placing (rot around Z-Axis)
                V to rotate item 90 along y-axis to vertical
                VR in addition to vertical as above, add a normal right rotation on z-axis (bottom of object is now facing us).
                F,B to rotate front/back on the X-Axis
                FL in addtion to F rotation above, rotate to left (z-axis)
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
      (w,l) = (l,w)
    if rotation == 'R':
      out = translate([0,w,0])(rotate(-90)(out))
      (w,l) = (l,w)
    if rotation == 180:
      out = translate([w,l,0])(rotate(180)(out))
    if rotation == 'V':
      out = translate([h,0,0])(rotate([0,-90,0])(out))
      (w,h) = (h,w)
    if rotation == 'VR':
      out = rotate(-90)(rotate([0,-90,0])(out))
      (w,l,h) = (l,h,w)
    if rotation == 'F':
      out = up(l)(rotate([-90,0,0])(out))
      (l,h) = (h,l)
    if rotation == 'B':
      out = forward(h)(rotate([90,0,0])(out))
      (l,h) = (h,l)
    if rotation == 'BL':
      out = rotate(90)(rotate([90,0,0])(out))
      (w,l,h) = (h,w,l)

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

    s.r_children.append(out)
    s.bom.add_child(item)

    return out
