print """<?xml version="1.0" ?>"""
width = 6
height = 7

print """<resource>
<imageatlas size="32x32" file="tiles.png">
"""

k = 0
for i in range(height):
    for j in range(width):
        print """<image id="%d" offset="%d,%d" />""" % (k, j*32, i*32)
        k += 1

print """</imageatlas>"""


tile_names = ["blank1", "mud_bl", "mud_b", "mud_br", "blank2", "blank3",
              "blank4", "mud_l", "mud_c", "mud_r", "mud_convex_bl", "mud_convex_br",
              "grass_1", "mud_tl", "mud_t", "mud_tr", "mud_convex_tl", "mud_convex_tr",
              "stones", "grass_2", "flowers", "mud_1", "wall_end_br", "wall_end_tr",
              "mud_1", "wall_bl", "wall_b", "wall_br", "wall_end_bl", "wall_end_tl",
              "buttercup", "wall_l", "grass_2", "wall_r", "wall_end_rb", "wall_end_lb",
              "daisy", "wall_tl", "wall_t", "wall_tr", "wall_end_rt", "wall_end_lt"]

print """<tileset>"""
k = 0
for i in range(height):
    for j in range(width):
      print """<tile id="%s"><image ref="%d"/></tile>""" % (tile_names[k], k) 
      k += 1
print """</tileset>"""
print """</resource>"""


