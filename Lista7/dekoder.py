from functools import reduce
from colors import *
import sys
import os


available_codes = [
    '00000000',
    '11010010',
    '01010101',
    '10000111',
    '10011001',
    '01001011',
    '11001100',
    '00011110',
    '11100001',
    '00110011',
    '10110100',
    '01100110',
    '01111000',
    '10101010',
    '00101101',
    '11111111',
]


def run(input_filename, output_filename):
    with open(input_filename, "rb") as f:
        bits = f.read()
        bits = decode(bits)
        with open(output_filename, "w", encoding="utf-8") as out:
            counter = 0
            while len(bits) >= 8:
                counter += 1
                bitstring = bits[:8]
                value = chr(int(bitstring, 2))
                out.write(value)
                bits = bits[8:]


def decode(text):
    bits = ""
    for character in text:
        bitstring = bin(character)[2:].rjust(8, '0')
        bits += bitstring

    result = ""
    error_count = 0
    while len(bits) >= 8:
        process = bits[:8]
        decoded, error = get_encoded(process)
        if error:
            error_count += 1
        result += decoded

        bits = bits[8:]
    print(f"Total of {error_count} errors.")

    return result


def get_encoded(bits):
    result = "0000"

    for code in available_codes:
        diffs = 0
        for index, value in enumerate(code):
            if value != bits[index]:
                diffs += 1

        if diffs == 0:
            return (bits[2] + bits[4:7], False)
        elif diffs == 1:  # correctable
            return (code[2] + code[4:7], False)

    return (result, True)


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
            f"Expected: {OPENBLUE}input.bin output.txt{CLOSECOLOR}")
        print(
            f"Got:\t  {' '.join(sys.argv[1:])}")
