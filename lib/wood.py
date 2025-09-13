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
    return "1\" Plywood: " + s.dimStr2D()

class Panel_1_8(WoodSheet):
  SIZE = 0.125
  def __init__(self, w, l, color=(86,54,39)):
    super().__init__([w, l, 0.125], color)

  def desc(s):
    return "1/8\" Hard Panel: " + s.dimStr2D()

class Lumber(Item):
  def __init__(self, l, color=None):
    super().__init__([l, self.SIZE[1], self.SIZE[0]])
    self.color = color if color else  (246,213,131)

  def desc(s):
    return "Lumber {0}: {1}".format(s.SIZE_STR, s.getW())

  def render(s):
    return(s.c(s.color, cube(s.getDim())))

class Lumber_2_4(Lumber):
  SIZE=[1.5,3.5]
  SIZE_STR='2x4'
  def __init__(self, l, color=None):
    super().__init__(l, color)

class Lumber_2_6(Lumber):
  SIZE=[1.5,5.5]
  SIZE_STR='2x6'
  def __init__(self, l, color=None):
    super().__init__(l, color)

class Lumber_2_8(Lumber):
  SIZE=[1.5,7.25]
  SIZE_STR='2x8'
  def __init__(self, l, color=None):
    super().__init__(l, color)

class Lumber_1_1(Lumber):
  SIZE=[0.75,0.75]
  SIZE_STR='1x1'
  def __init__(self, l, color=None):
    super().__init__(l, color)

class Lumber_1_2(Lumber):
  SIZE=[0.75,1.5]
  SIZE_STR='1x2'
  def __init__(self, l, color=None):
    super().__init__(l, color)

class Lumber_1_3(Lumber):
  SIZE=[0.75,2.5]
  SIZE_STR='1x3'
  def __init__(self, l, color=None):
    super().__init__(l, color)

class Lumber_1_4(Lumber):
  SIZE=[0.75,3.5]
  SIZE_STR='1x4'
  def __init__(self, l, color=None):
    super().__init__(l, color)
