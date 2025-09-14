#!/usr/bin/env python

from solid import *
from solid.utils import *
from lib.basic import Cube
from lib.shelf import ShelfUnit8020, ShelfUnitPly
from lib.chair import Chair
from lib.table import Table
from lib.item import Item, addOffsets
from lib.bed import Bed
from lib.cutout import Door, Window

BR_DIM = [12.4 * 12, 14.55 * 12, 10 * 12]

class CoffeeTable(Table):
  def __init__(self):
      super().__init__([70, 30, 20])

class Desk(Item):
  def __init__(self):
      super().__init__([35,20,53])
      self.color=(80,80,80)
  
  def render(s):
    (w,l,h) = s.getDim()
    bot = Cube([w,l,h/2], color=s.color)
    top = Cube([w,l/2,h/2], color=s.color)
    dl=11.5
    dh=0.5
    drawer = Cube([w,dl,dh], color=s.color)

    s.place(bot)
    s.place(top, offset=[0,l/2,h/2])
    s.place(drawer, offset=[0,-dl, h/2-dh-4])

    return None

class BedRoom(Item):
  def __init__(self):
    super().__init__(BR_DIM)

  def render(s):
    block1 = Cube([19,57,s.getH()], color=(218, 232, 247))
    block2 = Cube([67,17,s.getH()], color=(218, 232, 247))
    floor = Cube([s.getW(), s.getL(), 0.001], color=(87, 117, 144))
    door = Door(35, 81)
    window = Window(34, 58)

    s.place(floor)
    s.place(block1, rel_to="FL")
    s.place(block2, rel_to="FL", rel_to_item=(block1, "R"))
    s.place(door, rel_to="FR", rotation="L", offset=[0,-7,0])
    s.place(window, offset=[0, 21, 24], rotation="L")
    s.place(window, offset=[0, 60, 24], rotation="L")

    # small/large short drawers
    drawer1S = ShelfUnit8020([15,12,24], count=2, has_top_shelf=True)
    drawer2S = ShelfUnit8020([16,18,24], count=1, has_top_shelf=True)
    # small/large tall drawers stack (of two drawers)
    drawer1T = ShelfUnit8020([15,12,48], count=5, has_top_shelf=True)
    drawer2T = ShelfUnit8020([16,18,48], count=4, has_top_shelf=True)

    charger = Cube([25,18,36], color = (237, 232, 208))
    elec_table = Table([71,29,28], color=(200,200,200))
    elec_shelf_1 = ShelfUnitPly([31,12,48], count=2, with_back=True)
    elec_shelf_2 = ShelfUnitPly([29,12,48], count=2, with_back=True)
    desk = Desk()
    food_table = Table([20,16,30], color=(20,20,20))
    chair = Chair(dim=[29,23,46])
    bed = Bed()
    nightstand = Cube([22, 15, 24], color=(20,20,20))

    s.place(drawer1S, rel_to_item=[(block1,"R"), (block2,"B")])
    s.place(desk, rel_to_item=[(drawer1S,"R"), (block2,"B")], offset=[1,0,0])
    chair_off = addOffsets(desk.getRPos(), [2, -15-chair.getL(), 0])
    s.place(chair, offset=chair_off)
    food_off = addOffsets(chair.getRPos(), [4+chair.getW(), 0, 0])
    s.place(food_table, offset=food_off, rotation="L")
    s.place(drawer2S, rel_to_item=[(desk,"R"), (block2,"B")], offset=[1,0,0])

    s.place(charger, rotation="L", rel_to_item=(block1,"B"))
    s.place(elec_table, rotation="L", rel_to_item=(charger,"B"), offset=[0,-8,0])

    s.place(elec_shelf_1, rotation=180,)
    s.place(elec_shelf_2, rotation=180, rel_to_item=(elec_shelf_1,"R"), offset=[10,0,0])
    s.place(bed, rel_to="BR")
    s.place(nightstand, rotation="L", rel_to="BR", rel_to_item=(bed,"F"), offset=[0,1,0])

    dy = 89
    dx = drawer1T.getW()
    s.place(drawer1T, rel_to="BR", offset=[0,dy,0])
    s.place(drawer1T, rel_to="BR", offset=[-dx,dy,0])
    s.place(drawer1T, rel_to="BR", offset=[-2*dx,dy,0])
    dy = dy + 12
    dx2 = drawer2T.getW()
    s.place(drawer2T, rel_to="BR", offset=[0,dy,0])
    s.place(drawer1T, rel_to="BR", offset=[-dx2,dy,0])
    s.place(drawer1T, rel_to="BR", offset=[-dx2-dx,dy,0])
    return None


def render():
  b = BedRoom()
  return b.render_all()

