import random
import sys
import os
import math


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class SymbolPair:

    def __init__(self, symbol):
        self.__count = 0
        # if symbol == "\n":
        #    symbol = "\\n"
        self.__symbol = symbol
        self.__war = {}

    def incCount(self):
        self.__count += 1

    def addPair(self, pair):

        if pair not in self.__war:
            self.__war[pair] = 1
        else:
            self.__war[pair] += 1

    def print(self):
        # i_tab = self.__war

        print('Symbol({0}) count={1}: '.format(self.__symbol, self.__count))
        # for l in sorted(i_tab, key=i_tab.get, reverse=True):
        # sym = i_tab[l]
        # if sym[l] == "\n":
        # sym = "\\n"
        # elif sym[l] == "\0":
        # sym = "\\0"
        # print('\t\"{0}{1}\"\t'.format(l, self.__symbol), i_tab[l])

    def getCount(self):
        return self.__count

    def __lt__(self, other):
        l_val = self.__count
        r_val = other.__count
        return l_val < r_val

    def getConditionalEntropy(self):
        local = 0.0
        xcount = self.__count
        for xycount in self.__war.values():
            # prawdopodobienstwo wystapienia dwoch znakow obok siebie

            pyx = xycount/(xcount)  # uproszcony wzor
            local += pyx*(-1)*math.log2(pyx)
        return local


class DynamicEntropy:
    def __init__(self):
        self.total = 0
        self.strings = {}

    def process(self, string):
        if string not in self.strings:
            self.strings[string] = 1
        else:
            self.strings[string] += 1

        self.total += 1

    def entropy(self):
        entropy = 0.0
        for k in self.strings:
            p = self.strings[k]/self.total
            entropy += p*(-1)*math.log2(p)
        return entropy


class BinaryEntropy:
    def __init__(self):
        self.zero = 0
        self.one = 1

    def process(self, string):
        for char in string:
            if char == '0':
                self.zero += 1
            elif char == '1':
                self.one += 1
            else:
                raise TypeError("String should only take 0 and 1s")

    def entropy(self):
        total = self.zero + self.one
        p_1 = self.zero / total
        p_2 = self.one / total

        sum = p_1 * (-1)*math.log2(p_1)
        sum += p_2 * (-1)*math.log2(p_2)

        return sum


class EntropyReader:

    def __init__(self, filename, binary='y'):
        self.symbolsDictionary = {}
        self.symbolsCount = 0
        #last = "\0"

        if binary == 'Y' or binary == 'y':
            file = open(filename, "rb")
        else:
            file = open(filename, "r", encoding="utf8")

        c = file.read(1)
        file.seek(0, 0)
        if not c:
            return

        last = c

        while True:
            c = file.read(1)

            if not c:
                #print("End of file")
                break

            if c not in self.symbolsDictionary:
                self.symbolsDictionary[c] = SymbolPair(c)

            self.symbolsDictionary[c].incCount()
            self.symbolsCount += 1

            self.symbolsDictionary[c].addPair(last)
            last = c

    def getEntropy(self):
        entropy = 0.0
        for k in self.symbolsDictionary:
            p = self.symbolsDictionary[k].getCount()/self.symbolsCount
            entropy += p*(-1)*math.log2(p)
        return entropy

    def getConditionalEntropy(self):
        entropy_war = 0.0
        for k in self.symbolsDictionary:
            xcount = self.symbolsDictionary[k].getCount()
            entropy_war += xcount * \
                self.symbolsDictionary[k].getConditionalEntropy()
        return entropy_war/self.symbolsCount
