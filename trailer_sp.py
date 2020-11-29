#!/usr/bin/env python

from solid import *
from solid.utils import *  # Not required, but the utils module is useful
import math as M

from lib.bed import BedL, BedM, BedS
from lib.shell import SilverEagle, SilverStar
from lib.solar import SolarRenegy200w, SolarRenegy300w
from lib.fridge import FridgeIcecoGO20, FridgeIcecoVL35, FridgeAlpicoolT60
from lib.shelf import Shelf
from lib.battery import Battleborn100ah
from lib.toilet import DryFlushToilet
from lib.stove import Stove
from lib.chair import Chair


colors = [
    # (249, 65, 68),    #0
    (135, 65, 68, 128),    #0
    (243, 114, 44, 100),
    (248, 150, 30),
    (249, 199, 79),   #3
    (144, 190, 109),
    (67, 170, 139),
    (87, 117, 144),   #6
]

SHOW_ROOF = True
SHOW_FLOOR = True

# silver eagle 6x12
T_WIDTH = 6 * 12
T_LENGTH = 12 * 12
# silver start 79"x14'
# T_WIDTH = 79
# T_LENGTH = 14 * 12
T_HEIGHT = 6.25 * 12
T_COLOR = (87, 117, 144)
T_DOOR_W = 30
T_DOOR_OFF = 6
VNOSE_HEIGHT = 42
VNOSE_DEPTH = 2 * 12

BED_WIDTH_S = 24
BED_WIDTH_M = 30
BED_WIDTH_L = 36
BED_LENGTH = 6 * 12
BED_HEIGHT = 7 # 1 inch ply + 6" mattress
BED_Z = T_HEIGHT - 38 - BED_HEIGHT # 38" sitting clearance max bed Z
BED_COLOR = colors[5]

BED_SHELF_L = 28 # depth of shelf above bed
BED_SHELF_H = T_HEIGHT - BED_Z - BED_HEIGHT - 12 # allow for clearance above mattress

SHELF_COLOR = colors[4]
SHELF_COUNT = 3
SHELF_L = 18 # standard shelf depth

KITCHEN_H = VNOSE_HEIGHT
KITCHEN_W = 2.5 * 12
KITCHEN_L = SHELF_L
KITCHEN_C = (216, 224, 187)

# Renegy 300w
# SOLAR_W = 40
# SOLAR_L = 65
# Renegy 200w
SOLAR_W = 26
SOLAR_L = 64
SOLAR_H = 1.5
SOLAR_NUM = 4
SOLAR_C = colors[1]

# Battleborn 100ah/12v
BAT_L = 12.8
BAT_W = 6.9
BAT_H = 9
BAT_C = (243, 114, 44, 180)

CHAIR_W = 30
CHAIR_L = 20
CHAIR_H = 42
CHAIR_LEG_H = 18
CHAIR_C =     (248, 150, 30),


# dry flush toilet
TOILET_W = 16
TOILET_L = 20
TOILET_H = 18

# iceco VL35
FRIDGE_W = 27.2
FRIDGE_L = 15.2
FRIDGE_H = 15
# iceco GO20
# FRIDGE_W = 22.4
# FRIDGE_L = 12.6
# FRIDGE_H = 12.4
# Alpicool T60 (huge with freeze+fridge)
# FRIDGE_W = 28.5
# FRIDGE_L = 14.2
# FRIDGE_H = 21.6

# 6 litter jug
WATER_W = 14
WATER_L = 8
WATER_H = 21
# 5 litter jug 6 3/4” x 13 3/4” and 18”
# WATER_W = 13.75
# WATER_L = 6.75
# WATER_H = 18
WATER_C = (12, 148, 196) # blue water jug
# WATER_C = (103, 106, 96) # dark green

TABLE_W = 12
TABLE_L = 24
TABLE_H = 33
TABLE_C = colors[0]

GARAGE_L = 36 # standard garage length (depth)
GARAGE_COLOR = colors[3]
OPT_COLOR = colors[0]

def norm_color(cv):
  return color([c/255.0 for c in cv])

def swap(a,b):
  return (b,a)

def place(rel_to, obj_factory, size_v, rotation, offset, **kw):
  (x,y,z) = (0,0,0)
  (w,l,h) = size_v

  out = obj_factory(size_v, **kw)

  if rotation == 'L':
    out = translate([l,0,0])(rotate(90)(out))
    (w,l) = swap(w,l)
  if rotation == 'R':
    out = translate([0,w,0])(rotate(-90)(out))
    (w,l) = swap(w,l)
  if rotation == 180:
    out = translate([w,l,0])(rotate(180)(out))

  if rel_to == 'FL':
    out = translate([0,T_LENGTH-l,0])(out)
  if rel_to == 'FR':
    out = translate([T_WIDTH-w,T_LENGTH-l,0])(out)
  if rel_to == 'BR':
    out = translate([T_WIDTH-w,0,0])(out)
    
  if offset:
    out = translate(offset)(out)
  return out


