#!/usr/bin/env python

from solid import *
from solid.utils import *  # Not required, but the utils module is useful

from side_bed_layout import SideBedLayout
from rear_bed_layout import RearBedLayout

def render():
  t0 = SideBedLayout()
  t1 = RearBedLayout()
  return union()(t1.render_all(), right(200)(t0.render_all()))
