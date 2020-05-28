from math import floor, ceil, log10
from colors import *
import sys


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

    def file_format(self):
        return self.__repr__()

    @property
    def all(self):
        return (self.red + self.green + self.blue)//3

    @property
    def r(self):
        return self.red

    @property
    def g(self):
        return self.green

    @property
    def b(self):
        return self.blue

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
            reversed_height = file_pixel_height - i - 1

            image_mapped[reversed_height][j].rgb(red, green, blue)

    return image_mapped


def load_tga(filename, additionalInfo=False):
    with open(filename, 'rb') as f:
        byte = f.read(1)
        # print('ID LENGTH')
        byte = f.read(1)
        # print('COLOR MAP TYPE')
        byte = f.read(1)
        # print('IMAGE TYPE')
        byte = f.read(5)
        # print('COLOR MAP')
        byte = f.read(2)
        # print('-IMAGE SPECS-')
        # print('X-origin')
        byte = f.read(2)
        # print('Y-origin')
        byte1 = f.read(1)
        byte2 = f.read(1)
        # print('Width')
        byte1 = int(byte1.hex(), 16)
        byte2 = int(byte2.hex(), 16) * 256
        file_pixel_width = byte1 + byte2
        byte1 = f.read(1)
        byte2 = f.read(1)
        # print('Height')
        byte1 = int(byte1.hex(), 16)
        byte2 = int(byte2.hex(), 16) * 256
        file_pixel_height = byte1 + byte2
        byte = f.read(1)
        # print('Pixel depth')
        file_pixel_depth_in_bits = int(byte.hex(), 16)
        byte = f.read(1)
        # print('Image descriptor')
        return load_image(f, file_pixel_width, file_pixel_height)


def get_MSE(pixel_map, quantumized_map):
    sum_red = 0
    sum_green = 0
    sum_blue = 0
    sum_all = 0

    size_ = len(pixel_map) * len(pixel_map[0])
    for i in range(len(pixel_map)):
        for j in range(len(pixel_map[i])):
            q_r = (pixel_map[i][j].r - quantumized_map[i][j].r) ** 2
            q_g = (pixel_map[i][j].g - quantumized_map[i][j].g) ** 2
            q_b = (pixel_map[i][j].b - quantumized_map[i][j].b) ** 2

            sum_red += q_r
            sum_green += q_g
            sum_blue += q_b
            sum_all += (q_r+q_g+q_b)/3

    return sum_red/size_, sum_green/size_, sum_blue/size_, sum_all/size_


def get_SNR(pixel_map, mse):
    mse_r = mse[0]
    mse_g = mse[1]
    mse_b = mse[2]
    mse_all = mse[3]

    sum_red = 0
    sum_green = 0
    sum_blue = 0
    sum_all = 0

    size_ = len(pixel_map) * len(pixel_map[0])
    for i in range(len(pixel_map)):
        for j in range(len(pixel_map[i])):
            q_r = (pixel_map[i][j].r) ** 2
            q_g = (pixel_map[i][j].g) ** 2
            q_b = (pixel_map[i][j].b) ** 2

            sum_red += q_r
            sum_green += q_g
            sum_blue += q_b
            sum_all += (q_r+q_g+q_b)/3

    if mse_r == 0:
        mse_r = 1
        sum_red = size_
    if mse_g == 0:
        mse_g = 1
        sum_green = size_
    if mse_b == 0:
        mse_b = 1
        sum_blue = size_
    if mse_all == 0:
        mse_all = 1
        sum_all = size_

    return (sum_red/size_)/mse_r, (sum_green/size_)/mse_g, (sum_blue/size_)/mse_b, (sum_all/size_)/mse_all


def compare(input_, output_):
    original_map = load_tga(input_)
    decoded_map = load_tga(output_)

    mse_r, mse_g, mse_b, mse_all = get_MSE(original_map, decoded_map)
    snr_r, snr_g, snr_b, snr_all = get_SNR(
        original_map, [mse_r, mse_g, mse_b, mse_all])

    print(f"mse\t= {mse_all}")
    print(f"mse(r)\t= {mse_r}")
    print(f"mse(g)\t= {mse_g}")
    print(f"mse(b)\t= {mse_b}")
    print()

    print(f"SNR\t= {snr_all} ({10*log10(snr_all)}dB)")
    print(f"SNR(r)\t= {snr_r} ({10*log10(snr_r)}dB)")
    print(f"SNR(g)\t= {snr_g} ({10*log10(snr_g)}dB)")
    print(f"SNR(b)\t= {snr_b} ({10*log10(snr_b)}dB)")


if __name__ == '__main__':

    try:
        if len(sys.argv) < 3:
            raise Exception('')
        else:
            input_ = sys.argv[1]
            output_ = sys.argv[2]

            compare(input_, output_)

            print(f"{OPENGREEN}SUCCESS{CLOSECOLOR}")
    except Exception as e:
        print(f"{OPENRED}FAILURE{CLOSECOLOR}")
        print(e)
        print(
            f"Expected: {OPENBLUE} original.tga decoded.tga{CLOSECOLOR}")
        print(
            f"Got:\t  {' '.join(sys.argv[1:])}")