def frame_cutout(size_v):
  (w,h) = size_v
  ft = 0.1 # frame thickness
  fw = 2   # frame edge width
  frame = cube([w, ft, h]) - \
    translate([fw,-ft,fw])(cube([w-2*fw, 3*ft, h-2*fw]))
  return frame


def shell():
  # --- vnose shelf ---
  nose_d = VNOSE_DEPTH
  nose_s_w = T_WIDTH / 4.0 # width of angled segment 
  nose_s_l = M.sqrt(nose_d*nose_d + nose_s_w*nose_s_w) # length of nose angled segment
  nose_s_a = M.atan2(nose_d, nose_s_w) * 180 / M.pi
  nose_poly = polygon([(0,0), (nose_s_w,nose_d), (T_WIDTH-nose_s_w,nose_d), (T_WIDTH,0)])
  sink_cutout = translate([T_WIDTH/2.0, nose_d/2.0, -1])(cylinder(r=6, h=3))
  
  nose_shelf = translate([0,T_LENGTH,VNOSE_HEIGHT])(linear_extrude(height=1)(nose_poly) - sink_cutout)

  # --- floor ---
  pf = square([T_WIDTH,T_LENGTH]) + forward(T_LENGTH)(nose_poly)
  floor = linear_extrude(height=0.001)(pf)

  # --- vnose windows ---
  vw_w = nose_s_l-2
  vw_h = T_HEIGHT-VNOSE_HEIGHT-3
  vw1 = rotate(nose_s_a)(right(1)(frame_cutout([vw_w,vw_h])))
  vw1 = translate([0,T_LENGTH,VNOSE_HEIGHT+2])(vw1)
  vw2 = rotate(180-nose_s_a)(right(1)(frame_cutout([vw_w,vw_h])))
  vw2 = translate([T_WIDTH,T_LENGTH,VNOSE_HEIGHT+2])(vw2)
  vw3 = frame_cutout([T_WIDTH-2*nose_s_w-2,vw_h])
  vw3 = translate([nose_s_w+1,T_LENGTH+nose_d,VNOSE_HEIGHT+2])(vw3)

  # --- door ---
  df = frame_cutout([T_DOOR_W, T_HEIGHT])
  door = translate([T_WIDTH, T_LENGTH - T_DOOR_OFF - T_DOOR_W, 0])(rotate(90)(df))

  s = union()(nose_shelf, door, vw1, vw2, vw3)
  if SHOW_FLOOR:
    s.add(floor)
  return norm_color(T_COLOR)(s)

def solar():
  # --- solar panels ---
  sd = SOLAR_W + 2.0 # each panel has 2 inch in between
  ss = union()
  if SHOW_ROOF:
    for i in range(SOLAR_NUM):
      ss.add(forward(i*sd)(cube([SOLAR_L,SOLAR_W,SOLAR_H])))
  center_x = (T_WIDTH - SOLAR_L)/2.0
  return translate([center_x, 0, T_HEIGHT])(norm_color(SOLAR_C)(ss))


def shelf(size_v, num_shelfs = SHELF_COUNT, with_back=False, color=SHELF_COLOR):
  (w,l,h) = size_v
  sep = (h-1.0) / (num_shelfs+1)
  s = union()
  for i in range(num_shelfs+2):
    s = s.add(translate([0,0,i*sep])(cube([w,l,1])))
  v_shelf = cube([1,l,h])
  s.add([v_shelf, translate([w-1,0,0])(v_shelf)])
  if with_back:
    s.add(translate([0,l-1,0])(cube([w,1,h])))
  return norm_color(color)(s)

def battery(size_v):
  (w,l,h) = size_v
  t_size = 2
  b_body = union()(
    cube([w,l,h-1]),
    translate([0.25,0.25,h-1])(cube([w-2,l-0.5,1])),
  )
  return union()(
    norm_color(BAT_C)(b_body),
    color(Red)(translate([w-0.75,0.75,h-1])(cylinder(r=0.5,h=1))),
    color(Black)(translate([w-0.75,l-0.75,h-1])(cylinder(r=0.5,h=1))),
  )

def chair(size_v, leg_h=CHAIR_LEG_H, color=CHAIR_C):
  (w,l,h) = size_v

  seat = shelf([w,l,leg_h], num_shelfs=0)
  cushion = translate([1,1,leg_h+1])(cube([w-2,l-2,2]))
  back = up(leg_h)(cube([w,2,h-leg_h]))

  return norm_color(color)(union()(seat, cushion, back))

def fridge(size_v):
  return color(Cyan)(cube(size_v))

