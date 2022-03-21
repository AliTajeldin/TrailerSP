from solid import *
from solid.utils import *  # Not required, but the utils module is useful
from lib.item import Item


class Cube(Item):
  def __init__(self, dim, color=(31, 105, 33)):
    super().__init__(dim)
    self.color = color
  
  def render(s):
    return s.c(s.color, cube(s.getDim()))
