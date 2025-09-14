
from solid import *
from solid.utils import *
from lib.basic import Cube
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

  def desc(s):
    return "Lagun Table: " + s.dimStr2D()


class Table(Item):
  def __init__(self, dim, color=(31,51,105)):
    super().__init__(dim)
    self.color = color
  
  def render(s):
    (w,l,h) = s.getDim()
    color = s.color

    leg = Cube([1,1,h-1], color=color)
    top = Cube([w,l,1], color=color)
  
    s.place(leg, rel_to='BL')
    s.place(leg, rel_to='FL')
    s.place(leg, rel_to='BR')
    s.place(leg, rel_to='FR')
    s.place(top, rel_to='T')
  
    return None

  def desc(s):
    return "Table: " + s.dimStr2D()
