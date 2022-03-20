#!/usr/bin/env python

from solid import *

from trailer_sp import render as t_render
from heli_shelf import render as h_render
scad_render_to_file(h_render())
