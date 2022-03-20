#!/usr/bin/env python

from solid import *
from solid.utils import *

from lib.wood import Lumber_1_2, Lumber_1_3, Lumber_2_4, Lumber_2_8
from lib.shelf import ShelfUnit8020, ShelfUnitLumber, ShelfUnitPly

shelfDims = [55,24.5,43]

def render():
  s1 = ShelfUnitLumber(shelfDims, count=1, lumberFactory=Lumber_1_2).render_all()
  s2 = ShelfUnit8020(shelfDims, count=1, has_top_shelf=True).render_all()
  # s3 = ShelfUnitPly(shelfDims, count=1, with_back=True).render_all()

  a = union()(
    s1,
    right(100)(s2),
    # forward(50)(s3)
  )

  return a

