from pathlib import Path

import numpy

import retrodetect


def test_retrodetect():
    path = Path(__file__).parent.joinpath(
        'data/sessionA/setA/cam5/02D49634733/20200805_11+59+03.206111.0019_000001.np').absolute()
    print(path)
    retro = retrodetect.Retrodetect()

    photo_item = numpy.load(path, allow_pickle=True)
    retro.process_photo(photo_item=photo_item)
