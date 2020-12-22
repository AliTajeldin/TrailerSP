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
    return "Foam Mattress: " + s.dimStr2D()

  def render(s):
    (w,l,h) = s.getDim()
    return s.c(s.color, cube([w,l,h]))

class BedTop(Item):
  def __init__(self, w, l):
    super().__init__([w,l,BED_TOP_HEIGHT])

  def desc(s):
    return "Bed Top: " + s.dimStr2D()

  def render(s):
    (w,l,h) = s.getDim()

    ply = Ply_1_2(w,l)
    s.place(ply)

    mattress = Mattress(w-1, l-1)
    s.place(mattress, offset=[0.5,0.5,0.5])

    return None

class BedFrame8020(Item):
  def __init__(self, dim, mid_offset, railFactory):
    super().__init__(dim)
    self.railFactory = railFactory
    self.mid_offset = mid_offset

  def desc(s):
    return "Bed Frame of {0}: {1}".format(s.railFactory.__name__, s.dimStr3D())

  def render(s):
    (w,l,h) = s.getDim()
    sz = s.railFactory.SIZE

    # horizontal rails along width
    rw = s.railFactory(w)
    s.place(rw, rel_to='FL')
    s.place(rw, rel_to='BL')
    s.place(rw, rel_to='TFL')
    s.place(rw, rel_to='TBL')

    # leg rails
    leg = s.railFactory(h - 2*sz)
    s.place(leg, rel_to='FL', rotation='V', offset=[0,0,sz])
    s.place(leg, rel_to='BL', rotation='V', offset=[0,0,sz])
    s.place(leg, rel_to='FR', rotation='V', offset=[0,0,sz])
    s.place(leg, rel_to='BR', rotation='V', offset=[0,0,sz])

    # depth support pieces
    dep = s.railFactory(l - 2*sz)
    s.place(dep, rel_to='BL',  rotation='L', offset=[0,sz,0])
    s.place(dep, rel_to='TBL', rotation='L', offset=[0,sz,0])
    s.place(dep, rel_to='BR',  rotation='L', offset=[0,sz,0])
    s.place(dep, rel_to='TBR', rotation='L', offset=[0,sz,0])
    s.place(dep, rel_to='TBL', rotation='L', offset=[0.25*w,sz,0])
    s.place(dep, rel_to='TBL', rotation='L', offset=[0.75*w,sz,0])

    # add mid leg/support if specified
    if s.mid_offset:
      s.place(leg, rel_to='FL',  rotation='V', offset=[s.mid_offset,0,sz])
      s.place(leg, rel_to='BL',  rotation='V', offset=[s.mid_offset,0,sz])
      s.place(dep, rel_to='BL',  rotation='L', offset=[s.mid_offset,sz,0])
      s.place(dep, rel_to='TBL', rotation='L', offset=[s.mid_offset,sz,0])

    return None

class Bed8020(Item):
  def __init__(self, dim, mid_offset='M', railFactory=Rail1515):
    super().__init__(dim)
    self.railFactory = railFactory
    self.mid_offset = dim[0]/2 if mid_offset=='M' else mid_offset

  def desc(s):
    return "Bed of {0}: {1}".format(s.railFactory.__name__, s.dimStr3D())

  def render(s):
    (w,l,h) = s.dim

    # bed top
    bt = BedTop(w,l)
    s.place(bt, rel_to='TBL')

    # frame
    f = BedFrame8020([w,l,h-bt.getH()], mid_offset=s.mid_offset, railFactory=s.railFactory)
    s.place(f)

    return None
