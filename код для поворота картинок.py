from PIL import Image, ImageOps
import sys

try:
    im = Image.open('tile_1.bmp')
except IOError:
    print('error')
    sys.exit(1)

# rot90 = im.rotate(90)
# rot180 = im.rotate(180)
# rot270 = im.rotate(270)
# rot90.save('tile_10_rot90.bmp')
# rot180.save('tile_10_rot180.bmp')
# rot270.save('tile_10_rot270.bmp')
mirrored = ImageOps.flip(im)
mirrored.save('?.bmp')
