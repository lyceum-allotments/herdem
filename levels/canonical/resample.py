from gimpfu import pdb

filename = "tiles.xcf"
image = pdb.gimp_file_load(filename, filename)
pdb.gimp_image_scale(image, 32 * 7, 32 * 3)
outfilename = "../tiles.png"
layer = pdb.gimp_image_merge_visible_layers(image, 1)
pdb.gimp_file_save(image, layer, outfilename, outfilename)
