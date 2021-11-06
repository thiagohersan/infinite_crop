import cv2
import numpy as np

from os import listdir
from os.path import join, isfile
from queue import Queue
from threading import Thread, Lock
from time import time
import json
from colorsys import rgb_to_hls


IMAGES_DIR = join('..', 'imgs')

INPUT_DIR = join(IMAGES_DIR, '04.Sized')
OUTPUT_DIR = join(IMAGES_DIR, '05.Analyzed')
OUTPUT_FILENAME = 'MUMI-analysis.json'

CV_KMEANS_CRITERIA = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)
CV_KMEANS_K = 8

input_files = sorted([f for f in listdir(INPUT_DIR) if f.lower().startswith("mumi") and f.lower().endswith(".jpg")])
output_file = join(OUTPUT_DIR, OUTPUT_FILENAME)


analysis = {}
aLock = Lock()
if isfile(output_file):
    with open(output_file) as json_file:
        analysis = json.load(json_file)
else:
    open(output_file, 'a').close()

jobs = Queue()

for in_f in input_files:
    jobs.put((join(INPUT_DIR, in_f), in_f.replace('.jpg', '')))


def calculate_dominant_color(file_path):
    image = cv2.imread(file_path)
    image = cv2.resize(image, (0,0), fx=0.25, fy=0.25)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    pixel_values = np.float32(image.reshape((-1, 3)))
    _, labels, centers = cv2.kmeans(pixel_values, CV_KMEANS_K, None, CV_KMEANS_CRITERIA, 10, cv2.KMEANS_RANDOM_CENTERS)
    centers = np.uint8(centers)
    _, counts = np.unique(labels, return_counts=True)
    dominant_rgb = centers[np.argmax(counts)]
    dominant_hls = rgb_to_hls(*(dominant_rgb / [255, 255, 255]))
    return { 'rgb': [x.item() for x in dominant_rgb], 'hls': list(dominant_hls) }

def run_dominant(q):
    while not q.empty():
        print("items left: %i" % jobs.qsize())
        in_file_path, image_name = q.get()

        if image_name not in analysis:
            aLock.acquire()
            analysis[image_name] = calculate_dominant_color(in_file_path)
            aLock.release()

        q.task_done()


NUM_THREADS = 8

start_s = time()

for i in range(NUM_THREADS):
    worker = Thread(target=run_dominant, args=(jobs,))
    worker.start()

jobs.join()

with open(output_file, 'w') as json_file:
    json_file.write(json.dumps(analysis))
    
print("total time: %i seconds" % (time() - start_s))
