"""
This module contains functions used to process the images that are taken for detection of the reflective tags.
"""

import numpy as np


def getblockmaxedimage(img, blocksize, offset):
    """
    This is a fast approximate dilation method (could probably replace with
    a true dilation now the pi5 is being used).

    Effectively replaces each pixel with approximately the maximum of all the
    pixels within offset*blocksize of the pixel (in a square).

    Get a new image of the same size, but filtered such that each square patch
    of blocksize has its maximum calculated, then a search box of size
    (1+offset*2)*blocksize centred on each pixel is applied which finds the
    maximum of these patches.

    img = image to apply the filter to
    blocksize = size of the squares
    offset = how far from the pixel to look for maximum
    """

    k = int(img.shape[0] / blocksize)
    l = int(img.shape[1] / blocksize)
    if blocksize == 1:
        maxes = img
    else:
        maxes = img[:k * blocksize, :l * blocksize].reshape(k, blocksize, l, blocksize).max(
            axis=(-1, -3))  # from https://stackoverflow.com/questions/18645013/windowed-maximum-in-numpy

    xm, ym = maxes.shape
    i = 0
    for xoff in range(-offset + 1, offset, 1):  # (if offset=1, for xoff in [0]) (if offset=2, for xoff in [-1,0,1])...
        for yoff in range(-offset + 1, offset, 1):
            if i == 0:
                max_img = maxes[xoff + offset:xoff + xm - offset, yoff + offset:yoff + ym - offset]
            else:
                max_img = np.maximum(max_img, maxes[xoff + offset:xoff + xm - offset, yoff + offset:yoff + ym - offset])
            i += 1

    out_img = np.full_like(img, 0)
    inner_img = max_img.repeat(blocksize, axis=0).repeat(blocksize, axis=1)
    out_img[blocksize * offset:(blocksize * offset + inner_img.shape[0]),
    blocksize * offset:(blocksize * offset + inner_img.shape[1])] = inner_img

    return out_img
