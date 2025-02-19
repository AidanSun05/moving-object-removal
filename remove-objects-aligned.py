from os import listdir
from pathlib import Path
import cv2
import numpy as np
import sys

# Maximum number of features to detect
num_features = 500

# Percent of top features to keep
retain_percent = 0.15


def align(img1, img2):
    # Use grayscale images for faster performance, more reliable results
    img1_gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    img2_gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    # Apply ORB feature detection algorithm
    orb = cv2.ORB_create(num_features)
    kp1, des1 = orb.detectAndCompute(img1_gray, None)
    kp2, des2 = orb.detectAndCompute(img2_gray, None)

    matcher = cv2.DescriptorMatcher_create(cv2.DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMING)
    matches = matcher.match(des1, des2, None)
    matches = sorted(matches, key=lambda x: x.distance)

    # Retain top matches
    num_matches_keep = int(len(matches) * retain_percent)
    matches = matches[:num_matches_keep]

    # Extract location of good matches
    points1 = np.empty((len(matches), 2), dtype=np.float32)
    points2 = np.empty((len(matches), 2), dtype=np.float32)

    for i, match in enumerate(matches):
        points1[i] = kp1[match.queryIdx].pt
        points2[i] = kp2[match.trainIdx].pt

    # Calculate homography matrix to warp image
    h, _ = cv2.findHomography(points2, points1, cv2.RANSAC)

    # Warp image with homography matrix to align detected features
    # Keep new dimensions the same as the template image
    # BORDER_REPLICATE is used to eliminate possible borders of black pixels
    height, width, _ = img1.shape
    new_dims = (width, height)
    return cv2.warpPerspective(img2, h, new_dims, borderMode=cv2.BORDER_REPLICATE)


if len(sys.argv) < 2:
    print("Enter a directory of images")
    sys.exit(1)

in_dir = Path(sys.argv[1])
files = [in_dir.joinpath(i) for i in listdir(in_dir)]
images = [cv2.imread(file) for file in files if file.suffix == ".jpg"]

# Align images, use image 1 as a template
for i in range(1, len(images)):
    print("Aligning image:", i + 1)
    images[i] = align(images[0], images[i])

images_arr = np.array(images)
images_median = np.median(images_arr, axis=0).astype(np.uint8)

print(f"Input images: {images_arr.shape[0]}")
print(f"Output image shape: {images_median.shape}")
cv2.imwrite("output.jpg", images_median)
