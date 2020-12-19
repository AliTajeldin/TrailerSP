from solid import *
from solid.utils import *  # Not required, but the utils module is useful
from lib.item import Item
from lib.rail8020 import Rail1515

BED_TOP_HEIGHT = 7 # 1 inch ply + 6" mattress

class BedTop(Item):
  def __init__(self, w, l):
    super().__init__([w,l,BED_TOP_HEIGHT])
    self.color = (67, 170, 139)
  
  def render(s):
    # TODO: build this from cushion + plywood componenets
    (w,l,h) = s.dim
    b = union()(
      cube([w,l,1]),
      translate([1,1,1])(cube([w-2,l-2,h-1]))
    )
    return s.c(s.color, b)

class Bed8020(Item):
  def __init__(self, dim, mid_offset='M'):
    super().__init__(dim)
    self.color = (67, 170, 139)
    self.mid_offset = dim[0]/2 if mid_offset=='M' else mid_offset

  def render(s):
    (w,l,h) = s.dim
    fh = h - BED_TOP_HEIGHT # frame height

    # bed top
    bt = BedTop(w,l)
    s.place(bt, rel_to='TBL')

    # horizontal rails along width
    rw = Rail1515(w)
    s.place(rw, rel_to='TFL', offset=[0,0,-BED_TOP_HEIGHT])
    s.place(rw, rel_to='TBL', offset=[0,0,-BED_TOP_HEIGHT])

    # leg rails
    legl = fh-1.5
    rleg = Rail1515(legl)
    s.place(rleg, rel_to='FL', rotation='YL')
    s.place(rleg, rel_to='BL', rotation='YL')
    s.place(rleg, rel_to='FR', rotation='YL')
    s.place(rleg, rel_to='BR', rotation='YL')

    # depth support pieces
    dleg = Rail1515(l - 2*1.5)
    s.place(dleg, rel_to='BL', rotation='L', offset=[0,1.5,0])
    s.place(dleg, rel_to='BL', rotation='L', offset=[0,1.5,legl])
    s.place(dleg, rel_to='BR', rotation='L', offset=[0,1.5,0])
    s.place(dleg, rel_to='BR', rotation='L', offset=[0,1.5,legl])

    return None
