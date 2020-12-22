from solid import *
from solid.utils import *  # Not required, but the utils module is useful
import math as M

from lib.item import Item
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

class SideBedLayout(Item):
  def __init__(self):
    super().__init__([1000,1000,1000])

  def desc(s):
    return "Side bed layout with electric under bed"

  def render(self):
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
    s.place( ShelfUnit((bw, shelf_depth, bed_shelf_h), count=1, desc="Above bed"), rel_to='TBR')

    # --- solar ---
    solar_x_off = (sw - solar.getW()) / 2.0
    s.place(solar, offset=[solar_x_off,0,sh])

    # --- garage ---
    gc = (249, 199, 79) # garage color
    s.place( ShelfUnit((bw, gl, bed_z), count=0, with_back=True, color=gc, desc="right garage"), rel_to='BR')
    s.place( ShelfUnit((sw-bw, gl, bed_z), count=2, with_back=True, color=gc, desc="left garage"), rel_to='BL')

    # --- kitchen/cooking area ---
    kw = sl - bl - s.door_w - s.door_off
    kh = s.vnose_h
    kc = (216, 230, 92)
    k_off = bl
    s.place( ShelfUnit((kw, bw, kh), count=1, color=kc, desc="kitchen unit"),
            rel_to='BR', rotation='R', offset=[0,k_off,0])
    s.place( ShelfUnit((bw, 4, sh-kh), count=3, color=kc, with_back=True, desc="spice rack"),
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
    s.place( ShelfUnit((long_shelf_w, shelf_depth, sh), count=3, desc="long side shelf"),
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
    s.place( ShelfUnit((gl, shelf_depth, ssh), count=3, desc="sideway back shelf"),
            rel_to='BL', rotation='L', offset=[0,0,bed_z])
    s.place( ShelfUnit((s_opt_w, shelf_depth, ssh), count=3, color=s_opt_c, desc="opt back shelf"),
            rel_to='BL', offset=[shelf_depth,0,bed_z])

    self.place(s)
    return None

