from PIL import Image
import os

p = os.path.join(os.getcwd(), "test", "AD", "1020512_95.jpeg")
print(p)
im = Image.open(p)

print(im.size)
