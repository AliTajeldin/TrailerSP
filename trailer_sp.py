#!/usr/bin/env python

from solid import *
from solid.utils import *  # Not required, but the utils module is useful
import math as M

from lib.bed import BedTop
from lib.shell import SilverEagle, SilverStar
from lib.solar import SolarRenegy200w, SolarRenegy300w
from lib.fridge import FridgeIcecoGO20, FridgeIcecoVL35, FridgeAlpicoolT60
from lib.water import Water5L, Water6L
from lib.shelf import Shelf
from lib.battery import Battleborn100ah
from lib.toilet import DryFlushToilet
from lib.stove import Stove
from lib.chair import Chair
from lib.table import LagunTable

def side_back_bed_layout():
    # --- Config ---
  s = SilverEagle()
  # s = SilverStar()
  bed = BedTop(30, 6*12)
  fridge = FridgeIcecoVL35()
  solar = SolarRenegy200w()
  toilet = DryFlushToilet()
  bat = Battleborn100ah()
  water = Water6L()
  chair = Chair()
  table = LagunTable([12,24,33])
  shelf_depth = 18 # depth of side shelfs
  gl = 30 # garage length (depth)

  # --- Aliases ---
  (sw,sl,sh) = s.getDim()
  (bw,bl,bh) = bed.getDim()

  # --- bed ---
  bed_z = sh - 38 - bh # 38" sitting clearance max bed Z
  s.place( bed, rel_to='BR', offset=[0,0,bed_z])
  bed_shelf_h = sh - bed_z - bh - 12
  s.place( Shelf((bw, shelf_depth, bed_shelf_h), count=1), rel_to='TBR')

  # --- solar ---
  solar_x_off = (sw - solar.getW()) / 2.0
  s.place(solar, offset=[solar_x_off,0,sh])

  # --- garage ---
  gc = (249, 199, 79) # garage color
  s.place( Shelf((bw, gl, bed_z), count=0, with_back=True, color=gc), rel_to='BR')
  s.place( Shelf((sw-bw, gl, bed_z), count=2, with_back=True, color=gc), rel_to='BL')

  # --- kitchen/cooking area ---
  kw = sl - bl - s.door_w - s.door_off
  kh = s.vnose_h
  kc = (216, 230, 92)
  k_off = bl
  s.place( Shelf((kw, bw, kh), count=1, color=kc),
           rel_to='BR', rotation='R', offset=[0,k_off,0])
  s.place( Shelf((bw, 4, sh-kh), count=3, color=kc, with_back=True),
           rel_to='BR', rotation=180, offset=[0,k_off,kh])
  stove_off = s.door_off + s.door_w
  s.place(Stove(), rel_to='FR', rotation='R', offset=[-5,-stove_off-5,kh])

  # --- toilet ---
  s.place(toilet, rel_to='BR', offset=[0,gl,0])

  # --- elect cabinet (bat + chargers) ---
  bat_y_off = bl - bat.getW()
  s.place(bat, rel_to='BR', rotation='L', offset=[0,bat_y_off,0])
  s.place(bat, rel_to='BR', rotation='L', offset=[-bat.getL() - 1,bat_y_off,0])

  # --- chair ---
  s.place(chair, rel_to='FL', rotation='R')

  # --- fridge ---
  s.place(fridge, rel_to='FL', rotation='R', offset=[2,-1,1])

  # --- long side shelf ---
  long_shelf_w = sl - gl - chair.getW()
  s.place( Shelf((long_shelf_w, shelf_depth, sh), count=3),
           rel_to='BL', rotation='L', offset=[0,gl,0])

  # --- table ---
  s.place(table, rel_to='FL', rotation=180, offset=[chair.getL()-table.getW()+2,0,0])

  # --- water ---
  s.place(water, rel_to='FL', offset=[sw/4.0,s.vnose_l,0], rotation=180)
  s.place(water, rel_to='FR', offset=[-sw/4.0,s.vnose_l,0])

  # small shelfs in back
  ssh = sh - bed_z # height of small shelfs in back
  s_opt_c = (135, 65, 68, 128)
  s_opt_w = sw - bw - shelf_depth
  s.place( Shelf((gl, shelf_depth, ssh), count=3),
           rel_to='BL', rotation='L', offset=[0,0,bed_z])
  s.place( Shelf((s_opt_w, shelf_depth, ssh), count=3, color=s_opt_c),
           rel_to='BL', offset=[shelf_depth,0,bed_z])

  # --- render entire trailer ---
  return s.render_all()


