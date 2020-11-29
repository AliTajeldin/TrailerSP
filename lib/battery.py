
from solid import *
from solid.utils import *  # Not required, but the utils module is useful
from lib.item import Item


class Battery(Item):
  def __init__(self, dim):
    super().__init__(dim)
    self.color = (243, 114, 44, 180)
    self.pos_color = (255,0,0)
    self.neg_color = (0,0,0)
  
  def render(s):
    (w,l,h) = s.getDim()
    b_body = union()(
      cube([w,l,h-1]),
      translate([0.25,0.25,h-1])(cube([w-2,l-0.5,1])),
    )
    return union()(
      s.c(s.color, b_body),
      s.c(s.pos_color, translate([w-0.75,0.75,h-1])(cylinder(r=0.5,h=1))),
      s.c(s.neg_color, translate([w-0.75,l-0.75,h-1])(cylinder(r=0.5,h=1))),
    )


class Battleborn100ah(Battery):
  def __init__(self):
    super().__init__([12.8,6.9,9])