def toilet(size_v, t=0):
  (w,l,h) = size_v
  r = w/2.0
  offset = t * l
  c = hull()(cylinder(r=r, h=h) + forward(l-r)(cylinder(r=r, h=h)))
  c -= up(h)(sphere(r=r-2))
  t = translate([r,r,0])(c)
  return color(Cyan)(t)

def victron():
  pass

def water(size_v):
  (w,l,h) = size_v
  h2o = cube([w,l,h]) - \
    translate([-1,-1,(h-3)])(cube([5,l+2,5])) - \
    translate([5,-1,h-3-1])(cube([w-6,l+2,3]))
  h2o += translate([2,l/2.0,h-3])((cylinder(r=1.5, h=3, segments=10)))
  return norm_color(WATER_C)(h2o)

def table(size_v):
  (w,l,h) = size_v
  t = up(h-1)(cube([w,l,1])) + \
    translate([1,1,0])(cylinder(r=1, h=h))
  return norm_color(TABLE_C)(t)

# ----- MAIN -------

# back length wise bed with lots of side shelf and chair
def trailer0(_time = 0.0):
  bw = BED_WIDTH_M
  bl = BED_LENGTH
  k_len = T_LENGTH-bl-T_DOOR_W-T_DOOR_OFF
  long_shelf_w = T_LENGTH - GARAGE_L - CHAIR_W
  toilet_offset = TOILET_L * _time

  return union()(
  shell(),
  solar(),

  # bed
  place('BR', bed, (bw, bl, BED_HEIGHT), None, [0,0,BED_Z]),

  # electronics (battery, solar charger, etc)
  place('BR', battery, (BAT_W, BAT_L, BAT_H), 'L', [0,bl-BAT_W,0]),
  place('BR', battery, (BAT_W, BAT_L, BAT_H), 'L', [-1.1 * BAT_L,bl-BAT_W,0]),

  # garage
  place('BR', shelf, (bw, GARAGE_L, BED_Z), None, [0,0,0], num_shelfs=0, with_back=True, color=GARAGE_COLOR), # under bed
  place('BL', shelf, (T_WIDTH-bw, GARAGE_L, BED_Z), None, [0,0,0], num_shelfs=2, with_back=True, color=GARAGE_COLOR),

  # kitchen/cooking area
  place('BR', shelf, (k_len, bw, KITCHEN_H), 'R', [0,bl,0], num_shelfs=1), # kitchen shelf
  place('BR', shelf, (bw, 4, T_HEIGHT-KITCHEN_H), 180, [0,bl,KITCHEN_H], with_back=True, num_shelfs=3), # kitchen sep

  place('BL', shelf, (T_WIDTH-bw-18, 18, T_HEIGHT-BED_Z), 180, [18,0,BED_Z], num_shelfs=2, color=OPT_COLOR), # tiny on back (opt)
  place('BL', shelf, (GARAGE_L, 18, T_HEIGHT-BED_Z), 'L', [0,0,BED_Z], num_shelfs=2), # short side shelf in back
  place('BR', shelf, (bw, BED_SHELF_L, BED_SHELF_H), 180, [0,0,T_HEIGHT-BED_SHELF_H], num_shelfs=1), # above bed
  place('BL', shelf, (long_shelf_w, SHELF_L, T_HEIGHT), 'L', [0,GARAGE_L,0], num_shelfs=5), # long side shelf

  # chair
  place('FL', chair, (CHAIR_W, CHAIR_L, CHAIR_H), 'R', [0,0,0]),

  # fridge
  place('FL', fridge, (FRIDGE_W,FRIDGE_L,FRIDGE_H), 'R', [0,-1,1]),

  # toilet
  place('BR', toilet, (TOILET_W,TOILET_L,TOILET_H), 'L', [-toilet_offset,GARAGE_L,0], t=_time),

  # water
  place('FR', water, (WATER_W, WATER_L, WATER_H), '', [-T_WIDTH/4.0,VNOSE_DEPTH,0]),
  place('FR', water, (WATER_W, WATER_L, WATER_H), '', [-T_WIDTH/4.0 - WATER_W - 2,VNOSE_DEPTH,0]),

  # table
  place('FL', table, (TABLE_W,TABLE_L,TABLE_H), 180, [CHAIR_L-TABLE_W+2,0,0]),
)

