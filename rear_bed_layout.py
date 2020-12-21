from solid import *
from solid.utils import *  # Not required, but the utils module is useful
import math as M

from lib.bed import BedTop, Bed8020
from lib.shell import SilverEagle, SilverStar
from lib.solar import SolarRenegy200w, SolarRenegy300w
from lib.fridge import FridgeIcecoGO20, FridgeIcecoVL35, FridgeAlpicoolT60
from lib.water import Water5L, Water6L
from lib.shelf import ShelfUnit
from lib.battery import Battleborn100ah
from lib.toilet import DryFlushToilet
from lib.stove import Stove
from lib.chair import Chair
from lib.table import LagunTable
from lib.rail8020 import Rail1515
from lib.shelf import Shelf8020
from lib.wood import Ply_1_2, Panel_1_8

def rear_bed_layout():
  # --- Config ---
  s = SilverEagle()
  # s = SilverStar()
  g_shelf_w = 40
  bed = Bed8020([s.getW(), 36, s.getH() - 38], mid_offset=g_shelf_w-1.5)
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
  gl = bl # set garage depth same as bed
  elect_box_h = toilet.getH() + 2
  elect_box_w = sl - s.door_off - s.door_w - kitchen_w - gl

  # --- bed ---
  s.place(bed)
  s.place( ShelfUnit((bl, shelf_depth, 24), count=1),
           rotation='R', rel_to='TBR')
  gs = Shelf8020(g_shelf_w, bl, Rail1515)
  s.place(gs, offset=[0,0,15])

  # --- solar ---
  solar_x_off = (sw - solar.getW()) / 2.0
  s.place(solar, offset=[solar_x_off,0,sh])

  # --- obs: over battery shelf ---
  obs_w = elect_box_w
  obs_z = elect_box_h
  obs_h = sh - obs_z
  s.place( ShelfUnit((obs_w,shelf_depth,obs_h), count=4),
           rel_to='BR', rotation='R', offset=[0,gl,obs_z])

  # --- kitchen/cooking area ---
  kh = s.vnose_h
  kc = (216, 230, 92)
  k_off = gl + obs_w
  s.place( ShelfUnit((kitchen_w, shelf_depth, kh), count=1, color=kc),
           rel_to='BR', rotation='R', offset=[0,k_off,0])
  s.place( ShelfUnit((shelf_depth, 4, sh-kh), count=3, color=kc, with_back=True),
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
  s.place( ShelfUnit((long_shelf_w, shelf_depth, sh), count=3),
           rel_to='BL', rotation='L', offset=[0,gl,0])

  # --- table ---
  s.place(table, rel_to='FL', rotation=180, offset=[chair.getL()-table.getW()+2,0,0])

  # --- water ---
  s.place(water, rel_to='FL', offset=[sw/4.0,s.vnose_l,0], rotation=180)
  s.place(water, rel_to='FR', offset=[-sw/4.0,s.vnose_l,0])

  # --- render entire trailer ---
  return s.render_all()
