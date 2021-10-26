from io import BytesIO
from os import listdir
from os.path import join, isfile
from queue import Queue
from threading import Thread
from time import time

from PIL import Image

from rembg.bg import remove

# TODO: only process if no result

IMAGES_DIR = join('..', 'imgs')

INPUT_DIR = join(IMAGES_DIR, '00.Original')
OUTPUT_DIR = join(IMAGES_DIR, '01.Background')

input_files = sorted([f for f in listdir(INPUT_DIR) if f.lower().startswith("mumi") and f.lower().endswith("jpg")])

jobs = Queue()

for in_f in input_files:
    out_f = in_f.replace(".jpg", ".png").replace(".JPG", ".png")
    jobs.put((join(INPUT_DIR, in_f), join(OUTPUT_DIR, out_f)))


def image_to_byte_array(img):
    img_byte_arr = BytesIO()
    img.save(img_byte_arr, format="PNG")
    return img_byte_arr.getvalue()


def remove_background(img_in, MAX_DIM = 1024):
    width, height = img_in.size
    nWidth, nHeight = img_in.size

    if width >= height and width > MAX_DIM:
        nWidth = MAX_DIM
        nHeight = (MAX_DIM / width) * height
    elif height > width and height > MAX_DIM:
        nHeight = MAX_DIM
        nWidth = (MAX_DIM / height) * width

    img_in.thumbnail((nWidth, nHeight), Image.ANTIALIAS)

    result = remove(image_to_byte_array(img_in))
    img_out = Image.open(BytesIO(result)).convert("RGBA")

    return img_out


def run_remove_background(q):
    while not q.empty():
        print("items left: %i" % jobs.qsize())
        in_file_path, out_file_path = q.get()

        if not isfile(out_file_path):
            img_in = Image.open(in_file_path).convert("RGBA")
            img_no_bgnd = remove_background(img_in)
            img_no_bgnd.save(out_file_path)

        q.task_done()


NUM_THREADS = 8

start_s = time()

for i in range(NUM_THREADS):
    worker = Thread(target=run_remove_background, args=(jobs,))
    worker.start()

jobs.join()

print("total time: %i seconds" % (time() - start_s))
