from functools import reduce
from colors import *
import sys
import os


def run(input_filename, output_filename):
    with open(input_filename, "rb") as in1:
        with open(output_filename, "rb") as in2:
            in1_text = in1.read()
            in2_text = in2.read()
            compare(in1_text, in2_text)


def compare(in1, in2):
    diff_counter = 0

    for index, character1 in enumerate(in1):
        bitstring1 = bin(character1)[2:].rjust(8, '0')

        try:
            character2 = in2[index]
        except Exception:
            diff_counter += 2
            continue

        bitstring2 = bin(character2)[2:].rjust(8, '0')

        for index in range(4):
            if bitstring1[index] != bitstring2[index]:
                diff_counter += 1
                break
        for index in range(4, 8):
            if bitstring1[index] != bitstring2[index]:
                diff_counter += 1
                break

    print(f"Total of {diff_counter} differences in blocks!")


if __name__ == '__main__':

    try:
        if len(sys.argv) < 2:
            raise Exception('')
        else:
            input_1 = sys.argv[1]
            input_2 = sys.argv[2]
            run(input_1, input_2)

            print(f"{OPENGREEN}SUCCESS{CLOSECOLOR}")
    except Exception as e:
        print(f"{OPENRED}FAILURE{CLOSECOLOR}")
        print(e)
        print(
            f"Expected: {OPENBLUE}in1 in2{CLOSECOLOR}")
        print(
            f"Got:\t  {' '.join(sys.argv[1:])}")
