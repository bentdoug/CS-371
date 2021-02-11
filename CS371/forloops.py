#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 23 12:57:27 2021
Practice with Pythonic for loops!
@author: ben
"""

#the itterable (thing you can itterate through) that we will use
arr = [3, 7, 1, 4, 7, 2]

#The "Java Way"
for i in range(len(arr)):
    print(i, arr[i])
    #will print the index and the contents of the
    #array at this index
    
# The "Pythonic way" - works with other collections
# Like sets and maps
for i, x in enumerate(arr):
    print(i, x)
    
# Ex) Average every other element in arr
avg = 0
#Don't need indices:  General pattern: For element
# in collection, do something with element
for x in arr[0::2]:
    print(x, end = ' ')
    avg += x
print("Avg = ", avg/len(arr[0::2]))