from io import BytesIO
from os import listdir
from os.path import join, isfile
from queue import Queue
from threading import Thread, Lock
from time import time

from PIL import Image
from PIL.ImageOps import mirror

IMAGES_DIR = join('..', 'imgs')

INPUT_DIR = join(IMAGES_DIR, '03.Selection')
OUTPUT_DIR = join(IMAGES_DIR, '04.Sized')

input_files = sorted([f for f in listdir(INPUT_DIR) if f.lower().startswith("mumi") and f.lower().endswith(".jpg")])

jobs = Queue()

for in_f in input_files:
    jobs.put((join(INPUT_DIR, in_f), join(OUTPUT_DIR, in_f)))


# >1920: 2953, >1280: 688, >1024: 130, other: 12
def resize_reorient(img_in, MIN_DIM):
    width, height = img_in.size

    if height > width:
        img_in = mirror(img_in).rotate(90, expand=True)
        width, height = height, width

    if width / height > 3:
        nWidth = 3 * height
        crop_left = (width - nWidth) / 2
        img_in = img_in.crop((crop_left, 0, crop_left + nWidth, height))

    img_in.thumbnail((MIN_DIM, MIN_DIM / 3), Image.ANTIALIAS)

    return img_in

MIN_DIM = 1920
def run_resize(q):
    while not q.empty():
        print("items left: %i" % jobs.qsize())
        in_file_path, out_file_path = q.get()

        if not isfile(out_file_path):
            img_in = Image.open(in_file_path).convert("RGB")
            width, height = img_in.size

            if max(width, height) > MIN_DIM and min(width, height) > MIN_DIM / 3:
                img_sized = resize_reorient(img_in, MIN_DIM)
                img_sized.save(out_file_path, quality=70, optimize=True, progressive=True)

        q.task_done()


NUM_THREADS = 8

start_s = time()

for i in range(NUM_THREADS):
    worker = Thread(target=run_resize, args=(jobs,))
    worker.start()

jobs.join()

print("total time: %i seconds" % (time() - start_s))
