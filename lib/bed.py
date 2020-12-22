from solid import *
from solid.utils import *  # Not required, but the utils module is useful
from lib.item import Item
from lib.rail8020 import Rail1515
from lib.wood import Ply_1_2

BED_TOP_HEIGHT = 6.5 # 0.5 inch ply + 6" mattress

class Mattress(Item):
  def __init__(self, w, l):
    super().__init__([w,l,BED_TOP_HEIGHT-0.5])
    self.color = (67, 170, 210)

  def desc(s):
    return "Foam Mattress {0}x{1}".format(s.getW(), s.get(H))

  def render(s):
    (w,l,h) = s.getDim()
    return s.c(s.color, cube([w,l,h]))

class BedTop(Item):
  def __init__(self, w, l):
    super().__init__([w,l,BED_TOP_HEIGHT])
  
  def render(s):
    (w,l,h) = s.getDim()

    ply = Ply_1_2(w,l)
    s.place(ply)

    mattress = Mattress(w-1, l-1)
    s.place(mattress, offset=[0.5,0.5,0.5])

    return None

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
    s.place(rw, rel_to='FL')
    s.place(rw, rel_to='BL')
    s.place(rw, rel_to='FL', offset=[0,0,fh-1.5])
    s.place(rw, rel_to='BL', offset=[0,0,fh-1.5])

    # leg rails
    leg = Rail1515(fh - 2*1.5)
    s.place(leg, rel_to='FL', rotation='YL', offset=[0,0,1.5])
    s.place(leg, rel_to='BL', rotation='YL', offset=[0,0,1.5])
    s.place(leg, rel_to='FR', rotation='YL', offset=[0,0,1.5])
    s.place(leg, rel_to='BR', rotation='YL', offset=[0,0,1.5])

    # depth support pieces
    dep = Rail1515(l - 2*1.5)
    s.place(dep, rel_to='BL', rotation='L', offset=[0,1.5,0])
    s.place(dep, rel_to='BL', rotation='L', offset=[0,1.5,fh-1.5])
    s.place(dep, rel_to='BR', rotation='L', offset=[0,1.5,0])
    s.place(dep, rel_to='BR', rotation='L', offset=[0,1.5,fh-1.5])
    s.place(dep, rel_to='BL', rotation='L', offset=[0.25*w,1.5,fh-1.5])
    s.place(dep, rel_to='BL', rotation='L', offset=[0.75*w,1.5,fh-1.5])

    # add mid leg/support if specified
    if s.mid_offset:
      s.place(leg, rel_to='FL', rotation='YL', offset=[s.mid_offset,0,1.5])
      s.place(leg, rel_to='BL', rotation='YL', offset=[s.mid_offset,0,1.5])
      s.place(dep, rel_to='BL', rotation='L',  offset=[s.mid_offset,1.5,0])
      s.place(dep, rel_to='BL', rotation='L',  offset=[s.mid_offset,1.5,fh-1.5])

    return None
