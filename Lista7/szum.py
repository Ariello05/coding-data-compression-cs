from functools import reduce
from colors import *
import sys
import os
import random



def run(p, input_filename, output_filename):
    with open(input_filename, "rb") as f:
        bits = f.read()
        bytes_ = tore(p, bits)
        with open(output_filename, "wb") as out:
            for byte in bytes_:
                out.write(byte)


def tore(p, text):
    result = []
    for char in text:
        bitstring = bin(char)[2:].rjust(8, '0')
        proccess = ""
        for bit in bitstring:
            if random.random() < p:
                if bit == "1":
                    proccess += "0"
                else:
                    proccess += "1"
            else:
                proccess += bit

        num = int(proccess, 2)
        byte = num.to_bytes(1, byteorder="big")
        result.append(byte)

    return result


if __name__ == '__main__':

    try:
        if len(sys.argv) < 3:
            raise Exception('')
        else:
            p = float(sys.argv[1])
            input_ = sys.argv[2]
            output_ = sys.argv[3]
            run(p, input_, output_)

            print(f"{OPENGREEN}SUCCESS{CLOSECOLOR}")
    except Exception as e:
        print(f"{OPENRED}FAILURE{CLOSECOLOR}")
        print(e)
        print(
            f"Expected: {OPENBLUE} p input.bin output.bin{CLOSECOLOR}\n where p is between [0.0,1.0]")
        print(
            f"Got:\t  {' '.join(sys.argv[1:])}")
