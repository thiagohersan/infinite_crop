from os import listdir
from os.path import join, isfile
from queue import Queue
from subprocess import Popen
from threading import Thread
from time import time

IMAGES_DIR = join("..", "imgs")

INPUT_DIR = join(IMAGES_DIR, "01.Background")
OUTPUT_DIR = join(IMAGES_DIR, '02.Crop')

P5_SKETCH_PATH = "/Users/kny/Documents/isThisArt/2021-09__ComCiencia/dev/infinite.Crop-Images/p5/RemoveTransparent"

input_files = sorted([f for f in listdir(INPUT_DIR) if f.startswith("MUMI") and f.endswith("png")])

jobs = Queue()

for in_f in input_files:
    out_f = in_f.replace("png", "jpg")
    jobs.put((in_f.replace(".png", ""), join(OUTPUT_DIR, out_f)))

def run_crop(q):
    while not q.empty():
        print("items left: %i" % jobs.qsize())
        in_file_name, out_file_path = q.get()
        if not isfile(out_file_path):
            p = Popen(["processing-java", "--sketch=%s" % P5_SKETCH_PATH, "--run", "%s" % in_file_name])
            p.wait()
        q.task_done()


NUM_THREADS = 8

start_s = time()

for i in range(NUM_THREADS):
    worker = Thread(target=run_crop, args=(jobs,))
    worker.start()

jobs.join()

print("total time: %i seconds" % (time() - start_s))
