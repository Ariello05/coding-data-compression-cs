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