# Moving Object Removal

This is a Python script to remove moving objects from a sequence of images using a median operation.

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
python remove-objects.py [DIR]
```

where `[DIR]` is a path to a directory containing the set of input files to process. **These must be `.jpg` files and have the same dimensions (such as 1920x1080).**

This creates an `output.jpg` file with the result of the operation.

**For best results:**

- When taking the images to process, the camera should be completely still. This allows nonmoving objects (the ones you want to keep) to stay in the same place across all images.
- The moving objects should have minimal overlap between images, allowing the median operation to count them as outliers rather than persistent objects.
