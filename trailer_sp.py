#!/usr/bin/env python

from solid import *
from solid.utils import *  # Not required, but the utils module is useful

from side_bed_layout import side_back_bed_layout
from rear_bed_layout import rear_bed_layout

# t = side_back_bed_layout()
t = rear_bed_layout()

from lib.shelf import ShelfUnit8020
su = ShelfUnit8020([60,20,30], count=2, numSupports=3)
t = su.render_all()
scad_render_to_file(t)
    

