
from solid import *
from solid.utils import *  # Not required, but the utils module is useful
from lib.item import Item


class LagunTable(Item):
  def __init__(self, dim):
    super().__init__(dim)
    self.color = (135, 65, 68, 128)
  
  def render(s):
    (w,l,h) = s.getDim()

    t = up(h-1)(cube([w,l,1])) + \
      translate([1,1,0])(cylinder(r=1, h=h))
    return s.c(s.color, t)
