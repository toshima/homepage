"""
Convert an image to a compressed string so that it can be pasted into index.html.
"""

import json
import numpy as np
from PIL import Image
import sys


# We take every `stride_x` pixel horizontally and every `stride_y` pixel vertically
stride_x = 18
stride_y = 20


def main():
    if len(sys.argv) != 2:
        print("Usage: ./compress_image.py <image_file>")
        sys.exit(1)

    path = sys.argv[1]
    image = np.array(Image.open(path))

    # Convert to hex and sub-sample
    image = np.apply_along_axis(lambda rgb: f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}", 2, image)
    image = image[::stride_y, ::stride_x]

    # Get unique colors
    colors = list(sorted(set(x for row in image for x in row)))
    mapping = {c: i for i, c in enumerate(colors)}

    # Print compressed version
    print(json.dumps({
        "columns": len(image[0]),
        "colors": colors,
        "image": "".join(chr(mapping[x]) for row in image for x in row),
    }))


if __name__ == "__main__":
    main()
