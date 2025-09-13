#!/usr/bin/env python

from solid import *
from solid.utils import *
from lib.basic import Cube
from lib.shelf import ShelfUnit8020
from lib.chair import Chair
from lib.table import Table
from lib.item import Item
from lib.bed import Bed
from lib.cutout import Door, Window

BR_DIM = [12.41 * 12, 14.84 * 12, 10 * 12]

class CoffeeTable(Table):
  def __init__(self):
      super().__init__([70, 30, 20])

class WeighBench(Item):
  def __init__(self):
      super().__init__([45, 39, 60])
  
  def render(s):
    (w,l,h) = s.getDim()
    seat_l = 53

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

class BedRoom(Item):
  def __init__(self):
    super().__init__(BR_DIM)

  def render(s):
    block1 = Cube([19,39.5,s.getH()], color=(218, 232, 247))
    block2 = Cube([67,17,s.getH()], color=(218, 232, 247))
    floor = Cube([s.getW(), s.getL(), 0.001], color=(87, 117, 144))
    door = Door(35, 81)
    window = Window(34, 58)
    bed = Bed()

    s.place(floor )
    s.place(block1, rel_to="FL")
    s.place(block2, rel_to="FL", rel_to_item=(block1, "R"))
    s.place(door, rel_to="FR", rotation="L", offset=[0,-7,0])
    s.place(window, offset=[0, 21, 24], rotation="L")
    s.place(window, offset=[0, 60, 24], rotation="L")

    s.place(bed, rel_to="BR")
    
    s.place(Cube([24,24,24]), rel_to_item=[(block1,"R"), (block2,"B")])
    
    return None


def render():
  b = BedRoom()
  return b.render_all()

