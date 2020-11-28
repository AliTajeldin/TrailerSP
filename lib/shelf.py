
from solid import *
from solid.utils import *  # Not required, but the utils module is useful
from lib.item import Item

class Shelf(Item):
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
