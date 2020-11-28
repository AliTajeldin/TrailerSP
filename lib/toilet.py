
from solid import *
from solid.utils import *  # Not required, but the utils module is useful
from lib.item import Item


class Toilet(Item):
  def __init__(self, dim):
    super().__init__(dim)
    self.color = (0,255,255)
  
  def render(s):
    (w,l,h) = s.getDim()
    r = w/2.0
    c = hull()(cylinder(r=r, h=h) + forward(l-r)(cylinder(r=r, h=h)))
    c -= up(h)(sphere(r=r-2))
    t = translate([r,r,0])(c)
    return s.c(s.color, t)

class DryFlushToilet(Toilet):
  def __init__(self):
    super().__init__([16,20,18])

