# Bee retro-reflection detector

Bee tracking tool to detect retro-reflectors in images.

This new version 2 is completely rewritten and assumes all the photos are flash photos.

This tool is part of the [Sheffield Machine Learning Tracking](SheffieldMLtracking) project.

# Installation

Create a [virtual environment](https://docs.python.org/3/library/venv.html), activate it, then install this package
using the [Python package manager](https://pip.pypa.io/en/stable/).

```bash
pip install retrodetect
```

# Usage

There are two ways to use this package, either by running it as a terminal command or
importing the functions to use in your code.

## Command line interface

One passes a path and the tool will recursively search through the subdirectories, finding all the images, sorting
them (within that folder) and applying the retrodetect algorithm.

Usage example:

```bash
photo_path="~/beephotos/2023-06-29/sessionA/setA/cam5/02D49670796/"
btretrodetect $photo_path --after 10:32:29 --before 10:33:29 --threshold -10
```

To view the command line options, use the `--help` flag:

```bash
retrodetect --help
```

This will display the usage reference:

```
Runs the retoreflector detection algorithm

positional arguments:
  imgpath               Path to images (it will recursively search for images in these paths)

options:
  -h, --help            show this help message and exit
  -a AFTER, --after AFTER
                        Only process images that were created after this time HH:MM:SS
  -b BEFORE, --before BEFORE
                        Only process images that were created before this time HH:MM:SS
  -r, --refreshcache    Whether to refresh the cache
  -t THRESHOLD, --threshold THRESHOLD
                        Threshold of score before adding to data
  -s SOURCENAME, --sourcename SOURCENAME
                        The name to give this source of labels (default:retrodetect)
```

## Software framework

The `detectcontact` function in this package analyzes a sequence of photos captured by a tracking system to detect
potential retroreflectors with the `detect` function capturing the differences (retro-reflectors) detected between the
flash and no flash images.
See examples for details.

```python
from retrodetect import detect, detectcontact

contact, found, searchimg = detectcontact(photo_list, n, delsize=100)

output = detect(flash, noflash, blocksize=20, offset=10, searchbox=20, step=4, searchblocksize=50, ensemblesizesqrt=3,
                dilate=True, margin=100)
```

## Contributing

Interested in contributing? Check out
the [contributing guidelines](https://github.com/SheffieldMLtracking/.github/blob/main/CONTRIBUTING.md).
Please note that this project is released with a Code of Conduct.
By contributing to this project, you agree to abide by its terms.

This code is based on the original codebase at [lionfish0/btretrodetect](https://github.com/lionfish0/btretrodetect)
written by Michael T. Smith.
