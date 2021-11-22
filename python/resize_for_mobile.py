from io import BytesIO
from os import listdir
from os.path import join, isfile
from queue import Queue
from threading import Thread, Lock
from time import time
from math import floor, ceil, log2

from PIL import Image
from PIL.ImageOps import mirror

IMAGES_DIR = join('..', '..', '..', 'www', 'infinite-resources', 'assets', 'textures')

INPUT_DIR = join(IMAGES_DIR, '1920')
OUTPUT_DIR = join(IMAGES_DIR, '1024')

input_files = sorted([f for f in listdir(INPUT_DIR) if f.lower().startswith("mumi") and f.lower().endswith(".jpg")])

jobs = Queue()

for in_f in input_files:
    jobs.put((join(INPUT_DIR, in_f), join(OUTPUT_DIR, in_f)))


def resize(img_in, new_height):
    new_width = ceil(3 * new_height)
    img_in.thumbnail((new_width, new_height), Image.ANTIALIAS)

    crop_width = 2**floor(log2(new_width))
    crop_left = floor((new_width - crop_width) / 2)
    img_in = img_in.crop((crop_left, 0, crop_left + crop_width, new_height))

    return img_in

NEW_IMG_HEIGHT = 342
def run_resize(q):
    while not q.empty():
        print("items left: %i" % jobs.qsize())
        in_file_path, out_file_path = q.get()

        if not isfile(out_file_path):
            img_in = Image.open(in_file_path).convert("RGB")
            img_sized = resize(img_in, NEW_IMG_HEIGHT)
            img_sized.save(out_file_path, quality=70, optimize=True, progressive=True)

        q.task_done()


NUM_THREADS = 8

start_s = time()

for i in range(NUM_THREADS):
    worker = Thread(target=run_resize, args=(jobs,))
    worker.start()

jobs.join()

print("total time: %i seconds" % (time() - start_s))
