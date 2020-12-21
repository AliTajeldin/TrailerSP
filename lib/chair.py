from solid import *
from solid.utils import *  # Not required, but the utils module is useful
from lib.item import Item
from lib.shelf import ShelfUnit

class Chair(Item):
  def __init__(self):
    super().__init__([30,20,42])
    self.chair_leg_h = 18
    self.color = (2,48,2)
    self.cushion_color = (99,112,17)
  
  def render(s):
    (w,l,h) = s.getDim()
    leg_h = s.chair_leg_h

    seat = ShelfUnit([w,l,leg_h], count=0, color=s.color).render_all()
    back = up(leg_h)(cube([w,2,h-leg_h]))
    seat = s.c(s.color, union()(seat, back))

    cushion = s.c(s.cushion_color, translate([1,1,leg_h])(cube([w-2,l-2,2])))

    return seat + cushion





