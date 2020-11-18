#!/usr/bin/env python

from solid import *
from solid.utils import *  # Not required, but the utils module is useful
import math as M

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

T_WIDTH = 6 * 12
T_LENGTH = 12 * 12
T_HEIGHT = 6 * 12
T_COLOR = colors[6]
T_DOOR_W = 30
T_DOOR_OFF = 6
VNOSE_HEIGHT = 42
VNOSE_DEPTH = 2 * 12

GARAGE_L = 36
BED_SHELF_L = 28
BED_WIDTH_S = 24
BED_WIDTH_M = 30
BED_WIDTH_L = 36
BED_LENGTH = 6 * 12
BED_HEIGHT = 7 # 1 inch ply + 6" mattress
BED_Z = T_HEIGHT - 38 - BED_HEIGHT # 38" sitting clearance max bed Z
BED_COLOR = colors[5]

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
CHAIR_C = colors[2]

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

SHELF_COLOR = colors[4]
SHELF_COUNT = 3

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

def shell_frame(size_v):
  (w,h) = size_v
  ft = 0.1 # frame thickness
  fw = 2   # frame edge width
  frame = cube([w, ft, h]) - \
    translate([fw,-ft,fw])(cube([w-2*fw, 3*ft, h-2*fw]))
  return frame

def shell():
  nose_d = VNOSE_DEPTH
  nose_s_w = T_WIDTH / 4.0 # width of angled segment 
  nose_s_l = M.sqrt(nose_d*nose_d + nose_s_w*nose_s_w) # length of nose angled segment
  nose_s_a = M.atan2(nose_d, nose_s_w) * 180 / M.pi
  nose_poly = polygon([(0,0), (nose_s_w,nose_d), (T_WIDTH-nose_s_w,nose_d), (T_WIDTH,0)])

  pf = square([T_WIDTH,T_LENGTH]) + forward(T_LENGTH)(nose_poly)
  floor = linear_extrude(height=0.001)(pf)

  nose_shelf = translate([0,T_LENGTH,VNOSE_HEIGHT])(linear_extrude(height=1)(nose_poly))

  # --- vnose windows ---
  vw_w = nose_s_l-2
  vw_h = T_HEIGHT-VNOSE_HEIGHT-3
  vw1 = rotate(nose_s_a)(right(1)(shell_frame([vw_w,vw_h])))
  vw1 = translate([0,T_LENGTH,VNOSE_HEIGHT+2])(vw1)
  vw2 = rotate(180-nose_s_a)(right(1)(shell_frame([vw_w,vw_h])))
  vw2 = translate([T_WIDTH,T_LENGTH,VNOSE_HEIGHT+2])(vw2)
  vw3 = shell_frame([T_WIDTH-2*nose_s_w-2,vw_h])
  vw3 = translate([nose_s_w+1,T_LENGTH+nose_d,VNOSE_HEIGHT+2])(vw3)

  # --- door ---
  df = shell_frame([T_DOOR_W, T_HEIGHT])
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

def bed(size_v):
  (w,l,h) = size_v
  b = union()(
    cube([w,l,1]),
    translate([1,1,1])(cube([w-2,l-2,h-1]))
  )
  return norm_color(BED_COLOR)(b)

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


def fridge(size_v):
  return color(Cyan)(cube(size_v))

def toilet():
  pass

def victron():
  pass

def water():
  pass

def chair(size_v, leg_h=CHAIR_LEG_H, color=CHAIR_C):
  (w,l,h) = size_v

  # legs = union()(
  #   translate([2,2,0])(cylinder(r=2,h=leg_h)),
  #   translate([w-2,2,0])(cylinder(r=2,h=leg_h)),
  #   translate([2,l-2,0])(cylinder(r=2,h=leg_h)),
  #   translate([w-2,l-2,0])(cylinder(r=2,h=leg_h)),
  # )
  seat = shelf([w,l,leg_h], num_shelfs=0)
  back = up(leg_h)(cube([w,2,h-leg_h]))

  return norm_color(color)(union()(seat, back))

# ----- MAIN -------

bw = BED_WIDTH_M
bl = BED_LENGTH
k_len = T_LENGTH-bl-T_DOOR_W-T_DOOR_OFF
k_h = VNOSE_HEIGHT
bed_shelf_h = T_HEIGHT - BED_Z - BED_HEIGHT - 12 # allow for clearance above mattress
long_shelf_l = T_LENGTH - GARAGE_L - CHAIR_W

trailer = union()(
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
  place('BR', shelf, (k_len, bw, k_h), 'R', [0,bl,0], num_shelfs=1), # kitchen shelf
  place('BR', shelf, (bw, 4, T_HEIGHT-k_h), 180, [0,bl,k_h], with_back=True, num_shelfs=3), # kitchen sep

  place('BL', shelf, (T_WIDTH-bw-18, 18, T_HEIGHT-BED_Z), 180, [18,0,BED_Z], num_shelfs=2, color=OPT_COLOR), # tiny on back (opt)
  place('BL', shelf, (GARAGE_L, 18, T_HEIGHT-BED_Z), 'L', [0,0,BED_Z], num_shelfs=2), # short side shelf in back
  place('BR', shelf, (bw, BED_SHELF_L, bed_shelf_h), 180, [0,0,T_HEIGHT-bed_shelf_h], num_shelfs=1), # above bed
  place('BL', shelf, (long_shelf_l, 18, T_HEIGHT), 'L', [0,GARAGE_L,0], num_shelfs=5), # long side shelf

  # chair
  place('FL', chair, (CHAIR_W, CHAIR_L, CHAIR_H), 'R', [0,0,0]),

  # fridge
  place('FL', fridge, (FRIDGE_W,FRIDGE_L,FRIDGE_H), 'R', [0,-1,1]),

)

scad_render_to_file(trailer)
    

