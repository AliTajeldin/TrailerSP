from solid import *
from solid.utils import *  # Not required, but the utils module is useful
from lib.item import Item
from lib.shelf import ShelfUnit, ShelfUnit8020
from lib.rail8020 import Rail1515

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

class Chair8020(Item):
  def __init__(self):
    super().__init__([31,20,42])
    self.chair_leg_h = 19
    self.color = (144, 190, 109)
    self.cushion_color = (99,112,17)

  def render(s):
    (w,l,h) = s.getDim()
    leg_h = s.chair_leg_h

    seat = ShelfUnit8020([w,l,leg_h], count=0, railFactory=Rail1515, has_top_shelf=True)
    s.place(seat)

    back = s.c(s.color, up(leg_h)(cube([w,2,h-leg_h])))
    cushion = s.c(s.cushion_color, translate([1,1,leg_h])(cube([w-2,l-2,2])))

    return back + cushion
