import struct
from bitstring import ConstBitStream, BitArray
from bitarray import bitarray


class Node:

    def __init__(self, symbol=None):
        self.value = 1
        self.symbol = symbol
        self.right = None
        self.left = None
        self.parent = None

    @property
    def rightNode(self):
        return self.right

    @property
    def leftNode(self):
        return self.left

    @rightNode.setter
    def rightNode(self, right):
        if type(right) != Node:
            raise TypeError("Expected Node!")
        self.right = right

    @leftNode.setter
    def leftNode(self, left):
        if type(left) != Node:
            raise TypeError("Expected Node!")

        self.left = left

    def traverse_to_top(self):
        print(f"Start at: ({self.value},{self.symbol})")
        node = self.parent
        while(node != None):
            print(f"Parent: ({node.value},{node.symbol})")
            node = node.parent

        print()

    def traverse_from_top(self, flag="T", treeCode=""):  # DFS
        print(f"[{flag}] ({self.symbol}, {self.value}) \t - {treeCode}")
        if self.left is not None:
            self.left.traverse_from_top("L", treeCode+'0')

        if self.right is not None:
            self.right.traverse_from_top("R", treeCode+'1')


strr = "abcdefghijklmnopqrstuvwxyz"
fixed_code = {val: '{0:05b}'.format(ord(val)-96)
              for (i, val) in enumerate(strr)}
char_code = {'{0:05b}'.format(
    ord(val)-96): val for (i, val) in enumerate(strr)}


