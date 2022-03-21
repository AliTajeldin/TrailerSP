#!/usr/bin/env python

from solid import *
from solid.utils import *
from lib.basic import Cube

from lib.chair import Chair
from lib.table import Table
from lib.item import Item

LR_DIM = [154,228,101]
DR_DIM = [140,122,95]

class RickCouch(Chair):
  def __init__(self):
    super().__init__(dim=[83, 39, 37], cushion_color=(99, 112, 100))

class AliCouch(Chair):
  def __init__(self):
    super().__init__(dim=[75, 32, 37], cushion_color=(99, 112, 17))

class CoffeeTable(Table):
  def __init__(self):
      super().__init__([70, 30, 20])

class WeighBench(Item):
  def __init__(self):
      super().__init__([45, 39, 60])
  
  def render(s):
    (w,l,h) = s.getDim()
    seat_l = 54

    base = Cube([2,l,2])
    pole = Cube([2,2,h])
    bar = Cube([87,1,1], color=(193,209,193))
    seat = Table([12,seat_l,26])
    s.place(base, rel_to='BL')
    s.place(base, rel_to='BR')
    s.place(pole, rel_to='BL', offset=[0,0.8*l,0])
    s.place(pole, rel_to='BR', offset=[0,0.8*l,0])
    s.place(bar,  rel_to='CX', offset=[0,0.8*l,h])
    s.place(seat, rel_to='CX', offset=[0, (l/2.0)-seat_l, 0])

class FishingBench(Item):
  def __init__(self):
      super().__init__([66, 37, 50])
      self.color = (92, 43, 4)

  def render(s):
    (w,l,h) = s.getDim()
    c = s.color

    base_h = 35
    base = Cube([17,l,base_h], color=c)
    top = Cube([w,l, h-base_h], color=c)
    s.place(base, rel_to='BL')
    s.place(base, rel_to='BR')
    s.place(top, rel_to='T')

class TvStand(Item):
  def __init__(self):
      super().__init__([47, 21, 57])
      self.color = (17,4,46)

  def render(s):
    (w,l,h) = s.getDim()
    c = s.color
    tv_h=30

    base = Cube([w,l,20], color=c)
    arm = Cube([6,1,h], color=c)
    tv = Cube([w,3,tv_h], color=c)
    s.place(base)
    s.place(arm, rel_to='CX')
    s.place(tv, rel_to='CX', offset=[0,0,h-tv_h])

    return None

class LivingRoom(Item):
  def __init__(self, dim):
    super().__init__(dim)

  def render(s):
    s.place( RickCouch(), rel_to='FL', rotation=180, offset=[0,0,0])
    s.place( AliCouch(), rel_to='FL', offset=[0, -95, 0])
    s.place( CoffeeTable(), rel_to='FL', offset=[0, -50, 0])

    s.place( WeighBench(), rel_to='BR', rotation=180, offset=[-40,6,0])
    # s.place( WeighBench(), rel_to='BR', rotation='R', offset=[-6,40,0])
    s.place( FishingBench(), rel_to='BL', rotation='L', offset=[0,24,0])

    s.place( TvStand(), rel_to='FR', rotation='L', offset=[0,-40, 0])
    
    return None

class DiningRoom(Item):
  def __init__(self, dim):
    super().__init__(dim)

  def render(s):
    s.place( Table([48,48,27]), rel_to='BL', offset=[32,32,0])
    
    return None

class Layout(Item):
  def __init__(self, dim):
    super().__init__(dim)

  def render(s):
    lr_floor = s.c((87, 117, 144), cube([LR_DIM[0], LR_DIM[1], 0.001]))
    dr_floor = s.c((87, 117, 200), cube([DR_DIM[0], DR_DIM[1], 6]))
    lr_rail = s.c((0,0,0,100), right(LR_DIM[0])(cube([0.001, 65, 48])))
    floors = union()(
      lr_floor,
      lr_rail,
      LivingRoom(LR_DIM).render_all(),
      forward(LR_DIM[1])(dr_floor),
      translate([0,LR_DIM[1],6])(DiningRoom(DR_DIM).render_all()),
      )

    return floors

def render():
  l = Layout([0,0,0])
  return l.render_all()

