from solid import *
from solid.utils import *  # Not required, but the utils module is useful
import math as M

from lib.item import Item
from lib.bed import BedTop
from lib.shell import SilverEagle, SilverStar
from lib.solar import SolarRenegy200w, SolarRenegy300w
from lib.fridge import FridgeIcecoGO20, FridgeIcecoVL35, FridgeAlpicoolT60
from lib.water import Water5L, Water6L
from lib.shelf import ShelfUnit, ShelfUnit8020, Shelf8020
from lib.battery import Battleborn100ah
from lib.toilet import DryFlushToilet
from lib.stove import Stove
from lib.chair import Chair
from lib.table import LagunTable
from lib.rail8020 import Rail1515, Rail1010, Rail2020
from lib.wood import Ply_1_2, Ply_1, Panel_1_8

class RearBedLayout(Item):
  def __init__(self):
    super().__init__([1000,1000,1000])

  def desc(s):
    return "Rear bed layout with garage under bed"

  def render(self):
    # --- Config ---
    # s = SilverEagle()
    s = SilverStar()
    bed = BedTop(s.getW(), 36)
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

    # --- bed ---
    bed_z = sh - bh - 38
    s.place(bed, offset=[0,0,bed_z])
    bed_shelf = ShelfUnit8020((bl, shelf_depth, 24), count=1, has_bottom_shelf=True, desc="above bed")
    s.place(bed_shelf, rotation='R', rel_to='TBR')

    # --- garage ---
    g_shelf_off = 48
    gs1 = ShelfUnit8020([g_shelf_off,bl,bed_z], count=2, railFactory=Rail1515, desc="left garage")
    gs2 = ShelfUnit8020([sw-g_shelf_off,bl,bed_z], count=1, railFactory=Rail1515, numSupports=0, desc="right garage")
    s.place(gs1)
    s.place(gs2, rel_to='BR')

    # --- solar ---
    solar_x_off = (sw - solar.getW()) / 2.0
    s.place(solar, offset=[solar_x_off,0,sh])

    # --- right side shelf (between kitchen and bed) ---
    right_shelf_w = sl - s.door_off - s.door_w - kitchen_w - gl
    mrs = ShelfUnit8020((right_shelf_w,shelf_depth,sh), count=6, skip=1, desc="mid right shelf")
    s.place(mrs, rel_to='BR', rotation='R', offset=[0,gl,0])

    # --- kitchen/cooking area ---
    kh = s.vnose_h
    kc = (216, 230, 92)
    k_off = gl + right_shelf_w
    kus = ShelfUnit8020((kitchen_w, shelf_depth, kh), count=2, has_top_shelf=True, desc="kitchen unit")
    s.place(kus, rel_to='BR', rotation='R', offset=[0,k_off,0])

    spice_rack = ShelfUnit((shelf_depth, 4, sh-kh), count=3, color=kc, with_back=True, desc="spice rack")
    s.place(spice_rack, rel_to='BR', rotation=180, offset=[0,k_off,kh])

    stove_off = s.door_off + s.door_w + 1
    s.place(Stove(), rel_to='FR', rotation='R', offset=[-1,-stove_off,kh])

    # --- toilet ---
    s.place(toilet, rel_to='BR', offset=[-2,gl+2,0])

    # --- elect cabinet (bat + chargers) ---
    bat_y_off = gl + 2
    s.place(bat, rel_to='BL', rotation='L', offset=[2,bat_y_off,0])
    s.place(bat, rel_to='BL', rotation='L', offset=[3 + bat.getL(),bat_y_off,0])

    # --- chair ---
    s.place(chair, rel_to='FL', rotation='R')

    # --- fridge ---
    s.place(fridge, rel_to='FL', rotation='R', offset=[2,-1,1])

    # --- long side shelf ---
    # use two shelfs instead of one long one for shorter pieces
    long_shelf_w = sl - gl - chair.getW()
    ls1_w = 36
    ls2_w = long_shelf_w - ls1_w
    ls1 = ShelfUnit8020((ls1_w, shelf_depth, sh), count=6, numSupports=1, skip=1, desc="left long side shelf")
    ls2 = ShelfUnit8020((ls2_w, shelf_depth, sh), count=4, numSupports=2, skip=0, desc="right long side shelf")
    s.place(ls1, rel_to='BL', rotation='L', offset=[0,gl,0])
    s.place(ls2, rel_to='BL', rotation='L', offset=[0,gl+ls1_w,0])

    # --- table ---
    s.place(table, rel_to='FL', rotation=180, offset=[chair.getL()-table.getW()+2,0,0])

    # --- water ---
    s.place(water, rel_to='FL', offset=[sw/4.0,s.vnose_l,0], rotation=180)
    s.place(water, rel_to='FR', offset=[-sw/4.0,s.vnose_l,0])

    # --- cross braces to stabalize the shelves ---
    xb = Rail1010(sw - 2 * shelf_depth, color=(0,0,0))
    s.place(xb, rel_to='TBL', offset=[shelf_depth,gl,0])
    s.place(xb, rel_to='TBL', offset=[shelf_depth,gl+ls1_w,0])
    s.place(xb, rel_to='TBL', offset=[shelf_depth,gl+ls1_w-1,0])
    s.place(xb, rel_to='TBL', offset=[shelf_depth,gl+right_shelf_w-1,0])

    self.place(s)
    return None
