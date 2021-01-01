
from solid import *
from solid.utils import *  # Not required, but the utils module is useful
from lib.item import Item
from lib.rail8020 import Rail1010
from lib.wood import Panel_1_8, Ply_1_2, Lumber_1_2

class ShelfUnitPly(Item):
  def __init__(self, dim, count=3, with_back=False, color=(144, 190, 109), woodFactory=Ply_1_2, desc=""):
    super().__init__(dim)
    self.color = color
    self.count = count
    self.with_back = with_back
    self.woodFactory = woodFactory
    self.user_desc = desc

  def desc(s):
    u = ", " + s.user_desc  if s.user_desc else ""
    return "Wood Shelf Unit (ply){0}: {1}".format(u, s.dimStr3D())

  def render(s):
    (w,l,h) = s.getDim()
    sz = s.woodFactory.SIZE

    if s.with_back:
      l = l - sz # make room for the back vertical cover
      b = s.woodFactory(h,w, color=s.color)
      s.place(b, rel_to='FL', rotation='VR')

    sep = (h-sz) / (s.count+1.0)
    shelf = s.woodFactory(w-2*sz,l, color=s.color)
    for i in range(s.count+2):
      s.place(shelf, offset=[sz,0,i*sep])

    v_shelf = s.woodFactory(h,l, color=s.color)
    s.place(v_shelf, rotation='V')
    s.place(v_shelf, rotation='V', rel_to='BR')
    return None

class ShelfUnitLumber(Item):
  def __init__(self, dim, count=3, color=(144, 190, 109), plyFactory=Ply_1_2, lumberFactory=Lumber_1_2, desc=""):
    super().__init__(dim)
    self.color = color
    self.count = count
    self.plyFactory = plyFactory
    self.lumberFactory = lumberFactory
    self.user_desc = desc

  def desc(s):
    u = ", " + s.user_desc  if s.user_desc else ""
    return "Wood Shelf Unit (lum){0}: {1}".format(u, s.dimStr3D())

  def render(s):
    (w,l,h) = s.getDim()
    ply_sz = s.plyFactory.SIZE
    lum_sz = s.lumberFactory.SIZE

    # -- legs
    leg_h = h-ply_sz
    leg = s.lumberFactory(leg_h)
    s.place(leg, rotation='VR', rel_to='BL')
    s.place(leg, rotation='VR', rel_to='BR')
    s.place(leg, rotation='VR', rel_to='FL')
    s.place(leg, rotation='VR', rel_to='FR')

    # -- mid shelfs
    sep = (leg_h) / (s.count+1.0)
    shelf = s.plyFactory(w-2*lum_sz[1],l, color=s.color)
    hor_rail = s.lumberFactory(w-2*lum_sz[1])
    dep_rail = s.lumberFactory(l-2*lum_sz[0])
    for i in range(s.count):
      sbh = (i+1)*sep # shelf bottom height
      s.place(shelf, offset=[lum_sz[1],0,sbh])
      s.place(hor_rail, rotation='B', rel_to='BL', offset=[lum_sz[1],0,sbh-lum_sz[1]])
      s.place(hor_rail, rotation='B', rel_to='FL', offset=[lum_sz[1],0,sbh-lum_sz[1]])
      s.place(dep_rail, rotation='L', rel_to='BL', offset=[0,lum_sz[0],sbh-lum_sz[0]+ply_sz])
      s.place(dep_rail, rotation='L', rel_to='BR', offset=[0,lum_sz[0],sbh-lum_sz[0]+ply_sz])

    # -- top shelf
    top_shelf = s.plyFactory(w,l, color=s.color)
    s.place(top_shelf, rel_to='TBL')
    s.place(hor_rail, rotation='B', rel_to='TBL', offset=[lum_sz[1],0,-ply_sz])
    s.place(hor_rail, rotation='B', rel_to='TFL', offset=[lum_sz[1],0,-ply_sz])
    s.place(dep_rail, rotation='L', rel_to='TBL', offset=[0,lum_sz[0],-ply_sz])
    s.place(dep_rail, rotation='L', rel_to='TBR', offset=[0,lum_sz[0],-ply_sz])

    return None

