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
               CX, CY, CZ center relative to x,y,z axis
       rotation: L,R,180 to rotate item 90,-90,180 before placing (rot around Z-Axis)
                YL|YR to rotate item left/right 90 degress along y-axis to vertical
                F,B to rotate front/back on the X-Axis
                DEPRECATED: VR (same as 'YL:R'), rotate to vertical and right on x-axis (bottom shown)
                DEPRECATED: V (same as 'YL')
       offset: (x,y,z) offset to apply to item after rotation
       Note: the placement takes the w,l,h of child item when placing.  if child item is placed on the right side of this item,
       then the offset is from the right side of the child item.
    """
    (pw,pl,ph) = s.getDim()
    (w,l,h) = item.getDim()
    out = item.render_all()

    # print("placing", s.getDim(), item.getDim(), rel_to, rotation, offset)
    if rotation in (180, '180'): rotation = 'L:L'
    if rotation == 'VR': rotation = 'YL:R'
    for r in rotation.split(':'):
      if r == 'L':
        out = translate([l,0,0])(rotate(90)(out))
        (w,l) = (l,w)
      if r == 'R':
        out = translate([0,w,0])(rotate(-90)(out))
        (w,l) = (l,w)
      if r in ('YL', 'V'):
        out = translate([h,0,0])(rotate([0,-90,0])(out))
        (w,h) = (h,w)
      if r == 'YR':
        out = translate([0,0,w])(rotate([0,90,0])(out))
        (w,h) = (h,w)
      if r == 'F':
        out = up(l)(rotate([-90,0,0])(out))
        (l,h) = (h,l)
      if r == 'B':
        out = forward(h)(rotate([90,0,0])(out))
        (l,h) = (h,l)

    if rel_to in ('FL', 'TFL'):
      out = translate([0,pl-l,0])(out)
    if rel_to in ('FR', 'TFR'):
      out = translate([pw-w,pl-l,0])(out)
    if rel_to in ('BR', 'TBR'):
      out = translate([pw-w,0,0])(out)
    if rel_to[0] == 'T':
      out = up(ph-h)(out)

    if rel_to == 'CX':
      out = right((pw-w)/2.0)(out)
    if rel_to == 'CY':
      out = forward((pl-l)/2.0)(out)
    if rel_to == 'CZ':
      out = up((ph-h)/2.0)(out)

    if offset:
      out = translate(offset)(out)

    s.r_children.append(out)
    s.bom.add_child(item)

    return out
