from solid import *
from solid.utils import *  # Not required, but the utils module is useful
from lib.item import Item

BURNER_WITDH=12
BOTTLE_DIAMETER=6

class Stove(Item):
  def __init__(self):
    super().__init__([BURNER_WITDH+BOTTLE_DIAMETER, BURNER_WITDH, BOTTLE_DIAMETER])
    self.color = (0,0,0)
    self.bottle_color = (0,128,0)
  
  def render(s):
    bw = BURNER_WITDH
    bd = BOTTLE_DIAMETER
    bh = bd/2
    
    legs = union()(
      cube([1,1,bh]),
      forward(bw-1)(cube([1,1,bh])),
      right(bw-1)(cube([1,1,bh])),
      translate([bw-1,bw-1,0])(cube([1,1,bh])),
    )

    top = up(bh-1)(union()(
      cube([bw,1,1]),
      forward(bw-1)(cube([bw,1,1])),
      cube([1,bw,1]),
      right(bw-1)(cube([1,bw,1])),
      translate([bw/2, bw/2, 0])(cylinder(r=0.3*bw, h=1)),
    ))

    body = s.c(s.color, union()(legs, top))

    gas = translate([bw+bd/2,0,bd/2])(rotate([-90,0,0])(cylinder(r=bd/2,h=bw)))
    gas = s.c(s.bottle_color, gas)
    return union()(body, gas)
