import numpy as np


class RNG:

    @staticmethod
    def makeNumbers():
        f = open("Logxy.txt", "r")
        string = (f.read())
        string = string.replace("0b", "")
        n = 8
        split_string = [string[i:i + n] for i in range(0, len(string), n)]
        split_string = np.uint8(split_string)
        return split_string[0:len(split_string) - 2]

    def getNextRandom(self, R):
        rands = b''
        while len(rands) < R:
            self.iterator += 1
            if self.iterator == len(self.random):
                self.iterator = 0
            rands += self.random[self.iterator]

        return rands

    def __init__(self):
        self.iterator = -1
        self.random = self.makeNumbers()
