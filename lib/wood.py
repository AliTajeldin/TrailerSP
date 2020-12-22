from solid import *
from solid.utils import *  # Not required, but the utils module is useful
from lib.item import Item


class WoodSheet(Item):
  def __init__(self, dim, color):
    super().__init__(dim)
    self.color = color

  def render(s):
    return(s.c(s.color, cube(s.getDim())))

class Ply_1_2(WoodSheet):
  SIZE = 0.5
  def __init__(self, w, l, color=(193,154,107)):
    super().__init__([w, l, 0.5], color)

  def desc(s):
    return "1/2\" Plywood: " + s.dimStr2D()

class Ply_1(WoodSheet):
  SIZE = 1
  def __init__(self, w, l, color=(193,154,107)):
    super().__init__([w, l, 1], color)

  def desc(s):
    return "1/2\" Plywood: " + s.dimStr2D()

class Panel_1_8(WoodSheet):
  SIZE = 0.125
  def __init__(self, w, l, color=(86,54,39)):
    super().__init__([w, l, 0.125], color)

  def desc(s):
    return "1/8\" Hard Panel: " + s.dimStr2D()
