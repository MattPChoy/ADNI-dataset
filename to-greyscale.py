import os
from PIL import Image

paths = [
    "test/AD",
    "test/NC",
    "train/AD",
    "train/NC"
]

for p in paths:
    folder_fp = os.path.join(os.getcwd(), p)
    for im_fn in os.listdir(folder_fp):
        im_fp = os.path.join(folder_fp, im_fn);
        new_im = os.path.join(folder_fp, im_fn);
        im = Image.open(im_fp).convert("L")
        im.save(new_im)
