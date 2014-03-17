import os
import re

width = 630
height = 595
offset_x = 15
offset_y = 122

for filename in os.listdir("."):
    if re.match("band*", filename):
        image = pdb.file_png_load(filename, filename, run_mode = RUN_NONINTERACTIVE)
        if image.height == 822:
            image.crop(width, height, offset_x, offset_y)
            pdb.file_png_save_defaults(image, image.active_layer, filename, filename) 
        pdb.gimp_image_delete(image)

print "done"
pdb.gimp_quit(1)

