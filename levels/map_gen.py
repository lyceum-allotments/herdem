width = 40
height = 25
print """<resource><requires file="tiles.xml" /> 
<rectmap id="map0" origin="0,0,0" tile_size="32x32">"""

for i in range(width):
    print """<column>"""
    for j in range(height):
        print """<cell tile="grass_1"/>"""
    print """</column>"""

print """</rectmap>"""
print """</resource>"""
