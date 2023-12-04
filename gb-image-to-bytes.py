from PIL import Image
import numpy as np
import sys


def get_palette(arr):
    arr = np.array(arr)
    return np.unique(arr)


if len(sys.argv) == 1:
    print("Usage: python gb-image-to-bytes.py filename")
    exit()

try:
    photo = Image.open(sys.argv[1])
except:
    print("Can't open file")
    exit()

photo = photo.convert('L')

width = photo.size[0]
height = photo.size[1]

if (width % 8 != 0 or height % 8 != 0):
    print("Wrong size!")
    print("Image dimensions should be multiple of 8")
    exit()

values_array = [[0]*width for i in range(height)]

for y in range(0, width):
    for x in range(0, height):
        values_array[x][y] = photo.getpixel((y, x))

result_array = [[0]*width for i in range(height)]

color_palette = get_palette(values_array)
if len(color_palette) > 4:
    # Error
    print("More than 4 colors detected")
    exit()

for y in range(0, width):
    for x in range(0, height):
        color = values_array[x][y]
        if (color == color_palette[0]):
            result_array[x][y] = 3
        elif (color_palette[0] < color < color_palette[1]):
            result_array[x][y] = 2
        elif (color_palette[1] <= color < color_palette[2]):
            result_array[x][y] = 1
        else:
            result_array[x][y] = 0

print("Color palette: ░▒▓")
for line in result_array:
    for element in line:
        match element:
            case 3:
                print("  ", end="")
            case 2:
                print("░░", end="")
            case 1:
                print("▒▒", end="")
            case 0:
                print("▓▓", end="")
    print("")

bytes_array = []

for y in range(int(height / 8)):
    for x in range(int(width / 8)):
        print("----------------")
        for n in range(8):
            line = [a[x*8:(x+1)*8] for a in result_array][y*8:(y+1)*8][n]

            bytes_out = [0, 0]

            for i in range(8):
                bytes_out[0] |= (line[i] & 0b01) << (7 - i)
                bytes_out[1] |= ((line[i] & 0b10) >> 1) << (7 - i)

            bytes_array.append(bytes_out[0])
            bytes_array.append(bytes_out[1])

            # display tile
            for element in line:
                match element:
                    case 3:
                        print("  ", end="")
                    case 2:
                        print("░░", end="")
                    case 1:
                        print("▒▒", end="")
                    case 0:
                        print("▓▓", end="")
            print("")

for num in bytes_array:
    print(hex(num), end=' ')
print(f"\n{len(bytes_array)} bytes")
