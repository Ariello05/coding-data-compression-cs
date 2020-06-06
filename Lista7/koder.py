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
    with open(input_filename, "r") as f:
        bits = f.read()
        bits = encode(bits)
        with open(output_filename, "w") as out:
            out.write(bits)


def encode(bits):
    result = ""

    while len(bits) >= 4:
        process = bits[:4]
        result += str(get_encoded(process))
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
            f"Expected: {OPENBLUE} input output{CLOSECOLOR}")
        print(
            f"Got:\t  {' '.join(sys.argv[1:])}")
