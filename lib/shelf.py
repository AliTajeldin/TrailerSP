
from solid import *
from solid.utils import *  # Not required, but the utils module is useful
from lib.item import Item
from lib.rail8020 import Rail1515

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
  def __init__(self, w, l, railFactory, woodFactory=None):
    super().__init__([w, l, railFactory.SIZE])
    self.railFactory = railFactory
    self.woodFactory = woodFactory

  def render(s):
    (w,l,h) = s.getDim()
    sz = s.railFactory.SIZE

    d_rail = s.railFactory(l - 2*sz)
    h_rail = s.railFactory(w - 2*sz)

    s.place(h_rail, offset=[sz,0,0])
    s.place(h_rail, offset=[sz,0,0], rel_to='FL')
    s.place(d_rail, rotation='L', offset=[0,sz,0])
    s.place(d_rail, rotation='L', offset=[0,sz,0], rel_to='BR')

    if s.woodFactory:
      sheet = s.woodFactory(w - 2*sz, l)
      s.place(sheet, offset=[sz,0,sz])

    return None
