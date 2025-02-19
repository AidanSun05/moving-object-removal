from os import listdir
from pathlib import Path
import cv2
import numpy as np
import sys

if len(sys.argv) < 2:
    print("Enter a directory of images")
    sys.exit(1)

in_dir = Path(sys.argv[1])
files = [in_dir.joinpath(i) for i in listdir(in_dir)]
images = [cv2.imread(file) for file in files if file.suffix == ".jpg"]

images_arr = np.array(images)
images_median = np.median(images_arr, axis=0).astype(np.uint8)

print(f"Input images: {images_arr.shape[0]}")
print(f"Output image shape: {images_median.shape}")
cv2.imwrite("output.jpg", images_median)