class HuffmanCode:

    def decode(self, inputName, outputName):
        print("-"*32)
        self.top = Node("NYT")
        self.top.value = 0
        self.NYT = self.top
        self.characters = {}

        self.out = open(outputName, "w")

        file = ConstBitStream(filename=inputName)

        while True:

            if self.NYT == self.top:
                bits = file.read(8)
                bits = str(bits)[2:]
                #s = bits

                # print(f"Bits: {bits}")
                num = int(bits, 16)
                character = chr(num)
                # character = char_code[bits]

                self.insert(character)
                self.out.write(character)
            else:
                node = self.top
                # print(node.value, node.symbol)
                while(node.left != None and node.right != None):
                    try:
                        bit = file.read(1)
                    except:
                        # print(s)
                        self.out.close()
                        return

                    bit = str(bit)[2:]
                    #s += bit
                    # if len(s) > 32:
                    #    print(s[:32])
                    #    s = s[32:]

                    # print(f"Bit: {bit}")
                    if not bit:
                        # print(s)
                        return

                    if bit == '0':
                        node = node.left
                    elif bit == '1':
                        node = node.right

                    # print(bit, node.value, node.symbol)
                    # print(f"Bit: {bit}")

                character = node.symbol
                if character == "NYT":
                    try:
                        bits = file.read(8)
                    except:
                        # print(s)
                        self.out.close()
                        return

                    bits = str(bits)[2:]
                    #s += bits

                    # if len(s) > 32:
                    #    print(s[:32])
                    #    s = s[32:]
                    # print(bits)

                    #print(f"Bits: {bits}")
                    try:
                        # character = char_code[bits]
                        num = int(bits, 16)
                        if num == 0:
                            return

                        character = chr(num)
                    except KeyError:
                        #    print(s)
                        self.out.close()
                        return

                self.out.write(character)
                self.insert(character)

            # self.top.traverse_from_top()
        file.close()
        self.out.close()

    def encode(self, inputName, outputName):
        self.top = Node("NYT")
        self.top.value = 0
        self.NYT = self.top
        self.characters = {}
        self.bits = ""

        self.out = open(outputName, "wb")

        file = open(inputName, "r")
        while True:
            char = file.read(1)
            if not char:
                break

            ch = self.insert(char)
            #re = int(ch, 2)
            #print(ch, re)
            self.bits += ch

            if len(self.bits) > 32:
                wr, self.bits = self.bits[0:32], self.bits[32:]
                print(wr)
                num = int(wr, 2)
                by = num.to_bytes(4, byteorder="big")
                self.out.write(by)

        # print(self.bits)
        endFile = self.getTreeCoding(self.NYT)
        # print(self.bits)
        bits = self.bits + endFile + ('0' * 32)
        bits = bits[0:32]

        # testnode = self.characters["j"]
        # print("j_test:", self.getTreeCoding(testnode))

        print(bits)

        num = int(bits, 2)
        by = num.to_bytes(4, byteorder="big")

        self.top.traverse_from_top()
        self.out.write(by)

        file.close()
        self.out.close()

    def insert(self, char):  # encoding main function
        new_node = Node(char)
        write = ""

        if self.top.right == None:
            new_top = Node()
            new_top.left = self.top
            new_top.right = new_node
            self.top = new_top

            # write = fixed_code[char]
            # write = ord(char)
            # print(bin(ord(char))[2:])
            write = bin(ord(char))[2:]
            if int(write, 2) not in range(0, 127):
                raise Exception(
                    f"Character <{char}> out of range of alphabet")

            w_size = 8 - len(write)
            write = ("0" * w_size) + write

            new_node.parent = new_top
            self.NYT.parent = new_top
            self.characters[char] = new_node

        else:
            if char not in self.characters:
                replace_nyt = Node()
                replace_nyt.left = self.NYT
                replace_nyt.right = new_node
                replace_nyt.parent = self.NYT.parent
                replace_nyt.value = 0  # will update

                nyt_code = self.getTreeCoding(self.NYT)
                fixed = bin(ord(char))[2:]
                if int(fixed, 2) not in range(0, 127):
                    raise Exception(
                        f"Character <{char}> out of range of alphabet")

                w_size = 8 - len(fixed)
                fixed = ("0" * w_size) + fixed
                write = nyt_code + fixed
                # write = nyt_code+fixed_code[char]

                self.NYT.parent.left = replace_nyt
                self.NYT.parent = replace_nyt
                new_node.parent = replace_nyt
                new_node.value = 0  # will update

                self.characters[char] = new_node
            else:
                # self.characters[char].value += 1
                char_code = self.getTreeCoding(self.characters[char])
                write = char_code

            self.check_for_swaps(char)
            self.update_path(char)

        return write

    def swap(self, node_one, node_two):
        parent_one = node_one.parent
        parent_two = node_two.parent

        if node_one == parent_one.left:
            parent_one.left = node_two
        else:
            parent_one.right = node_two

        if node_two == parent_two.left:
            parent_two.left = node_one
        else:
            parent_two.right = node_one

        node_one.parent = parent_two
        node_two.parent = parent_one

    def check_for_swaps(self, char):
        node = self.characters[char]
        degree = len(self.getTreeCoding(node))
        for to_check in self.characters.values():
            if to_check.value == node.value:
                to_check_degree = len(self.getTreeCoding(to_check))
                if to_check_degree < degree:
                    self.swap(node, to_check)

                    degree = len(self.getTreeCoding(node))

        start = node.parent
        degree -= 1
        while start != self.top:
            internals = self.get_nodes(degree, start.value)
            if len(internals) == 0:
                start = start.parent
                degree -= 1
                continue
            else:
                self.swap(internals[0], start)
                degree = len(self.getTreeCoding(start))
                degree -= 1
                start = start.parent
                continue

    # gets nodes above degree of same value

    def get_nodes(self, degree, value):
        queue = [self.top]
        internal = []

        while len(queue) > 0:
            node = queue.pop(0)
            s_degree = len(self.getTreeCoding(node))
            if s_degree > degree:
                continue

            if node.value + 1 == value:
                internal.append(node)

            if node.left is not None:
                queue.append(node.left)
            if node.right is not None:
                queue.append(node.right)

        return internal

    def update_path(self, char):
        node = self.characters[char]
        node.value += 1
        start = node.parent
        while start != None:
            start.value += 1
            start = start.parent

    def getTreeCoding(self, node):
        current = node
        parent = node.parent

        # if parent is None:
        #    return None  # ONLY NYT

        str_ = ''

        while parent is not None:
            if current is parent.left:
                str_ = '0' + str_
            elif current is parent.right:
                str_ = '1' + str_
            current = parent
            parent = current.parent

        return str_


hf = HuffmanCode()
hf.encode("test.txt", "exit.bin")
hf.decode("exit.bin", "exit2.txt")

# a = "00001000"
# num = int(a, 2)
# file = open("binary", "wb")
# by = num.to_bytes(1, byteorder="big")
# print(by)

# file.write(by)
# file.close()
# file = open("binary", "rb")
# file = ConstBitStream(filename='binary')
# r = file.read('bin:8')
# print(r)
# r = str(r)[2:]
# print(r)
# file.close()
