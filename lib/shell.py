from solid import *
from solid.utils import *  # Not required, but the utils module is useful
import math as M

from lib.item import Item

T_COLOR = (87, 117, 144)
T_DOOR_W = 30
T_DOOR_OFF = 6
VNOSE_HEIGHT = 42
VNOSE_DEPTH = 2 * 12

class ShellBase(Item):
  def __init__(self, dim):
    super().__init__(dim)

  @staticmethod
  def frame_cutout(size_v):
    (w,h) = size_v
    ft = 0.1 # frame thickness
    fw = 2   # frame edge width
    frame = cube([w, ft, h]) - \
      translate([fw,-ft,fw])(cube([w-2*fw, 3*ft, h-2*fw]))
    return frame

  def render(s):
    (w,l,h) = s.getDim()

    # --- vnose shelf ---
    nose_d = VNOSE_DEPTH
    nose_s_w = w / 4.0 # width of angled segment 
    nose_s_l = M.sqrt(nose_d*nose_d + nose_s_w*nose_s_w) # length of nose angled segment
    nose_s_a = M.atan2(nose_d, nose_s_w) * 180 / M.pi
    nose_poly = polygon([(0,0), (nose_s_w,nose_d), (w-nose_s_w,nose_d), (w,0)])
    sink_cutout = translate([w/2.0, nose_d/2.0, -1])(cylinder(r=6, h=3))
    
    nose_shelf = translate([0,l,VNOSE_HEIGHT])(linear_extrude(height=1)(nose_poly) - sink_cutout)

    # --- floor ---
    pf = square([w,l]) + forward(l)(nose_poly)
    floor = linear_extrude(height=0.001)(pf)

    # --- vnose windows ---
    vw_w = nose_s_l-2
    vw_h = h-VNOSE_HEIGHT-3
    vw1 = rotate(nose_s_a)(right(1)(ShellBase.frame_cutout([vw_w,vw_h])))
    vw1 = translate([0,l,VNOSE_HEIGHT+2])(vw1)
    vw2 = rotate(180-nose_s_a)(right(1)(ShellBase.frame_cutout([vw_w,vw_h])))
    vw2 = translate([w,l,VNOSE_HEIGHT+2])(vw2)
    vw3 = ShellBase.frame_cutout([w-2*nose_s_w-2,vw_h])
    vw3 = translate([nose_s_w+1,l+nose_d,VNOSE_HEIGHT+2])(vw3)

    # --- door ---
    df = ShellBase.frame_cutout([T_DOOR_W, h])
    door = translate([w, l - T_DOOR_OFF - T_DOOR_W, 0])(rotate(90)(df))

    u = union()(nose_shelf, door, vw1, vw2, vw3, floor)
    return s.c(T_COLOR, u)

class SilverEagle(ShellBase):
  def __init__(self):
    super().__init__([6 * 12, 12 * 12, 6.25 * 12])

class SilverStar(ShellBase):
  def __init__(self):
    super().__init__([79, 12 * 14, 7 * 12])
