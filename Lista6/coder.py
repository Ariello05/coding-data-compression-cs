# autor Paweł Dychus
from math import floor, ceil, log10
from colors import *
import sys
import os
import re


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
        descriptor = [byteify(0)]

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
            for pixel in data:
                self.image_data.append(byteify(pixel.blue))
                self.image_data.append(byteify(pixel.green))
                self.image_data.append(byteify(pixel.red))

            f.writelines(self.file_header)
            f.writelines(self.image_data)


def load_image(f, file_pixel_width, file_pixel_height):
    image_mapped = [RGB() for j in range(file_pixel_width*file_pixel_height)]

    # reading from bottom-left
    for i in range(file_pixel_height*file_pixel_width):
        blue = f.read(1)
        blue = int(blue.hex(), 16)
        green = f.read(1)
        green = int(green.hex(), 16)
        red = f.read(1)
        red = int(red.hex(), 16)

        image_mapped[i].rgb(red, green, blue)

    return image_mapped


def load_encoded(filename):

    with open(filename, "r") as f:
        w = int(f.readline())
        h = int(f.readline())

        map_ = f.readline()
        map_ = [re.split(",", item)
                for item in re.findall("(-*\d+,-*\d+,-*\d+)", map_)]
        map_ = [RGB(int(item[0]), int(item[1]), int(item[2])) for item in map_]
        return map_, w, h


def load_tga(filename, additionalInfo=False):
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
        # print('Width')
        # print(f'pixels: {byte1+byte2}')
        byte1 = int(byte1.hex(), 16)
        byte2 = int(byte2.hex(), 16) * 256
        file_pixel_width = byte1 + byte2
        # if additionalInfo:
        #    print(f'pixels [INT]: {file_pixel_width}')

        byte1 = f.read(1)
        byte2 = f.read(1)
        # print('Height')
        # print(f'pixels: {byte1+byte2}')
        byte1 = int(byte1.hex(), 16)
        byte2 = int(byte2.hex(), 16) * 256
        file_pixel_height = byte1 + byte2
        # if additionalInfo:
        #    print(f'pixels [INT]: {file_pixel_height}')

        byte = f.read(1)
        # print('Pixel depth')
        # print(byte)
        file_pixel_depth_in_bits = int(byte.hex(), 16)
        # print(file_pixel_depth_in_bits)

        byte = f.read(1)
        # print('Image descriptor')
        # print(byte)
        # print("Loading pixels!")
        return load_image(f, file_pixel_width, file_pixel_height), file_pixel_width, file_pixel_height


def get_pixel_mapper(bits):
    map_ = [0 for i in range(512)]

    current = 0
    step = floor(512/2**(bits))
    for i in range(2**(bits)):
        next_ = current + step

        for j in range(current, next_):
            map_[j] = round((current+next_)/2)
        current += step

    def pixel_mapper(pixel):
        # print(
        #    f"{pixel.g} -> {map_[pixel.g+256] - 256} => {(map_[pixel.g+256] - 256)-pixel.g}")
        return RGB(map_[pixel.r+256] - 256, map_[pixel.g+256] - 256, map_[pixel.b+256] - 256)

    return pixel_mapper


def quantumize(pixel_map, bits):

    pixel_quantumazing_function = get_pixel_mapper(bits)

    new_map = []
    prev_pixel = RGB(0, 0, 0)
    prev_q = RGB(0, 0, 0)

    for pixel in pixel_map:
        difference = pixel - prev_pixel - prev_q
        #print(f"{pixel.g} - {prev_pixel.g} - {prev_q.g}")
        mapped = (pixel_quantumazing_function(difference))
        new_map.append(mapped)

        prev_pixel = pixel
        prev_q = mapped - difference

    return new_map


def decode_map(pixel_map):
    prev_pixel = RGB(0, 0, 0)
    new_map = []
    for pixel in pixel_map:
        new_pixel = pixel + prev_pixel
        # 256 case
        if new_pixel.r > 255:
            new_pixel[0] = 255
        if new_pixel.b > 255:
            new_pixel[2] = 255
        if new_pixel.g > 255:
            new_pixel[1] = 255

        # -1 case
        if new_pixel.r < 0:
            new_pixel[0] = 0
        if new_pixel.b < 0:
            new_pixel[2] = 0
        if new_pixel.g < 0:
            new_pixel[1] = 0

        new_map.append(new_pixel)
        prev_pixel = new_pixel
    return new_map


def decode(input_, output_):
    pixel_map, w, h = load_encoded(input_)
    pixel_map = decode_map(pixel_map)
    tga = TGAImage()
    tga.init_header()
    tga.finish_header(w, h)
    tga.save_to_file(pixel_map, output_)


def encode(input_, output_, bits):
    pixel_map, w, h = load_tga(input_)
    print("File loaded.")
    print("Proccessing...")
    # tga = TGAImage()
    # tga.init_header()
    # tga.finish_header(len(pixel_map[0]), len(pixel_map))
    quantumized_map = quantumize(pixel_map, bits)
    with open(output_, "w") as f:
        f.write(str(w))
        f.write("\n")
        f.write(str(h))
        f.write("\n")
        for pixel in quantumized_map:
            f.write(pixel.file_format())

    print(f"Image proccessed and saved to: {output_}")


if __name__ == '__main__':

    try:
        if len(sys.argv) < 4:
            raise Exception('')
        else:
            command = sys.argv[1]
            input_ = sys.argv[2]
            output_ = sys.argv[3]

            if command == "--encode" or command == "-E":
                bits = int(sys.argv[4], 10)
                if bits not in range(1, 8):
                    print(f"Bits must be in range of 1-7")
                    raise Exception('')
                encode(input_, output_, bits)
            elif command == "--decode" or command == "-D":
                decode(input_, output_)

            print(f"{OPENGREEN}SUCCESS{CLOSECOLOR}")
    except Exception as e:
        print(f"{OPENRED}FAILURE{CLOSECOLOR}")
        print(e)
        print(
            f"Expected: {OPENBLUE} (--encode -E | --decode -D) input.tga output.bin Bits{CLOSECOLOR}")
        print(
            f"Got:\t  {' '.join(sys.argv[1:])}")
