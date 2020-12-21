from solid import *
from solid.utils import *  # Not required, but the utils module is useful
from lib.item import Item


class Plywood(Item):
  def __init__(self, dim):
    super().__init__(dim)
    self.color = (193,154,107)

  def render(s):
    return(s.c(s.color, cube(s.getDim())))

class Ply_1_2(Plywood):
  def __init__(self, w, l):
    super().__init__([w, l, 0.5])

  def desc(s):
    return "1/2\" Plywood: {0}x{1}".format(s.getW(),s.getL())
