# autor Paweł Dychus
from math import floor, ceil, log10
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


def byteify(value, bytes=1):
    return value.to_bytes(bytes, byteorder="big")


class TGAImage:
    def init_header(self):
        id_length = [byteify(0)]
        color_map_type = [byteify(0)]
        image_type = [byteify(2)]
        color_map = [byteify(0), byteify(0), byteify(0),
                     byteify(0), byteify(0)]
        x_origin = [byteify(0), byteify(0)]
        y_origin = [byteify(0), byteify(0)]

        self.file_header = []
        self.file_header.extend(id_length)
        self.file_header.extend(color_map_type)
        self.file_header.extend(image_type)
        self.file_header.extend(color_map)
        self.file_header.extend(x_origin)
        self.file_header.extend(y_origin)

    def finish_header(self, width, height, pixel_bits=RGB(8, 8, 8)):
        width = [byteify(width % 256), byteify(floor(width/256))]
        height = [byteify(height % 256), byteify(floor(height/256))]
        pixel_depth = [
            byteify(max([pixel_bits.r, pixel_bits.g, pixel_bits.b])*3)]
        descriptor = [byteify(32)]

        self.file_header.extend(width)
        self.file_header.extend(height)
        self.file_header.extend(pixel_depth)
        self.file_header.extend(descriptor)

        self.red_bits = pixel_bits.r
        self.green_bits = pixel_bits.g
        self.blue_bits = pixel_bits.b

    def save_to_file(self, data, filename):
        with open(filename, "wb") as f:
            self.image_data = []
            for row in data:
                for pixel in row:
                    self.image_data.append(byteify(pixel.blue))
                    self.image_data.append(byteify(pixel.green))
                    self.image_data.append(byteify(pixel.red))

            f.writelines(self.file_header)
            f.writelines(self.image_data)


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


def get_data(filename, additionalInfo=False):
    with open(filename, 'rb') as f:
        byte = f.read(1)
        #print('ID LENGTH')
        # print(byte)

        byte = f.read(1)
        #print('COLOR MAP TYPE')
        # print(byte)

        byte = f.read(1)
        #print('IMAGE TYPE')
        # print(byte)

        byte = f.read(5)
        #print('COLOR MAP')
        # print(byte)

        byte = f.read(2)
        #print('-IMAGE SPECS-')
        # print('X-origin')
        # print(byte)

        byte = f.read(2)
        # print('Y-origin')
        # print(byte)

        byte1 = f.read(1)
        byte2 = f.read(1)
        # print('Width')
        #print(f'pixels: {byte1+byte2}')
        byte1 = int(byte1.hex(), 16)
        byte2 = int(byte2.hex(), 16) * 256
        file_pixel_width = byte1 + byte2
        # if additionalInfo:
        #    print(f'pixels [INT]: {file_pixel_width}')

        byte1 = f.read(1)
        byte2 = f.read(1)
        # print('Height')
        #print(f'pixels: {byte1+byte2}')
        byte1 = int(byte1.hex(), 16)
        byte2 = int(byte2.hex(), 16) * 256
        file_pixel_height = byte1 + byte2
        # if additionalInfo:
        #    print(f'pixels [INT]: {file_pixel_height}')

        byte = f.read(1)
        #print('Pixel depth')
        # print(byte)
        file_pixel_depth_in_bits = int(byte.hex(), 16)
        # print(file_pixel_depth_in_bits)

        byte = f.read(1)
        #print('Image descriptor')
        # print(byte)
        #print("Loading pixels!")
        return load_image(f, file_pixel_width, file_pixel_height)


def get_pixel_mapper(bits):
    map_ = [0 for i in range(256)]

    current = 0
    step = floor(256/2**(bits))
    for i in range(2**(bits)):
        next_ = current + step
        for j in range(current, next_):
            map_[j] = floor((current+next_)/2)
        current += step

    def pixel_mapper(value):
        return map_[value]

    return pixel_mapper


def quantumize(pixel_map, pixel_data):
    red_range = pixel_data.r
    green_range = pixel_data.g
    blue_range = pixel_data.b

    red_map = get_pixel_mapper(red_range)
    green_map = get_pixel_mapper(green_range)
    blue_map = get_pixel_mapper(blue_range)

    new_map = []
    for row in pixel_map:
        new_row = []
        for pixel in row:
            new_pixel = RGB(red_map(pixel.r), green_map(
                pixel.g), blue_map(pixel.b))

            new_row.append(new_pixel)

        new_map.append(new_row)

    return new_map


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


def run(input_, output_, R, G, B):
    pixel_map = get_data(input_)
    print("File loaded.")
    print("Proccessing...")
    tga = TGAImage()
    tga.init_header()
    tga.finish_header(len(pixel_map[0]), len(pixel_map))
    quantumized_map = quantumize(pixel_map, RGB(R, G, B))

    mse_r, mse_g, mse_b, mse_all = get_MSE(pixel_map, quantumized_map)
    snr_r, snr_g, snr_b, snr_all = get_SNR(
        pixel_map, [mse_r, mse_g, mse_b, mse_all])

    print(f"mse\t= {mse_all}")
    print(f"mse(r)\t= {mse_r}")
    print(f"mse(g)\t= {mse_g}")
    print(f"mse(b)\t= {mse_b}")
    print()

    print(f"SNR\t= {snr_all} ({10*log10(snr_all)}dB)")
    print(f"SNR(r)\t= {snr_r} ({10*log10(snr_r)}dB)")
    print(f"SNR(g)\t= {snr_g} ({10*log10(snr_g)}dB)")
    print(f"SNR(b)\t= {snr_b} ({10*log10(snr_b)}dB)")

    tga.save_to_file(quantumized_map, "out.tga")
    print(f"Image proccessed and saved to: {output_}")


if __name__ == '__main__':

    try:
        if len(sys.argv) < 2:
            print(f"{OPENRED}FAILURE{CLOSECOLOR}")
            print(
                f"Expected: {OPENBLUE}input.tga output.tga R G B{CLOSECOLOR}")
            print(
                f"Got:\t  {' '.join(sys.argv[1:])}")
            raise Exception('')
        else:
            input_ = sys.argv[1]
            output_ = sys.argv[2]
            R = int(sys.argv[3], 10)
            G = int(sys.argv[4], 10)
            B = int(sys.argv[5], 10)
            if R not in range(9) or G not in range(9) or B not in range(9):
                print(f"Bits must be in range of 0-8")
                raise Exception('')

            run(input_, output_, R, G, B)

            print(f"{OPENGREEN}SUCCESS{CLOSECOLOR}")
    except:
        print(f"{OPENRED}FAILURE{CLOSECOLOR}")
        print(
            f"Expected: {OPENBLUE}input.tga output.tga R G B{CLOSECOLOR}")
        print(
            f"Got:\t  {' '.join(sys.argv[1:])}")
