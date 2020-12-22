from solid import *
from solid.utils import *  # Not required, but the utils module is useful
from lib.item import Item


class WoodSheet(Item):
  def __init__(self, dim):
    super().__init__(dim)
    self.color = (193,154,107)

  def render(s):
    return(s.c(s.color, cube(s.getDim())))

class Ply_1_2(WoodSheet):
  def __init__(self, w, l):
    super().__init__([w, l, 0.5])
  def desc(s):
    return "1/2\" Plywood: " + s.dimStr2D()

class Panel_1_8(WoodSheet):
  def __init__(self, w, l):
    super().__init__([w, l, 0.125])
    self.color = (86,54,39)
  def desc(s):
    return "1/8\" Hard Panel: " + s.dimStr2D()
