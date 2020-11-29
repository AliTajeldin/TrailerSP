from solid import *
from solid.utils import *  # Not required, but the utils module is useful
from lib.item import Item

class FridgeBase(Item):
  def __init__(self, dim):
    super().__init__(dim)
    self.body_color = (80,80,90)
    self.top_color = (64,140,128)
  
  def render(s):
    (w,l,h) = s.dim
    top_h = 2
    body_h = h-top_h
    f = union()(
      s.c(s.body_color, cube([w,l,body_h])),
      s.c(s.top_color, up(body_h)(cube([w,l,top_h]))),
    )
    return f

class FridgeIcecoVL35(FridgeBase):
  def __init__(self):
      super().__init__([27.2,15.2,15])

class FridgeIcecoGO20(FridgeBase):
  def __init__(self):
      super().__init__([22.4,12.6,12.4])

class FridgeAlpicoolT60(FridgeBase):
  """huge with freeze+fridge"""
  def __init__(self):
      super().__init__([28.5,14.2,21.6])
