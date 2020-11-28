from solid import *
from solid.utils import *  # Not required, but the utils module is useful
from lib.item import Item

class SolarBase(Item):
  def __init__(self, w, l, count):
    super().__init__((w,l,1.5))
    self.color = (243, 114, 44, 100)
    self.count = count

  def render(s):
    (w,l,h) = s.getDim()
    sd = w + 2.0 # each panel has 2 inch in between
    ss = union()
    for i in range(s.count):
      ss.add(forward(i*sd)(cube([l,w,h])))
    return s.c(s.color, ss)

class SolarRenegy300w(SolarBase):
  def __init__(self):
    super().__init__(40, 65, 3)

class SolarRenegy200w(SolarBase):
  def __init__(self):
    super().__init__(26, 64, 4)
