#!/usr/bin/env python

from solid import *
from solid.utils import *  # Not required, but the utils module is useful

colors = [
    # (249, 65, 68),    #0
    (135, 65, 68),    #0
    (243, 114, 44),
    (248, 150, 30),
    (249, 199, 79),   #3
    (144, 190, 109),
    (67, 170, 139),
    (87, 117, 144),   #6
]

T_WIDTH = 6 * 12
T_LENGTH = 12 * 12
T_HEIGHT = 6 * 12
T_COLOR = colors[6]

BED_WIDTH_S = 24
BED_WIDTH_M = 30
BED_WIDTH_L = 36
BED_LENGTH = 6 * 12
BED_HEIGHT = 7 # 1 inch ply + 6" mattress
BED_Z = T_HEIGHT - 38 - BED_HEIGHT # 38" sitting clearance max bed Z
BED_COLOR = colors[5]

SHELF_COLOR = colors[4]
SHELF_COUNT = 3

def norm_color(cv):
  return color([cv[0]/255.0, cv[1]/255.0, cv[2]/255.0])

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

def shell():
  nose_h = 0.3 * T_WIDTH
  p = polygon([
    (0,0), (0,T_LENGTH), (T_WIDTH/2.0,T_LENGTH + nose_h), (T_WIDTH,T_LENGTH), (T_WIDTH,0)])
  floor = linear_extrude(height=0.001)(p)
  return norm_color(T_COLOR)(floor)

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
    s.add(cube([w,1,h])) # back cover
  return norm_color(color)(s)

def fridge():
  pass


def toilet():
  pass

def victron():
  pass

# ----- MAIN -------

bw = BED_WIDTH_M
trailer = union()(
  shell(),
  place('BR', bed, (bw, BED_LENGTH, BED_HEIGHT), '', [0,0,BED_Z]),
  place('BL', shelf, (T_WIDTH-bw, 18, T_HEIGHT), 180, [0,0,0], num_shelfs=10, with_back=True, color=colors[0]),
  place('BR', shelf, (bw, 36, BED_Z), 180, [0,0,0], num_shelfs=0, with_back=True, color=colors[0]),
  place('BL', shelf, (T_LENGTH-36, 18, T_HEIGHT), 'R', [0,36,0], num_shelfs=5),
)

scad_render_to_file(trailer)
    

