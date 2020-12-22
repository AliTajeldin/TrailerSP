from solid import *
from solid.utils import *  # Not required, but the utils module is useful
from lib.item import Item

# space between panels
PANEL_SEP=2
PANEL_H=1

class SolarBase(Item):
  def __init__(self, panel_w, panel_l, count):
    self.panel_w = panel_w
    self.panel_l = panel_l
    self.color = (243, 114, 44, 100)
    self.count = count
    w = count * (panel_w + PANEL_SEP) - PANEL_SEP
    super().__init__((panel_l,w,PANEL_H))

  def render(s):
    sd = s.panel_w + PANEL_SEP
    ss = union()
    for i in range(s.count):
      ss.add(forward(i*sd)(cube([s.panel_l,s.panel_w,PANEL_H])))
    return s.c(s.color, ss)

class SolarRenegy300w(SolarBase):
  def __init__(self):
    super().__init__(40, 65, 3)

  def desc(s):
    return "Renegy Solar Panel 300W"

class SolarRenegy200w(SolarBase):
  def __init__(self):
    super().__init__(26, 64, 4)

  def desc(s):
    return "Renegy Solar Panel 200W"
