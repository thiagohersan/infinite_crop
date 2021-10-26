from os import listdir
from os.path import join, isfile
from queue import Queue
from subprocess import Popen
from threading import Thread
from time import time

IMAGES_DIR = join("..", "imgs")

INPUT_DIR = join(IMAGES_DIR, "01.Background")
OUTPUT_DIR = join(IMAGES_DIR, "02.Crop")
OUTPUT_BAD_DIR = join(IMAGES_DIR, "02.Crop", "_x")

P5_SKETCH_PATH = "/Users/kny/Documents/isThisArt/2021-09__ComCiencia/dev/infinite.Crop-Images/p5/RemoveTransparent"

input_files = sorted([f for f in listdir(INPUT_DIR) if f.startswith("MUMI") and f.endswith("png")])

jobs = Queue()

for in_filename in input_files:
    image_name = in_filename.replace(".png", "")
    out_filename = in_filename.replace(".png", ".jpg")
    jobs.put((image_name, out_filename))

def run_crop(q):
    while not q.empty():
        print("items left: %i" % jobs.qsize())
        image_name, out_filename = q.get()
        if not (isfile(join(OUTPUT_DIR, out_filename)) or isfile(join(OUTPUT_BAD_DIR, out_filename))):
            p = Popen(["processing-java", "--sketch=%s" % P5_SKETCH_PATH, "--run", "%s" % image_name])
            try:
                p.wait(timeout=60)
            except:
                print("%s timedout" % image_name)
        q.task_done()


NUM_THREADS = 8

start_s = time()

for i in range(NUM_THREADS):
    worker = Thread(target=run_crop, args=(jobs,))
    worker.start()

jobs.join()

print("total time: %i seconds" % (time() - start_s))
