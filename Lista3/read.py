from bitstring import ConstBitStream
from entropy import EntropyReader
import sys


class BetterReader:

    # writes as many bytes from write_bits as it's possible
    def writeBits(self, write_bits, exit_file):
        to_write = int(write_bits[:8], 2)
        # print(write_bits[:8])
        self.out_bytes += 1
        exit_file.write(to_write.to_bytes(1, byteorder="big"))
        write_bits = write_bits[8:]
        while len(write_bits) > 8:
            to_write = int(write_bits[:8], 2)
            # print(write_bits[:8])
            self.out_bytes += 1
            exit_file.write(to_write.to_bytes(1, byteorder="big"))
            write_bits = write_bits[8:]

        return write_bits

    def encode(self, file_name, out_file_name):
        rev_dictionary = {chr(i): i for i in range(255)}

        current_value = len(rev_dictionary) + 1
        bits = 9
        threshold = 512

        buffor_bits = ''
        self.in_bytes = 0
        self.out_bytes = 0

        exit_file = open(out_file_name, "wb")
        with open(file_name, "r") as f:
            c = f.read(1)
            while True:
                if current_value == threshold:
                    threshold *= 2
                    bits += 1

                s = f.read(1)
                self.in_bytes += 1
                if not s:
                    break
                w = c + s

                if w not in rev_dictionary:
                    #print(f"1. (c,s): ({c},{s})")

                    to_write = bin(rev_dictionary.get(c))[2:]
                    to_write = to_write.rjust(bits, '0')
                    #print(f"{to_write} -1> {int(to_write,2)}")
                    buffor_bits += to_write
                    buffor_bits = self.writeBits(buffor_bits, exit_file)

                    # print(current_value)
                    rev_dictionary[w] = current_value

                    current_value += 1
                    w = w[-1]
                    c = w
                else:
                    #print(f"2. (c,s): ({c},{s})")
                    c += s

            if len(c) > 0:
                to_write = bin(rev_dictionary.get(c))[2:]
                to_write = to_write.rjust(bits, '0')
                #print(f"{to_write} -2> {int(to_write,2)}")
                buffor_bits += to_write
                self.out_bytes += 1
                buffor_bits = self.writeBits(buffor_bits, exit_file)

                if len(buffor_bits) > 0:
                    buffor_bits = buffor_bits.ljust(8, '0')
                    #print(f"{buffor_bits} -3> {int(buffor_bits,2)}")
                    to_write = int(buffor_bits, 2)
                    self.out_bytes += 1
                    exit_file.write(to_write.to_bytes(1, byteorder="big"))

        exit_file.close()

        #print(f"Entropy of in file: {entropy_in}")
        #print(f"Entropy of out file (0/1 bits): {be.entropy()}")
        # print(
        #    f"Entropy of out file (standard bytes): {dynamic_entropy.entropy()}")
        print(f"Length of in file:{self.in_bytes}")
        print(f"Length of code (bytes):{self.out_bytes}")
        er = EntropyReader(file_name)
        er2 = EntropyReader(out_file_name)
        print(f"Entropy of in file: {er.getEntropy()}")
        print(f"Entropy of out file: {er2.getEntropy()}")

        print("Compression level: {:4.2f}%".format(
            self.out_bytes/self.in_bytes * 100))

    def decode(self, file_name, out_file_name):
        f = ConstBitStream(filename=file_name)
        dictionary = {i: chr(i) for i in range(255)}

        current_value = len(dictionary) + 1
        threshold = 512
        bits = 9

        with open(out_file_name, "w", encoding="utf-8") as exit_file:
            read_bits = f.read(bits)
            value = int(str(read_bits)[2:], 2)
            #print(f"{str(read_bits)[2:]} -> {int(str(read_bits)[2:],2)}")
            c = chr(value)
            exit_file.write(c)

            while True:
                if current_value == threshold-1:
                    threshold *= 2
                    bits += 1

                try:
                    read_bits = f.read(bits)
                except:
                    return

                if not read_bits:
                    return
                #print(f"{str(read_bits)[2:]} -> {int(str(read_bits)[2:],2)}")
                value = int(str(read_bits)[2:], 2)
                #print(f"(c): ({c})")

                if value in dictionary:
                    entry = dictionary[value]
                else:
                    entry = c + c[0]
                    #raise ValueError(f'Nie ma wpisu dla value:{value}')

                exit_file.write(entry)
                # print(current_value)
                dictionary[current_value] = c + entry[0]
                current_value += 1

                c = entry


if __name__ == "__main__":
    try:
        if len(sys.argv) < 3:
            print(f"FAILURE")
            print(
                f"Expected: (-E | --encode) or (-D | --decode) input output")
            print(
                f"Got:\t  {' '.join(sys.argv[1:])}")
        else:
            in_name = sys.argv[2]
            out_name = sys.argv[3]
            hc = BetterReader()

            code_type = sys.argv[1]
            if code_type == "-E" or code_type == "--encode":
                hc.encode(in_name, out_name)
            elif code_type == "-D" or code_type == "--decode":
                hc.decode(in_name, out_name)
            else:
                print(f"In first argument expected: (-E | --encode) or (-D | --decode) ")
                print(f"Got:\t {sys.argv[1]}")

            print(f"SUCCESS")
    except:
        print(f"FAILURE")
        raise
