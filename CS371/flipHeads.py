#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 23 12:49:50 2021
Calculating how many coin flips it will take to get 10 heads in a row
@author: ben
"""
import numpy as np
import matplotlib.pyplot as plt
import random

"""
#You'll get the same result everytime with a seed

np.random.seed(0)

for i in range (20):
    if np.random.randint(2) == 1:
        print("H", end='')
    else:
        print("T", end='')
"""

for i in range(num_trials):
    numFlips = 0
    numHeads = 0
    
    while numHeads < 10:
        numFlips += 1
        if random.choice(['heads', 'tails']) == 'heads':
            numHeads += 1
        else:
            numHeads = 0;
    trials[i] = numFlips
print(numFlips)
"""