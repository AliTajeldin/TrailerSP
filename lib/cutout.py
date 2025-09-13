from solid import *
from solid.utils import *  # Not required, but the utils module is useful

from lib.item import Item

class Cutout(Item):
  def __init__(self, w, l, frame_thickness, frame_width):
    super().__init__([w,frame_thickness,l])
    self.color = (87, 117, 144)
    self.frame_thickness = frame_thickness
    self.frame_width = frame_width

  def render(s):
    (w,l,h) = s.getDim()
    ft = s.frame_thickness
    fw = s.frame_width
    frame = cube([w, ft, h]) - \
      translate([fw,-ft,fw])(cube([w-2*fw, 3*ft, h-2*fw]))
    return s.c(s.color, frame)

class Window(Cutout):
  def __init__(self, w, l, frame_thickness=0.1, frame_width=2):
    super().__init__(w,l,frame_thickness,frame_width)
    self.color = (87, 117, 144)

  def desc(s):
    return "Window: " + s.dimStr3D()

class Door(Cutout):
  def __init__(self, w, l, frame_thickness=0.1, frame_width=2):
    super().__init__(w,l,frame_thickness,frame_width)
    self.color = (80, 80, 200)

  def desc(s):
    return "Door: " + s.dimStr3D()
