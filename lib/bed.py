from solid import *
from solid.utils import *  # Not required, but the utils module is useful
from lib.item import Item

BED_WIDTH_S = 24
BED_WIDTH_M = 30
BED_WIDTH_L = 36
BED_HEIGHT = 7 # 1 inch ply + 6" mattress

class BedBase(Item):
  def __init__(self, dim):
    super().__init__(dim)
    self.color = (67, 170, 139)
  
  def render(s):
    (w,l,h) = s.dim
    b = union()(
      cube([w,l,1]),
      translate([1,1,1])(cube([w-2,l-2,h-1]))
    )
    return s.c(s.color, b)

class BedS(BedBase):
  def __init__(self, bed_l):
    super().__init__([BED_WIDTH_S, bed_l, BED_HEIGHT])

class BedM(BedBase):
  def __init__(self, bed_l):
    super().__init__([BED_WIDTH_M, bed_l, BED_HEIGHT])

class BedL(BedBase):
  def __init__(self, bed_l):
    super().__init__([BED_WIDTH_L, bed_l, BED_HEIGHT])

