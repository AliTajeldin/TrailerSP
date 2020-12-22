from solid import *
from solid.utils import *  # Not required, but the utils module is useful
from lib.item import Item
from lib.rail8020 import Rail1515
from lib.wood import Ply_1_2

BED_TOP_HEIGHT = 6.5 # 0.5 inch ply + 6" mattress

class Mattress(Item):
  def __init__(self, w, l):
    super().__init__([w,l,BED_TOP_HEIGHT-0.5])
    self.color = (67, 170, 210)

  def desc(s):
    return "Foam Mattress: " + s.dimStr2D()

  def render(s):
    (w,l,h) = s.getDim()
    return s.c(s.color, cube([w,l,h]))

class BedTop(Item):
  def __init__(self, w, l):
    super().__init__([w,l,BED_TOP_HEIGHT])

  def desc(s):
    return "Bed Top: " + s.dimStr2D()

  def render(s):
    (w,l,h) = s.getDim()

    ply = Ply_1_2(w,l)
    s.place(ply)

    mattress = Mattress(w-1, l-1)
    s.place(mattress, offset=[0.5,0.5,0.5])

    return None
