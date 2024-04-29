import numpy as np
import math

def RoundNum(a, b):
    return int(a/b)*b

class HuffmanTree:
    def __init__(self, alpha = 'S', value = -1):
        self.left = None
        self.right = None
        self.value = value
        self.alpha = alpha

    def insert(self, A, val):
        if(self.value == -1):
            self.value = val
            self.alpha = A
            return
        
        if(self.left == None):
            if(val < self.value):
                self.left = HuffmanTree(alpha = A, value = val)
                self.right = HuffmanTree(alpha = self.alpha, value = self.value)
            else:
                self.left = HuffmanTree(alpha = self.alpha, value = self.value)
                self.right = HuffmanTree(alpha = A, value = val)
            self.value = self.left.value + self.right.value
            return
            
        if(self.left.value < self.right.value):
            self.left.insert(A, val)
            self.value = self.left.value + self.right.value
            return
        else:
            self.right.insert(A, val)
            self.value = self.left.value + self.right.value
            return

    def insertDict(self, dict):
        dict = {k:v for  k, v in sorted(dict.items(), key=lambda item: -item[1])}
        for k, v in dict.items():
            self.insert(k, v)
    
    def printRecur(self):
        if(self.left == None):
            return [[b'', self.alpha]]
        strL = [[b'0'+x[0], x[1]] for x in self.left.printRecur()]
        strR = [[b'1'+x[0], x[1]] for x in self.right.printRecur()]
        return strR + strL
    
    def dict(self):
        Out = self.printRecur()
        return {k:v for [v, k] in Out}
        
    def print(self):
        print(self.printRecur())

class QuantizationTablePreprocess:
    def __init__(self, quant):
        self.quant = quant
        self.quant_pre = np.zeros((2, 8, 8, 8, 8))

        #forward
        for i in range(8):
            for j in range(8):
                for x in range(8):
                    for y in range(8):
                        self.quant_pre[0, i, j, x, y] = math.cos(((2 * x) + 1) * i * math.pi / 16) * math.cos(((2 * y) + 1) * j * math.pi / 16)
                        self.quant_pre[0, i, j, x, y] /= self.quant[i, j]
        
                        if(i == 0):
                            self.quant_pre[0, i, j, x, y] /= math.sqrt(2)
                        if(j == 0):
                            self.quant_pre[0, i, j, x, y] /= math.sqrt(2)

        #inverse
        for i in range(8):
            for j in range(8):
                for x in range(8):
                    for y in range(8):
                        self.quant_pre[1, x, y, i, j] = math.cos(((2 * x) + 1) * i * math.pi / 16) * math.cos(((2 * y) + 1) * j * math.pi / 16)
                        self.quant_pre[1, x, y, i, j] *= self.quant[i, j]
                        if(i == 0):
                            self.quant_pre[1, x, y, i, j] /= math.sqrt(2)
                        if(j == 0):
                            self.quant_pre[1, x, y, i, j] /= math.sqrt(2)

        self.quant_pre /= 4
                            