def rear_bed_layout():
  # --- Config ---
  s = SilverEagle()
  # s = SilverStar()
  bed = BedTop(36, s.getW())
  fridge = FridgeIcecoVL35()
  solar = SolarRenegy200w()
  toilet = DryFlushToilet()
  bat = Battleborn100ah()
  water = Water6L()
  chair = Chair()
  table = LagunTable([12,24,33])
  kitchen_w = 2.5 * 12
  shelf_depth = 20 # depth of side shelfs

  # --- Aliases ---
  (sw,sl,sh) = s.getDim()
  (bw,bl,bh) = bed.getDim()
  elect_box_h = toilet.getH() + 2
  elect_box_w = sl - s.door_off - s.door_w - kitchen_w - bw

  # --- bed ---
  bed_z = sh - 38 - bh # 38" sitting clearance max bed Z
  s.place( bed, rotation='L', offset=[0,0,bed_z])
  bed_shelf_h = sh - bed_z - bh - 12
  s.place( Shelf((bw, shelf_depth, bed_shelf_h), count=1),
           rotation='R', rel_to='TBR')

  # --- solar ---
  solar_x_off = (sw - solar.getW()) / 2.0
  s.place(solar, offset=[solar_x_off,0,sh])

  # --- garage ---
  gl = bw # set garage depth same as bed
  gc = (249, 199, 79) # garage color
  s.place( Shelf((bw, gl, bed_z), count=0, with_back=True, color=gc), rel_to='BR')
  s.place( Shelf((sw-bw, gl, bed_z), count=2, with_back=True, color=gc), rel_to='BL')

  # --- obs: over battery shelf ---
  obs_w = elect_box_w
  obs_z = elect_box_h
  obs_h = sh - obs_z
  s.place( Shelf((obs_w,shelf_depth,obs_h), count=4),
           rel_to='BR', rotation='R', offset=[0,bw,obs_z])

  # --- kitchen/cooking area ---
  kh = s.vnose_h
  kc = (216, 230, 92)
  k_off = bw + obs_w
  s.place( Shelf((kitchen_w, shelf_depth, kh), count=1, color=kc),
           rel_to='BR', rotation='R', offset=[0,k_off,0])
  s.place( Shelf((shelf_depth, 4, sh-kh), count=3, color=kc, with_back=True),
           rel_to='BR', rotation=180, offset=[0,k_off,kh])
  stove_off = s.door_off + s.door_w + 1
  s.place(Stove(), rel_to='FR', rotation='R', offset=[-1,-stove_off,kh])

  # --- toilet ---
  s.place(toilet, rel_to='BR', offset=[0,gl,0])

  # --- elect cabinet (bat + chargers) ---
  bat_y_off = k_off - bat.getW()
  s.place(bat, rel_to='BR', rotation='L', offset=[0,bat_y_off,0])
  s.place(bat, rel_to='BR', rotation='L', offset=[-bat.getL() - 1,bat_y_off,0])

  # --- chair ---
  s.place(chair, rel_to='FL', rotation='R')

  # --- fridge ---
  s.place(fridge, rel_to='FL', rotation='R', offset=[2,-1,1])

  # --- long side shelf ---
  long_shelf_w = sl - gl - chair.getW()
  s.place( Shelf((long_shelf_w, shelf_depth, sh), count=3),
           rel_to='BL', rotation='L', offset=[0,gl,0])

  # --- table ---
  s.place(table, rel_to='FL', rotation=180, offset=[chair.getL()-table.getW()+2,0,0])

  # --- water ---
  s.place(water, rel_to='FL', offset=[sw/4.0,s.vnose_l,0], rotation=180)
  s.place(water, rel_to='FR', offset=[-sw/4.0,s.vnose_l,0])

  # --- render entire trailer ---
  return s.render_all()

# t = side_back_bed_layout()
# t = rear_bed_layout()
from lib.bed import Bed8020
b = Bed8020([6*12, 36, 40])
t = b.render_all()
b.bom.print()
# print(b.bom._group_children())

# from lib.rail8020 import Rail1010, Rail1515, Rail2020
# t = union()(Rail1010(3).render_all(), forward(4)(Rail1515(3).render_all()))
scad_render_to_file(union()(t))
    

