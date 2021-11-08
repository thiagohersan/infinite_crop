from os.path import join
from shutil import copy2
from time import time
import json


IMAGES_DIR = join('..', 'imgs')

INPUT_DIR = join(IMAGES_DIR, '04.Sized')
OUTPUT_DIR = join(IMAGES_DIR, '06.Ordered')

start_s = time()

for order in ['rgb', 'hls']:
    OUTPUT_DIR_ORDER = join(OUTPUT_DIR, 'by_%s' % order)
    input_file = join(OUTPUT_DIR, 'by_%s.json' % order)

    with open(input_file) as json_file:
        image_names = json.load(json_file)

    for idx, image_name in enumerate(image_names):
        image_index = ('0000000%i' % idx)[-4:]
        in_file = join(INPUT_DIR, '%s.jpg' % image_name)
        out_file = join(OUTPUT_DIR_ORDER, '%s_%s.jpg' % (image_index, image_name))
        copy2(in_file, out_file)


print("total time: %i seconds" % (time() - start_s))
