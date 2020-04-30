class RGB:
    def __init__(self):
        self.red = 0
        self.green = 0
        self.blue = 0

    def rgb(self, red, green, blue):
        self.red = red
        self.green = green
        self.blue = blue

    def __repr__(self):
        return f"({self.red},{self.green},{self.blue})"


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


with open('example0.tga', 'rb') as f:
    byte = f.read(1)
    print('ID LENGTH')
    print(byte)

    byte = f.read(1)
    print('COLOR MAP TYPE')
    print(byte)

    byte = f.read(1)
    print('IMAGE TYPE')
    print(byte)

    byte = f.read(5)
    print('COLOR MAP')
    print(byte)

    byte = f.read(2)
    print('-IMAGE SPECS-')
    print('X-origin')
    print(byte)

    byte = f.read(2)
    print('Y-origin')
    print(byte)

    byte1 = f.read(1)
    byte2 = f.read(1)
    print('Width')
    print(f'pixels: {byte1+byte2}')
    byte1 = int(byte1.hex(), 16)
    byte2 = int(byte2.hex(), 16) * 16
    file_pixel_width = byte1 + byte2
    print(f'pixels [INT]: {file_pixel_width}')

    byte1 = f.read(1)
    byte2 = f.read(1)
    print('Height')
    print(f'pixels: {byte1+byte2}')
    byte1 = int(byte1.hex(), 16)
    byte2 = int(byte2.hex(), 16) * 16
    file_pixel_height = byte1 + byte2
    print(f'pixels [INT]: {file_pixel_height}')

    byte = f.read(1)
    print('Pixel depth')
    print(byte)
    file_pixel_depth_in_bits = int(byte.hex(), 16)
    print(file_pixel_depth_in_bits)

    byte = f.read(1)
    print('Image descriptor')
    print(byte)

    print(image_mapped)


print("Finished")