def trailer1(_time = 0.0):
  bw = BED_WIDTH_M
  bl = BED_LENGTH
  gl = bw # garage length (depth).  override to fit under bed

  BED_SHELF_H = T_HEIGHT - BED_Z - BED_HEIGHT - 12 # allow for clearance above mattress
  long_shelf_w = T_LENGTH - gl - CHAIR_W
  elect_box_h = TOILET_H + 2
  elect_box_w = T_LENGTH - T_DOOR_OFF - T_DOOR_W - KITCHEN_W - bw
  # obs = over battery shelf
  obs_w = elect_box_w
  obs_z = elect_box_h
  obs_h = T_HEIGHT - obs_z
  k_off = bw + obs_w
  toilet_offset = TOILET_L * _time

  return union()(
  shell(),
  solar(),

  # bed
  place('BL', bed, (bw, bl, BED_HEIGHT), 'L', [0,0,BED_Z]),

  # garage
  place('BR', shelf, (bw, gl, BED_Z), None, [0,0,0], num_shelfs=0, with_back=True, color=GARAGE_COLOR), # under bed
  place('BL', shelf, (T_WIDTH-bw, gl, BED_Z), None, [0,0,0], num_shelfs=2, with_back=True, color=GARAGE_COLOR),

  # kitchen/cooking area
  place('BR', shelf, (KITCHEN_W, KITCHEN_L, KITCHEN_H), 'R', [0,k_off,0], num_shelfs=1), # kitchen shelf
  place('BR', shelf, (KITCHEN_L, 4, T_HEIGHT-KITCHEN_H), 180, [0,k_off,KITCHEN_H], with_back=True, num_shelfs=3), # kitchen sep

  place('BR', shelf, (bw, SHELF_L, BED_SHELF_H), 'R', [0,0,T_HEIGHT-BED_SHELF_H], num_shelfs=1), # above bed
  place('BR', shelf, (obs_w, SHELF_L, obs_h), 'R', [0,bw,obs_z], num_shelfs=4), # above battery/toilet
  place('BL', shelf, (long_shelf_w, SHELF_L, T_HEIGHT), 'L', [0,gl,0], num_shelfs=5), # long side shelf

  # chair
  place('FL', chair, (CHAIR_W, CHAIR_L, CHAIR_H), 'R', [0,0,0]),

  # fridge
  place('FL', fridge, (FRIDGE_W,FRIDGE_L,FRIDGE_H), 'R', [0,-1,1]),

  # toilet
  place('BR', toilet, (TOILET_W,TOILET_L,TOILET_H), '', [-toilet_offset,gl,0], t=_time),

  # # electronics (battery, solar charger, etc)
  place('BR', battery, (BAT_W, BAT_L, BAT_H), '', [0,k_off-BAT_L,0]),
  place('BR', battery, (BAT_W, BAT_L, BAT_H), '', [-1.1 * BAT_W,k_off-BAT_L,0]),

  # water
  place('FR', water, (WATER_W, WATER_L, WATER_H), '', [-T_WIDTH/4.0,VNOSE_DEPTH,0]),
  place('FR', water, (WATER_W, WATER_L, WATER_H), '', [-T_WIDTH/4.0 - WATER_W - 2,VNOSE_DEPTH,0]),

  # table
  place('FL', table, (TABLE_W,TABLE_L,TABLE_H), 180, [CHAIR_L-TABLE_W+2,0,0]),
  )

def layout1():
  # --- Config ---
  s = SilverEagle()
  # s = SilverStar()
  bed = BedL(s.getW())
  fridge = FridgeIcecoVL35()
  solar = SolarRenegy200w()
  toilet = DryFlushToilet()
  bat = Battleborn100ah()
  kitchen_w = 2.5 * 12
  shelf_depth = 18 # depth of side shelfs

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
  s.place(bat, rel_to='BR', rotation='R', offset=[0,bat_y_off,0])
  s.place(bat, rel_to='BR', rotation='R', offset=[-bat.getL() - 1,bat_y_off,0])

  # --- chair ---
  s.place(Chair(), rel_to='FL', rotation='R')

  # --- fridge ---
  s.place(fridge, rel_to='FL', rotation='R', offset=[2,-1,1])

  # --- long side shelf ---
  # long_shelf_w = sl - gl - chair.getW()
  # place('BL', shelf, (long_shelf_w, SHELF_L, T_HEIGHT), 'L', [0,gl,0], num_shelfs=5), # long side shelf

  # --- render entire trailer ---
  return s.render_all()



  # # # electronics (battery, solar charger, etc)

  # # water
  # place('FR', water, (WATER_W, WATER_L, WATER_H), '', [-T_WIDTH/4.0,VNOSE_DEPTH,0]),
  # place('FR', water, (WATER_W, WATER_L, WATER_H), '', [-T_WIDTH/4.0 - WATER_W - 2,VNOSE_DEPTH,0]),

  # # table
  # place('FL', table, (TABLE_W,TABLE_L,TABLE_H), 180, [CHAIR_L-TABLE_W+2,0,0]),

# t0 = trailer0(_time=0)
# t1 = right(T_WIDTH * 2)(trailer1(_time=0))
# scad_render_to_file(union()(t0, t1))
# t = BedL().render()
# t = SilverStar().render_all()
t = layout1()
scad_render_to_file(union()(t))

# scad_render_animated_file(trailer0)
    

