from solid import *
from solid.utils import *  # Not required, but the utils module is useful
from lib.item import Item

BED_WIDTH_S = 24
BED_WIDTH_M = 30
BED_WIDTH_L = 36
BED_LENGTH = 6 * 12
BED_HEIGHT = 7 # 1 inch ply + 6" mattress
# BED_Z = T_HEIGHT - 38 - BED_HEIGHT # 38" sitting clearance max bed Z
BED_COLOR = (67, 170, 139)

def bed(size_v):
  (w,l,h) = size_v
  b = union()(
    cube([w,l,1]),
    translate([1,1,1])(cube([w-2,l-2,h-1]))
  )
  # return norm_color(BED_COLOR)(b)
  return (b)


class BedBase(Item):
  def __init__(self, dim):
    super().__init__(dim)
  
  def render(self):
    (w,l,h) = self.dim
    b = union()(
      cube([w,l,1]),
      translate([1,1,1])(cube([w-2,l-2,h-1]))
    )
    return self.c(BED_COLOR, b)

class BedS(BedBase):
  def __init__(self):
    super().__init__([BED_WIDTH_S, BED_LENGTH, BED_HEIGHT])

class BedM(BedBase):
  def __init__(self):
    super().__init__([BED_WIDTH_M, BED_LENGTH, BED_HEIGHT])

class BedL(BedBase):
  def __init__(self):
    super().__init__([BED_WIDTH_L, BED_LENGTH, BED_HEIGHT])

