
from solid import *
from solid.utils import *  # Not required, but the utils module is useful
from lib.item import Item

class Water(Item):
  def __init__(self, dim):
    super().__init__(dim)
    self.color = (12, 148, 196)
  
  def render(s):
    (w,l,h) = s.getDim()
    h2o = cube([w,l,h]) - \
      translate([-1,-1,(h-3)])(cube([5,l+2,5])) - \
      translate([5,-1,h-3-1])(cube([w-6,l+2,3]))
    h2o += translate([2,l/2.0,h-3])((cylinder(r=1.5, h=3, segments=10)))
    return s.c(s.color, h2o)

class Water22L(Water):
  def __init__(self):
    super().__init__([13.75,6.75,18])

  def desc(s):
    return "5L Water Jug"

class Water20L(Water):
  def __init__(self):
    super().__init__([13.5,6.5,19])

  def desc(s):
    return "6L Water Jug"

