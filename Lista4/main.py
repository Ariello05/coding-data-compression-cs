# autor Paweł Dychus
import math
from colors import *
import sys
import os


class RGB:

    def __init__(self, r=0, g=0, b=0):
        self.rgb(r, g, b)

    def rgb(self, red, green, blue):
        self.red = red
        self.green = green
        self.blue = blue

    def __add__(self, other):
        return RGB(self.red + other.red, self.green + other.green, self.blue + other.blue)

    def __sub__(self, other):
        return RGB(self.red - other.red, self.green - other.green, self.blue - other.blue)

    def __truediv__(self, num):
        return RGB(self.red // num, self.green // num, self.blue // num)

    def __mod__(self, num):
        return RGB(self.red % num, self.green % num, self.blue % num)

    def __repr__(self):
        return f"({self.red},{self.green},{self.blue})"

    def __getitem__(self, key):
        if key == 0:
            return self.red
        elif key == 1:
            return self.green
        elif key == 2:
            return self.blue
        else:
            raise IndexError("Index out of bouds, expected [0-3]")

    def __setitem__(self, key, value):
        if key == 0:
            self.red = value
        elif key == 1:
            self.green = value
        elif key == 2:
            self.blue = value
        else:
            raise IndexError("Index out of bouds, expected [0-3]")


def color_entropy(pixel_map):
    r_stat = [0 for i in range(256)]
    g_stat = [0 for i in range(256)]
    b_stat = [0 for i in range(256)]

    for row in pixel_map:
        for pixel in row:
            r_stat[pixel.red] += 1
            g_stat[pixel.green] += 1
            b_stat[pixel.blue] += 1

    all_stat = [(r_stat[i] + g_stat[i] + b_stat[i])/3 for i in range(0, 256)]

    r_stat = list(filter(lambda u: u > 0, r_stat))  # remove 0s
    g_stat = list(filter(lambda u: u > 0, g_stat))
    b_stat = list(filter(lambda u: u > 0, b_stat))
    all_stat = list(filter(lambda u: u > 0, all_stat))

    red_sum = 0
    green_sum = 0
    blue_sum = 0
    full_sum = 0

    pixel_count = len(pixel_map) * len(pixel_map[0])

    for red in r_stat:
        p = (red / pixel_count)
        red_sum += p * (-1)*math.log2(p)

    for green in g_stat:
        p = (green / pixel_count)
        green_sum += p * (-1)*math.log2(p)

    for blue in b_stat:
        p = (blue / pixel_count)
        blue_sum += p * (-1)*math.log2(p)

    for mixed in all_stat:
        p = (mixed / pixel_count)
        full_sum += p * (-1)*math.log2(p)

    return [red_sum, green_sum, blue_sum, full_sum]


def load_image(f, file_pixel_width, file_pixel_height):
    image_mapped = [[RGB() for j in range(file_pixel_width)]
                    for i in range(file_pixel_height)]  # `height` lists of `width` RGB's

    # reading from bottom-left
    for i in range(file_pixel_height):
        for j in range(file_pixel_width):
            blue = f.read(1)
            blue = int(blue.hex(), 16)
            green = f.read(1)
            green = int(green.hex(), 16)
            red = f.read(1)
            red = int(red.hex(), 16)
            # print(
            #    f'Pixel [{j},{i}] has RGB: ({int(red.hex(),16)},{int(green.hex(),16)},{int(blue.hex(),16)})')
            reversed_height = file_pixel_height - i - 1

            image_mapped[reversed_height][j].rgb(red, green, blue)

        # for k in range(file_pixel_depth_in_bits/8):

    return image_mapped


def get_data(filename, additionalInfo):
    with open(filename, 'rb') as f:
        byte = f.read(1)
        # print('ID LENGTH')
        # print(byte)

        byte = f.read(1)
        # print('COLOR MAP TYPE')
        # print(byte)

        byte = f.read(1)
        # print('IMAGE TYPE')
        # print(byte)

        byte = f.read(5)
        # print('COLOR MAP')
        # print(byte)

        byte = f.read(2)
        # print('-IMAGE SPECS-')
        # print('X-origin')
        # print(byte)

        byte = f.read(2)
        # print('Y-origin')
        # print(byte)

        byte1 = f.read(1)
        byte2 = f.read(1)
        if additionalInfo:
            print('Width')
        # print(f'pixels: {byte1+byte2}')
        byte1 = int(byte1.hex(), 16)
        byte2 = int(byte2.hex(), 16) * 256
        file_pixel_width = byte1 + byte2
        if additionalInfo:
            print(f'pixels [INT]: {file_pixel_width}')

        byte1 = f.read(1)
        byte2 = f.read(1)
        if additionalInfo:
            print('Height')
        # print(f'pixels: {byte1+byte2}')
        byte1 = int(byte1.hex(), 16)
        byte2 = int(byte2.hex(), 16) * 256
        file_pixel_height = byte1 + byte2
        if additionalInfo:
            print(f'pixels [INT]: {file_pixel_height}')

        byte = f.read(1)
        # print('Pixel depth')
        # print(byte)
        file_pixel_depth_in_bits = int(byte.hex(), 16)
        # print(file_pixel_depth_in_bits)

        byte = f.read(1)
        # print('Image descriptor')
        # print(byte)
        print("Loading pixels!")
        return load_image(f, file_pixel_width, file_pixel_height)


def new_standard(n, w, nw):
    pixel = RGB()

    for i in range(3):
        if nw[i] >= max([n[i], w[i]]):
            pixel[i] = max([n[i], w[i]])
        elif nw[i] <= min([n[i], w[i]]):
            pixel[i] = min([n[i], w[i]])
        else:
            pixel[i] = (w[i]+n[i]-nw[i]) % 256

    return pixel


def get_map_functions():

    names = ["W", "N", "NW", "N+W-NW",
             "N+(W-NW)/2", "W+(N-NW)/2", "(N+W)/2", "New standard"]
    functions = []
    functions.append(lambda n, w, nw: w)
    functions.append(lambda n, w, nw: n)
    functions.append(lambda n, w, nw: nw)
    functions.append(lambda n, w, nw: ((n+w)-nw) % 256)
    functions.append(lambda n, w, nw: (n+(w-nw)/2) % 256)
    functions.append(lambda n, w, nw: (w+(n-nw)/2) % 256)
    functions.append(lambda n, w, nw: ((n+w)/2) % 256)
    functions.append(new_standard)

    return functions, names


def jpeg_ls(pixel_map, map_function):
    result = []
    for i in range(0, len(pixel_map)):
        row = []
        for j in range(0, len(pixel_map[i])):
            if i > 0:
                n = pixel_map[i-1][j]
            else:
                n = RGB()

            if j > 0:
                w = pixel_map[i][j-1]
            else:
                w = RGB()

            if i > 0 and j > 0:
                nw = pixel_map[i-1][j-1]
            else:
                nw = RGB()

            row.append((pixel_map[i][j]-map_function(n, w, nw)) % 256)

        result.append(row)

    return result


def run(filename, additionalInfo=False):
    pixel_map = get_data(filename, additionalInfo)
    print("File loaded.")
    funs, names = get_map_functions()
    input_entropy = color_entropy(pixel_map)
    print()
    print(
        f"input_entropy (Red,Green,Blue,All): \t({input_entropy[0]},{input_entropy[1]},{input_entropy[2]},{input_entropy[3]})")

    mod_entropy = []
    i = 0
    for mapper in funs:
        modified = jpeg_ls(pixel_map, mapper)
        temp = color_entropy(modified)
        temp.append(i)
        mod_entropy.append(temp)
        i += 1

    red_min = min(mod_entropy, key=lambda u: u[0])
    green_min = min(mod_entropy, key=lambda u: u[1])
    blue_min = min(mod_entropy, key=lambda u: u[2])
    full_min = min(mod_entropy, key=lambda u: u[3])

    if additionalInfo:
        mod_entropy = sorted(mod_entropy, key=lambda u: u[0])
        print()
        for i in range(len(funs)):
            print(
                f"{OPENRED}Reds{CLOSECOLOR}:\t({mod_entropy[i][0]}, {names[mod_entropy[i][4]]})")
        mod_entropy = sorted(mod_entropy, key=lambda u: u[1])
        print()
        for i in range(len(funs)):
            print(
                f"{OPENGREEN}Greens{CLOSECOLOR}:\t({mod_entropy[i][1]}, {names[mod_entropy[i][4]]})")
        mod_entropy = sorted(mod_entropy, key=lambda u: u[2])
        print()
        for i in range(len(funs)):
            print(
                f"{OPENBLUE}Blues{CLOSECOLOR}:\t({mod_entropy[i][2]}, {names[mod_entropy[i][4]]})")
        mod_entropy = sorted(mod_entropy, key=lambda u: u[3])
        print()
        for i in range(len(funs)):
            print(
                f"{CLOSECOLOR}Alls{CLOSECOLOR}:\t\t({mod_entropy[i][3]}, {names[mod_entropy[i][4]]})")

    print("\n\t\t\t(value,name)")
    print(
        f"Best for {OPENRED}red{CLOSECOLOR}:\t({red_min[0]}, {names[red_min[4]]})")
    print(
        f"Best for {OPENGREEN}green{CLOSECOLOR}:\t({green_min[1]}, {names[green_min[4]]})")
    print(
        f"Best for {OPENBLUE}blue{CLOSECOLOR}:\t({blue_min[2]}, {names[blue_min[4]]})")
    print(
        f"Best for {CLOSECOLOR}all{CLOSECOLOR}:\t     ({full_min[3]}, {names[full_min[4]]})")

    print("Finished.")


if __name__ == '__main__':

    try:
        if len(sys.argv) < 2:
            print(f"{OPENRED}FAILURE{CLOSECOLOR}")
            print(
                f"Expected: {OPENBLUE}filepath, <optionally> -a | --additionalInfo{CLOSECOLOR}")
            print(
                f"Got:\t  {' '.join(sys.argv[1:])}")
        else:
            filepath = sys.argv[1]
            if len(sys.argv) == 3:
                run(filepath, sys.argv[2])
            else:
                run(filepath)
            print(f"{OPENGREEN}SUCCESS{CLOSECOLOR}")
    except:
        print(f"{OPENRED}FAILURE{CLOSECOLOR}")
        raise
