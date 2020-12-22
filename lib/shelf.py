
from solid import *
from solid.utils import *  # Not required, but the utils module is useful
from lib.item import Item
from lib.rail8020 import Rail1515
from lib.wood import Panel_1_8

class ShelfUnit(Item):
  def __init__(self, dim, count=3, with_back=False, color=(144, 190, 109)):
    super().__init__(dim)
    self.color = color
    self.count = count
    self.with_back = with_back
  
  def render(s):
    (w,l,h) = s.getDim()
    sep = (h-1.0) / (s.count+1)
    u = union()
    for i in range(s.count+2):
      u = u.add(up(i*sep)(cube([w,l,1])))
    v_shelf = cube([1,l,h])
    u.add([v_shelf, translate([w-1,0,0])(v_shelf)])
    if s.with_back:
      u.add(translate([0,l-1,0])(cube([w,1,h])))
    return s.c(s.color, u)

class Shelf8020(Item):
  """single shelf (not unit). assumes 8020 frame is already there"""
  def __init__(self, w, l, railFactory=Rail1515, woodFactory=Panel_1_8, numSupports=1):
    super().__init__([w, l, railFactory.SIZE])
    self.railFactory = railFactory
    self.woodFactory = woodFactory
    self.numSupports = numSupports

  def render(s):
    (w,l,h) = s.getDim()
    sz = s.railFactory.SIZE

    h_rail = s.railFactory(w - 2*sz)
    s.place(h_rail, offset=[sz,0,0])
    s.place(h_rail, offset=[sz,0,0], rel_to='FL')

    d_rail = s.railFactory(l - 2*sz)
    off = (w-sz) / (s.numSupports+1)
    for i in range(s.numSupports+2):
      s.place(d_rail, rotation='L', offset=[i * off,sz,0])

    if s.woodFactory:
      sheet = s.woodFactory(w - 2*sz, l)
      s.place(sheet, offset=[sz,0,sz])

    return None

class ShelfUnit8020(Item):
  def __init__(self, dim, count=3, railFactory=Rail1515,
               woodFactory=Panel_1_8, numSupports=1):
    super().__init__(dim)
    self.count = count
    self.railFactory = railFactory
    self.woodFactory = woodFactory
    self.numSupports = numSupports

  def render(s):
    (w,l,h) = s.getDim()
    sz = s.railFactory.SIZE

    # vertical rails
    vrail = s.railFactory(h - 2*sz)
    s.place(vrail, rel_to='FL', rotation='YL', offset=[0,0,sz])
    s.place(vrail, rel_to='BL', rotation='YL', offset=[0,0,sz])
    s.place(vrail, rel_to='FR', rotation='YL', offset=[0,0,sz])
    s.place(vrail, rel_to='BR', rotation='YL', offset=[0,0,sz])

    # horizontal rails along width
    rw = s.railFactory(w)
    s.place(rw, rel_to='FL')
    s.place(rw, rel_to='BL')
    s.place(rw, rel_to='TFL')
    s.place(rw, rel_to='TBL')

    # horizontal rails along depth
    rd = s.railFactory(l - 2*sz)
    s.place(rd, rel_to='BL', rotation='L', offset=[0,sz,0])
    s.place(rd, rel_to='BR', rotation='L', offset=[0,sz,0])
    s.place(rd, rel_to='TBL', rotation='L', offset=[0,sz,0])
    s.place(rd, rel_to='TBR', rotation='L', offset=[0,sz,0])

    # shelves
    vsep = (h-sz) / (s.count+1)
    for i in range(s.count):
      shelf = Shelf8020(w,l, railFactory=s.railFactory, woodFactory=s.woodFactory, numSupports=s.numSupports)
      s.place(shelf, offset=[0,0,(i+1)*vsep])

    return None