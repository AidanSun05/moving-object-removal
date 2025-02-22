# Moving Object Removal

This is a Python script to remove moving objects from a sequence of images using a median operation. There are 2 Python programs in this repository:

- `remove-objects.py` only removes moving objects.
- `remove-objects-aligned.py` first performs image alignment to account for small camera movements, then removes moving objects.

See [Example Usage](example.md) for sample input and output images.

## Setup

```shell
# Virtual environment
python -m venv venv
source venv/bin/activate

# Dependencies
pip install opencv-python numpy
```

## Usage

```shell
# Object removal only
python remove-objects.py [DIR]

# Object removal with image alignment
python remove-objects-aligned.py [DIR]
```

where `[DIR]` is a path to a directory containing the set of input files to process. **These must be `.jpg` files and have the same dimensions (such as 1920x1080).**

This creates an `output.jpg` file with the result of the operation.

**For best results:**

- When taking the images to process, the camera should be completely still. This allows nonmoving objects (the ones you want to keep) to stay in the same place across all images.
- The moving objects should have minimal overlap between images, allowing the median operation to count them as outliers rather than persistent objects.

## How it Works

The `np.median` function is used to take the median value of each red, green, and blue color channel for each pixel across all images.

- Pixels containing an undesired object only in a few images will be outliers, and computing the median will favor what's present in the rest of the images at that pixel.
- Pixels which are consistent throughout all images will remain unchanged.

This process only retains details that exist in all images, erasing moving or anomalous ones.

Image alignment is performed with an ORB feature detector (`cv2.ORB_create`). This feature detector uses the first available image as a template, and all later images will be adjusted to match it. The top feature matches are selected for a reliable alignment operation, which is outlined below:

- A homography matrix is calculated using the matching feature points in both images with `cv2.findHomography`.
- Warping of an image is performed with `cv2.warpPerspective`.
