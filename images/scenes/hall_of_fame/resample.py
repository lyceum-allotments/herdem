from gimpfu import pdb

filename = "hall_of_fame_large.xcf"
image = pdb.gimp_file_load(filename, filename)
pdb.gimp_image_scale(image, 1280, 800)
outfilename = "hall_of_fame.png"
layer = pdb.gimp_image_merge_visible_layers(image, 1)
pdb.gimp_file_save(image, layer, outfilename, outfilename)
