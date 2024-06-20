#!/usr/bin/env python

import argparse
import logging
import json
import os
import re
from glob import glob
import pickle

from retrodetect import Retrodetect

DESCRIPTION = """
Runs the retoreflector detection algorithm
"""
USAGE = """
TODO
"""

logger = logging.getLogger(__name__)


def get_args() -> argparse.Namespace:
    """
(    Command line arguments

    See: Argparse tutorial
    https://docs.python.org/3/howto/argparse.html
    """

    parser = argparse.ArgumentParser(description=DESCRIPTION, usage=USAGE)

    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('imgpath', type=str,
                        help='Path to images (it will recursively search for images in these paths)')
    parser.add_argument('-a', '--after', required=False, type=time_to_seconds, default=0,
                        help='Only process images that were created after this time HH:MM:SS')
    parser.add_argument('-b', '--before', required=False, type=time_to_seconds,
                        default=time_to_seconds('23:59:59'),
                        help='Only process images that were created before this time HH:MM:SS')
    parser.add_argument('-r', '--refreshcache', help='Whether to refresh the cache', action="store_true")
    parser.add_argument('-t', '--threshold', help='Threshold of score before adding to data',
                        type=str, default=0)
    parser.add_argument('-s', '--sourcename', type=str, default='retrodetect',
                        help='The name to give this source of labels (default:retrodetect)')

    return parser.parse_args()


def time_to_seconds(time_string: str) -> int:
    """
    Converts a time string in HH:MM:SS format to total seconds.

    Args:
        time_string (str): The time string in HH:MM:SS format. Hours (HH) can optionally
                  be prefixed with a plus (+) or minus (-) sign to indicate
                  positive or negative durations, respectively. Minutes (MM)
                  and seconds (SS) must be within the range of 00 to 59.

    Returns:
        int: The total number of seconds represented by the time string.

    Raises:
        ValueError: If the time string is not in the correct format (HH:MM:SS)
                    or if any of the time components are outside the valid range.

    Examples:
        >>> time_to_seconds("01:23:45")  # Returns 5025
        >>> time_to_seconds("10:00:00")  # Returns 36000
        >>> time_to_seconds("-02:30:15")  # Returns -8715 (negative duration)
        >>> time_to_seconds("abc:def:ghi")  # Raises ValueError
    """
    time_hms = [int(s) for s in re.findall(r'([0-9]{1,2})[:\+]([0-9]{2})[:\+]([0-9]{2})', time_string)[0]]
    total_seconds = time_hms[0] * 3600 + time_hms[1] * 60 + time_hms[2]
    return total_seconds


def main():
    args = get_args()
    logging.basicConfig(
        format="%(name)s:%(asctime)s:%(levelname)s:%(message)s",
        level=logging.DEBUG if args.verbose else logging.INFO
    )

    # Find files
    imgpath = args.imgpath
    for possible_path in [x[0] for x in os.walk(imgpath) if '/.' not in x[0]]:
        image_paths = sorted(glob(possible_path + '/*.np'))
        retro = Retrodetect()
        for i, path in enumerate(image_paths):
            image_filename = path.split('/')[-1]  # remove the path
            logger.info(image_filename)
            if not args.before > time_to_seconds(image_filename) > args.after:
                continue
            with open(path, 'rb') as file:
                res = retro.process_photo(pickle.load(file))
            json_list = list()
            for r in res:

                # not a tag, so skip
                if r[0] < float(args.threshold):
                    continue

                metastring = "%0.1f" % r[0] + '(' + ', '.join(["%0.0f" % d for d in r[3:9]]) + ')'
                json_item = {"x": int(r[1]), "y": int(r[2]), "source": args.sourcename, "meta": metastring,
                             "version": "retrodetect, v2.0", "label": "", "confidence": r[0]}
                json_list.append(json_item)

            datapath = possible_path + '/' + args.sourcename
            try:
                os.mkdir(datapath)
            except FileExistsError:
                pass
            data_file_name = image_filename[:-2] + 'json'
            with open(datapath + '/' + data_file_name, 'w') as file:
                json.dump(json_list, file)


if __name__ == '__main__':
    main()
