from solid import *
from solid.utils import *  # Not required, but the utils module is useful
from lib.item import Item

INCH_MM = 0.0393701


class Rail8020(Item):
  def __init__(self, size, length, color):
    super().__init__([length,size,size])
    self.color = color
    self.size = size
    self.length = length
  
  def desc(s):
    return type(s).__name__ + ': ' + str(s.length)

  def render(self):
    s = self.size
    rw = 0.37 * s # rail edge width (for a single triangle)
    rt = 0.09 * s # rail thickness

    p1 = polygon([(0,0), (rw,0), (rw,rt), (0.55*rw,rt), (0.55*rw + s/2,rt+s/2),
                 (rt+s/2,0.55*rw + s/2), (rt,0.55*rw), (rt,rw), (0,rw)])
    
    p2 = translate([s,0])(rotate(90)(p1))
    p3 = translate([s, s])(rotate(180)(p1))
    p4 = translate([0,s])(rotate(-90)(p1))

    r = linear_extrude(height=self.length)(p1+p2+p3+p4)
    r = self.c(self.color, up(s)(rotate([0,90,0])(r)))
    return r

class Rail1515(Rail8020):
  def __init__(self, length, color=(84, 227, 136)):
    super().__init__(1.5, length, color)

class Rail1010(Rail8020):
  def __init__(self, length, color=(193, 235, 56)):
    super().__init__(1.0, length, color)

class Rail2020(Rail8020):
  def __init__(self, length, color=(219,90,178)):
    super().__init__(20 * INCH_MM, length, color)

class Rail4040(Rail8020):
  def __init__(self, length, color=(219,90,178)):
    super().__init__(40 * INCH_MM, length, color)
