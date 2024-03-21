# Bee retroreflection detector

Detect retroreflectors in image pair.

# Installation

```bash
pip install retrodetect
```

# Usage
The `detectcontact` function in this package analyzes a sequence of photos captured by a tracking system to detect potential retroreflectors with the `detect` function captures the differences (retro-reflectors) detected between the flash and no flash images.
See examples for more details.

```python
from retrodetect import detect, detectcontact

contact,found,searchimg = detectcontact(photo_list,n,delsize=100)

output = detect(flash,noflash,blocksize=20, offset=10, searchbox=20, step=4, searchblocksize=50, ensemblesizesqrt=3, dilate=True,margin=100)
```

#Citation

