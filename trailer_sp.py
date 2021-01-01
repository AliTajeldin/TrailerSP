#!/usr/bin/env python

from solid import *
from solid.utils import *  # Not required, but the utils module is useful

from side_bed_layout import SideBedLayout
from rear_bed_layout import RearBedLayout

# t0 = SideBedLayout()
# t1 = RearBedLayout()

from lib.wood import Lumber_1_2, Lumber_1_3, Lumber_2_4, Lumber_2_8
from lib.shelf import ShelfUnit8020, ShelfUnitLumber, ShelfUnitPly
s1 = ShelfUnitLumber([60,16,45], count=1, lumberFactory=Lumber_1_2).render_all()
s2 = ShelfUnit8020([60,16,45], count=1, has_top_shelf=True).render_all()
s3 = ShelfUnitPly([60,16,45], count=1).render_all()

a = union()(
  s1,
  right(100)(s2),
  forward(50)(s3)
)
# t1 = Lumber_2_8(24)
scad_render_to_file(a)
# scad_render_to_file(t1.render_all())
# scad_render_to_file(union()(t.render_all(), right(200)(t0.render_all())))

# t1.print_bom()


