#!/usr/bin/env python

from solid import *

from trailer_sp import render as t_render
from heli_shelf import render as h_render
from living_room import render as l_render
scad_render_to_file(l_render())
