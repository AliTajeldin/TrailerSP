from solid import *
from solid.utils import *  # Not required, but the utils module is useful
from lib.item import Item


class Rail8020(Item):
  def __init__(self, size, length, color):
    super().__init__([size,length,size])
    self.color = color
  
  def render(s):
    (w,l,h) = s.getDim()
    rw = 0.37 * w # rail edge width (for a single triangle)
    rt = 0.09 * w # rail thickness

    p1 = polygon([(0,0), (rw,0), (rw,rt), (0.55*rw,rt), (0.55*rw + w/2,rt+w/2),
                 (rt+w/2,0.55*rw + w/2), (rt,0.55*rw), (rt,rw), (0,rw)])
    
    p2 = translate([w,0])(rotate(90)(p1))
    p3 = translate([w, w])(rotate(180)(p1))
    p4 = translate([0,w])(rotate(-90)(p1))

    r = linear_extrude(height=l)(p1+p2+p3+p4)
    r = s.c(s.color, up(w)(rotate([0,90,0])(r)))
    return r

class Rail1515(Rail8020):
  def __init__(self, length, color=(219,90,178)):
    super().__init__(1.5, length, color)

class Rail2020(Rail8020):
  def __init__(self, length, color=(84, 227, 136)):
    super().__init__(2.0, length, color)
