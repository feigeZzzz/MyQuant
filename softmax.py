#!/usr/bin/env.python
import numpy as np
import math

def softmax(maxarray: np.array):
    m, n = maxarray.shape
    returnArray = np.zeros((m, n))
    for i in range(m):
        returnArray[i, :] = np.exp(maxarray[i, :]) / np.exp(maxarray[i, :]).sum()
    return returnArray

if __name__ == '__main__':
    end = softmax(np.array([[1,2,3,4],
                      [5,5,6,7]]))
    print(end)