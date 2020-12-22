from solid import *
from solid.utils import *  # Not required, but the utils module is useful
from lib.item import Item


class Battery(Item):
  def __init__(self, dim):
    super().__init__(dim)
    self.color = (64,64,64)
    self.top_color = (62,93,220)
    self.pos_color = (160,0,0)
    self.neg_color = (0,160,0)
  
  def render(s):
    (w,l,h) = s.getDim()

    ps = 2 # post area size x/y
    th = 1.5 # top height
    top_poly = polygon([(0,ps), (0,l), (w,l), (w,ps), (w-ps,ps), (w-ps,0), (ps,0), (ps,ps)])
    top = s.c(s.top_color, up(h-th)(linear_extrude(height=th)(top_poly)))

    body = s.c(s.color, cube([w,l,h-th]))

    post = cylinder(r=0.3*ps, h=th, segments=10)
    posts = union()(
      s.c(s.pos_color, translate([ps/2,ps/2,h-th])(post)),
      s.c(s.neg_color, translate([w-ps/2,ps/2,h-th])(post)),
    )
    return union()(body, top, posts)

class Battleborn100ah(Battery):
  def __init__(self):
    super().__init__([12.8,6.9,9])

  def desc(s):
    return "Battleborn 100AH Battery"
