#!/usr/bin/env python

from solid import *
from solid.utils import *  # Not required, but the utils module is useful

from side_bed_layout import SideBedLayout
from rear_bed_layout import RearBedLayout

# t0 = SideBedLayout()
# t1 = RearBedLayout()

# from lib.shelf import ShelfUnit8020
# su = ShelfUnit8020([60,20,30], count=2, numSupports=3)
# t = su.render_all()
from lib.wood import Lumber_2_4, Lumber_2_8
t1 = Lumber_2_8(24)
scad_render_to_file(t1.render_all())
# scad_render_to_file(union()(t.render_all(), right(200)(t0.render_all())))

t1.print_bom()


