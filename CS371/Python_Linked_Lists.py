#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  3 13:39:38 2021

@author: ben
"""

class Node:
    def __init__(self, value):
        self.value = value
        self.next = None # Python's version of "null" is "None"
        self.previous = None

class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.N = 0
    
    def add(self, value):
        """
        Parameters
        ----------
        value: any
            Add a new node to the beginning with this value
        """
        new_node = Node(value)
        head_before = self.head
        self.head = new_node
        new_node.next = head_before
        if new_node.next == None:
            self.tail = new_node
        self.N += 1
    
    def add_last(self, value):
        new_node = Node(value)
        self.tail.next = new_node
        self.tail = new_node
        self.N += 1
        """new_node = Node(value)
        node = self.head
        while node.next: # As long as node.next is not None
            node = node.next
        node.next = new_node
        self.tail = new_node
        self.N += 1"""
    
    def remove_first(self):
        """
        Remove and return the first value from the linked list
        or do nothing and return None if it's already empty
        """
        ret = None
        if self.head: # If the head is not None
            ret = self.head.value
            self.head = self.head.next
            self.N -= 1
        return ret
    
    """def remove_last(self):"""
        
        
    def __str__(self):
        # This is like the to-string method
        s = "LinkedList: "
        node = self.head
        while node: #As long as the node is not None
            s += "{} ==> ".format(node.value)
            node = node.next
        return s
    
    def __len__(self):
        # This allows us to use len() on our object to get its length!
        return self.N
    
    def get_tail(self):
        return self.tail
    
if __name__ == '__main__':
    L = LinkedList()
    L.add(10)
    L.add(4)
    L.add("chris")
    L.add_last("layla")
    L.add_last("theo")
    print(L)
    print(len(L))
    print(L.remove_first())
    print(L)
    print(len(L)) 