class Shelf8020(Item):
  """single shelf (not unit). assumes 8020 frame is already there"""
  def __init__(self, w, l, railFactory=Rail1010, woodFactory=Panel_1_8, numSupports=1):
    super().__init__([w, l, railFactory.SIZE])
    self.railFactory = railFactory
    self.woodFactory = woodFactory
    self.numSupports = numSupports

  def desc(s):
    return "{0} Shelf(s): {1}".format(s.railFactory.__name__, s.dimStr2D())

  def render(s):
    (w,l,h) = s.getDim()
    sz = s.railFactory.SIZE

    h_rail = s.railFactory(w - 2*sz)
    s.place(h_rail, offset=[sz,0,0])
    s.place(h_rail, offset=[sz,0,0], rel_to='FL')

    d_rail = s.railFactory(l - 2*sz)
    off = (w-sz) / (s.numSupports+1)
    for i in range(s.numSupports+2):
      s.place(d_rail, rotation='L', offset=[i * off,sz,0])

    if s.woodFactory:
      sheet = s.woodFactory(w - 2*sz, l)
      s.place(sheet, offset=[sz,0,sz])

    return None

class ShelfUnit8020(Item):
  def __init__(self, dim, count=3, railFactory=Rail1010, woodFactory=Panel_1_8,
               has_bottom_shelf=False, has_top_shelf=False,
               skip=0, numSupports=1, desc=""):
    super().__init__(dim)
    self.count = count
    self.railFactory = railFactory
    self.woodFactory = woodFactory
    self.has_bottom_shelf = has_bottom_shelf
    self.has_top_shelf = has_top_shelf
    self.numSupports = numSupports
    self.user_desc = desc
    self.skip = skip

  def desc(s):
    u = ", " + s.user_desc  if s.user_desc else ""
    return "{0} Shelf Unit{1}: {2}".format(s.railFactory.__name__, u, s.dimStr3D())

  def render(s):
    (w,l,h) = s.getDim()
    sz = s.railFactory.SIZE

    if s.has_top_shelf:
      s.place(s.woodFactory(w,l), rel_to='TBL')
      h -= s.woodFactory.SIZE

    # vertical rails
    vrail = s.railFactory(h - 2*sz)
    s.place(vrail, rel_to='FL', rotation='V', offset=[0,0,sz])
    s.place(vrail, rel_to='BL', rotation='V', offset=[0,0,sz])
    s.place(vrail, rel_to='FR', rotation='V', offset=[0,0,sz])
    s.place(vrail, rel_to='BR', rotation='V', offset=[0,0,sz])

    # horizontal rails along width
    rw = s.railFactory(w)
    s.place(rw, rel_to='FL')
    s.place(rw, rel_to='BL')
    s.place(rw, rel_to='FL', offset=[0,0,h-sz])
    s.place(rw, rel_to='BL', offset=[0,0,h-sz])

    # horizontal rails along depth
    rd = s.railFactory(l - 2*sz)
    s.place(rd, rel_to='BL', rotation='L', offset=[0,sz,0])
    s.place(rd, rel_to='BR', rotation='L', offset=[0,sz,0])
    s.place(rd, rel_to='BL', rotation='L', offset=[0,sz,h-sz])
    s.place(rd, rel_to='BR', rotation='L', offset=[0,sz,h-sz])

    # shelves
    vsep = (h-sz) / (s.count+1)
    shelf = Shelf8020(w,l, railFactory=s.railFactory, woodFactory=s.woodFactory, numSupports=s.numSupports)
    for i in range(s.skip, s.count):
      s.place(shelf, offset=[0,0,(i+1)*vsep])

    if s.has_bottom_shelf:
      bsw = s.woodFactory(w-2*sz, l)
      s.place(bsw, offset=[sz,0,sz])

    return None