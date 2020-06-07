from functools import reduce
from colors import *
import sys
import os


def get_encoded(bits):
    p1 = str((int(bits[0]) + int(bits[1]) + int(bits[3])) % 2)
    p2 = str((int(bits[0]) + int(bits[2]) + int(bits[3])) % 2)
    p4 = str((int(bits[1]) + int(bits[2]) + int(bits[3])) % 2)

    result = p1 + p2 + bits[0] + p4 + bits[1:]
    sum_ = reduce(lambda prev, u: int(prev) + int(u), result) % 2
    result += str(sum_)

    return result


def run(input_filename, output_filename):
    with open(input_filename, "r", encoding="utf-8") as f:
        text = f.read()
        bits = ""
        for character in text:
            integer = ord(character)
            bitstring = bin(integer)[2:].rjust(8, '0')
            bits += bitstring

        bytes_ = encode(bits)
        with open(output_filename, "wb") as out:
            for byte in bytes_:
                out.write(byte)


def encode(bits):
    result = []

    while len(bits) >= 4:
        process = bits[:4]
        encoded = get_encoded(process)
        num = int(encoded, 2)
        byte = num.to_bytes(1, byteorder="big")
        result.append(byte)
        bits = bits[4:]

    return result


if __name__ == '__main__':

    try:
        if len(sys.argv) < 2:
            raise Exception('')
        else:
            input_ = sys.argv[1]
            output_ = sys.argv[2]
            run(input_, output_)

            print(f"{OPENGREEN}SUCCESS{CLOSECOLOR}")
    except Exception as e:
        print(f"{OPENRED}FAILURE{CLOSECOLOR}")
        print(e)
        print(
            f"Expected: {OPENBLUE} input.txt output.bin{CLOSECOLOR}")
        print(
            f"Got:\t  {' '.join(sys.argv[1:])}")
