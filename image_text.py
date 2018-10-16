from PIL import Image
import argparse

# define var
ascii_char = list("$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. ")
img = ""
text = ""

# define function
def get_char(r, g, b):
    length = len(ascii_char)
    gray = int(0.2126 * r + 0.7152 * g + 0.0722 * b)

    unit = (256.0 + 1)/length
    return ascii_char[int(gray/unit)]

# define parser
parser = argparse.ArgumentParser()

# add argument to parser
parser.add_argument("--s", type = str, dest = "image", help = "Image to convert")
parser.add_argument("--w", type = int, dest = "width", default = 80, help = "Desire width")
parser.add_argument("--h", type = int, dest="height", default = 80, help = "Desire height")

args = parser.parse_args()

IMG = args.image
WIDTH = args.width
HEIGHT = args.height

# program start here
# load image
try:
    img = Image.open(IMG)
    img = img.resize((WIDTH, HEIGHT), Image.NEAREST)
except IOError:
    print("Cannot load image {}.".format(IMG))

for i in range(HEIGHT):
    for j in range(WIDTH):
        text += get_char(*img.getpixel((j, i)))
    text += "\n"

# print result

print("\n\n\n\n\n", text)