from gimpfu import pdb

for i in range(5):
    filename = "%s.xcf" % i
    image = pdb.gimp_file_load(filename, filename)
    pdb.gimp_image_rotate(image, 0)
    pdb.gimp_image_scale(image, 104, 68)
    outfilename = "../../dog/%s.png" % i
    layer = pdb.gimp_image_merge_visible_layers(image, 1)
    pdb.gimp_file_save(image, layer, outfilename, outfilename)
