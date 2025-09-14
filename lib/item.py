from abc import ABC, abstractmethod
from solid import *
from solid.utils import *  # Not required, but the utils module is useful

def addOffsets(o1, o2):
  return (o1[0]+o2[0], o1[1]+o2[1], o1[2]+o2[2])


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
    self.rpos = (0,0,0) # last rendered position of this item relative to parent.
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

  def getRPos(s):
    return s.rpos

  def c(s, cv, item):
    """apply color vector to given item and return the colored item"""
    return color([c/255.0 for c in cv])(item)

  # TODO: remove next two funcs t,r
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

  def place(s, item, rel_to='BL', rel_to_item=[], rotation='', offset=[0,0,0]):
    """places a child item inside this item.
       rel_to: BL, FL, BR, FR corresponding to Back/Front Left/Right
               TBL, TFL, TBR, TFR same as above but relative to top of parent item
               CX, CY, CZ center relative to x,y,z axis
       rel_to_item: (ritem, rel_pos) or [(ritem, rel_pos), ...] for multiple placements.
                ritem is the item we want to position next to.
                rel_pos is one of "LRFBTU" for left, right, front, back, top, under
                if "A" as in "AL" or "AT" then align position to left, top, etc.
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

    (dx,dy,dz) = (0,0,0)

    if rel_to in ('FL', 'TFL'):
      dy = pl-l
    if rel_to in ('FR', 'TFR'):
      (dx,dy) = (pw-w,pl-l)
    if rel_to in ('BR', 'TBR'):
      dx = pw-w
    if rel_to[0] == 'T':
      dz = ph-h

    if rel_to == 'CX':
      dx = (pw-w)/2.0
    if rel_to == 'CY':
      dy = (pl-l)/2.0
    if rel_to == 'CZ':
      dz = (ph-h)/2.0

    if type(rel_to_item) == type(()):
      rel_to_item = [rel_to_item]

    for rti in rel_to_item:
      (i, r) = rti
      irp = i.getRPos()
      if "L" == r:
        dx = irp[0] - w
      if "AL" == r:
        dx = irp[0]
      if "R" == r:
        dx = irp[0] + i.getW()
      if "AR" == r:
        dx = irp[0] + i.getW() - w
      if "F" == r:
        dy = irp[1] + i.getL()
      if "AF" == r:
        dy = irp[1] + i.getL() - l
      if "B" == r:
        dy = irp[1] - l
      if "AB" == r:
        dy = irp[1]
      if "T" == r:
        dz = irp[2] + i.getH()
      if "AT" == r:
        dz = irp[2] + i.getH() - h
      if "U" == r:
        dz = irp[2] - h
      if "AU" == r:
        dz = irp[2]
   
    item.rpos = addOffsets((dx,dy,dz), offset)
    out = translate(item.rpos)(out)

    s.r_children.append(out)
    s.bom.add_child(item)

    return out
