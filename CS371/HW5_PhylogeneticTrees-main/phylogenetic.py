import numpy as np
import matplotlib.pyplot as plt
import json
from unionfind import *
import random
from collections import deque




class TreeNode(object):
    """
    Attributes
    ----------
    left: TreeNode
        Left child
    right: TreeNode
        Right child
    sim: int
        Phylogenetic similarity between two children if
        internal node, or max similarity between any two
        nodes if leaf node
    key: string
        Name of species if leaf node
    """

    def __init__(self, param):
        """
        Initialize a tree node

        Parameters
        ----------
        param: string or int
            If string, this is a leaf node with the name of a species
            If int, then this is an internal node with a particular
            height in the phylogenetic tree
        """
        self.sim = 0
        self.key = None
        if type(param) is str:
            self.key = param
        else:
            self.sim = param
        self.left = None
        self.right = None
    
    def __str__(self):
        """
        String is key if key is not None, or blank otherwise
        """
        ret = ""
        if self.key:
            ret = "{}".format(self.key)
        return ret

    def compute_y_coords(self, maxsim=[0], y=[0]):
        """
        Recursively compute y coordinate of nodes via an inorder
        traversal, while computing the maximum phylogenetic 
        similarity as a side effect

        Parameters
        ----------
        maxsim: list of [int]
            Maximum similarity
        y: list of [int]
            Current y coordinate
        """
        #Left
        if self.left:
            self.left.compute_y_coords(maxsim, y)
        #Root
        maxsim[0] = max(maxsim[0], self.sim)
        self.y = y[0]
        y[0] += 1
        #Right
        if self.right:
            self.right.compute_y_coords(maxsim, y)


    def compute_y_coordsPost(self, maxsim=[0], y=[0]):
        """
        Recursively compute y coordinate of nodes via an postorder
        traversal, while computing the maximum phylogenetic 
        similarity as a side effect

        Parameters
        ----------
        maxsim: list of [int]
            Maximum similarity
        y: list of [int]
            Current y coordinate
        """
        #Root
        maxsim[0] = max(maxsim[0], self.sim)
        self.y = y[0]
        y[0] += 1
        #Right
        y[0]-=1
        if self.right:
            self.right.compute_y_coordsPost(maxsim, y)
        y[0]+=2
        #Left
        if self.left:
            self.left.compute_y_coordsPost(maxsim, y)
        
        
    def compute_x_coords(self, maxsim):
        """
        Recursively compute and store the x coordinates
        of all nodes.  If the nodes are internal, then the
        x coordinate is the phylogenetic similarity.
        If the node is a leaf node, then the x coordinate
        is the maximum phylogenetic similarity among all
        internal nodes

        Parameters
        ----------
        maxsim: int
            Maximum phylogenetic similarity across all nodes
        """
        if self.left:
            self.left.compute_x_coords(maxsim)
        if self.right:
            self.right.compute_x_coords(maxsim)
        if self.key:
            self.x = maxsim
        else:
            self.x = self.sim
            
    

    def draw(self):
        """
        Recursively draw phylogenetic tree.  Assumes that the
        x and y coordinates have been precomputed
        """
        x1, y1 = self.x, self.y
        # Draw a dot
        plt.scatter(x1, y1, 50, 'k')
        # Draw some text indicating what the key is
        plt.text(x1+10, y1, "{}".format(self))
        if self.left:
            # Draw a line segment from my node to this left child
            x2, y2 = self.left.x, self.left.y
            plt.plot([x1, x2], [y1, y2])
            self.left.draw()
        if self.right:
            # Draw a line segment from my node to this right child
            x2, y2 = self.right.x, self.right.y
            plt.plot([x1, x2], [y1, y2])
            self.right.draw()

class PhyloTree(object):
    def __init__(self):
        self.root = None

    def draw(self, threshold=None):
        """
        Draw the phylogenetic tree from the bottom up

        Parameters
        ----------
        threshold: int
            If specified, draw a vertical line showing a similarity
            threshold for clustering
        """
        if self.root:
            maxsim = [0]
            self.root.compute_y_coords(maxsim)
            self.root.compute_x_coords(maxsim[0])
            self.root.draw()
            ax = plt.gca()
            xlim = ax.get_xlim()
            ax.set_xlim([xlim[0], xlim[1]+200])
            if threshold:
                clusters = []
                clusters = (self.getClusters(threshold, clusters))
                self.printClusters(clusters)
                ylim = ax.get_ylim()
                plt.plot([threshold, threshold], [ylim[0], ylim[1]], 'k', linestyle='--', linewidth=3)
                plt.title("Similarity Threshold = {}".format(threshold))
            ax.set_yticks([])
            plt.xlabel("Needleman-Wunsch Similarity")
            plt.tight_layout()
            
            
    def getClusters(self, thresh, clusters):
        """
        

        Parameters
        ----------
        thresh : Choosen threshold.

        Returns
        -------
        clusters : List of cluster lists.

        """
        if self.root.key:
            clusters.append((sorted(self.searchSubTrees(self.root).split("  "))))
        elif self.root.sim >= thresh:
            clusters.append((sorted(self.searchSubTrees(self.root).split("  "))))
        else:
            t = PhyloTree()
            t.root = self.root.right
            t.getClusters(thresh, clusters)
            t.root = self.root.left
            t.getClusters(thresh, clusters)
        return clusters
    def searchSubTrees(self, node):
        """
        

        Parameters
        ----------

        Returns
        -------
        ret : List of cluster lists.

        """
        if node.key:
            return node.key
        else:
            return self.searchSubTrees(node.right)+ "  " +self.searchSubTrees(node.left)
            
    
    def printClusters(self, clusters):
        for cluster in clusters:
            print(len(cluster), cluster)
    
    
def load_blosum(filename):
    """
    Load in a BLOSUM scoring matrix for Needleman-Wunsch

    Parameters
    ----------
    filename: string
        Path to BLOSUM file
    
    Returns
    -------
    A dictionary of {string: int}
        Key is string, value is score for that particular 
        matching/substitution/deletion
    """
    fin = open(filename)
    lines = [l for l in fin.readlines() if l[0] != "#"]
    fin.close()
    symbols = lines[0].split()
    X = [[int(x) for x in l.split()] for l in lines[1::]]
    X = np.array(X, dtype=int)
    N = X.shape[0]
    costs = {}
    for i in range(N-1):
        for j in range(i, N):
            c = X[i, j]
            if j == N-1:
                costs[symbols[i]] = c
            else:
                costs[symbols[i]+symbols[j]] = c
                costs[symbols[j]+symbols[i]] = c
    return costs





def Needleman(s1, s2, costs):
    N = len(s1)
    M = len(s2)
    S = np.zeros((N+1, M+1))
    #print(N, M, S.shape)
    
    total = 0
    for i in range(len(s1)+1):
        if i != 0:
            S[i, 0] = total + costs[s1[i-1]]
            total = S[i, 0]
    total = 0
    for i in range(len(s2)+1):
        if i != 0:
            S[0, i] = total + costs[s2[i-1]]
            total = S[0, i]
    for i in range(1, len(s1)+1):
        for j in range(1, len(s2)+1):
            choices = []
            choices.append((S[i-1, j-1]+costs[s1[i-1]+s2[j-1]]))
            choices.append((S[i, j-1]+costs[s2[j-1]]))
            choices.append((S[i-1, j]+costs[s1[i-1]]))
            S[i, j] = choices[np.argmax(choices)]
    #print(S)
    return S[N, M]

def All_Pairs_Needleman_Wunsch():
    costs = load_blosum("blosum62.bla")
    species = json.load(open("organisms.json"))
    table = {}
    for animal1 in species:
        for animal2 in species:
            if animal1 is not animal2:
                animals = sorted((animal1, animal2))
                key = animals[0]+"|"+animals[1]
                
                if key not in table:
                    print(key)
                    table[key] = Needleman(species[animal1], species[animal2], costs)
    json.dump({"table":table}, open("table.json", "w"))
                

'''All_Pairs_Needleman_Wunsch()

costs = load_blosum("blosum62.bla")
species = json.load(open("organisms.json"))


print(Needleman(species["Domestic Yak"], species["Wild boar"], costs))

costs = {"a":-1, "b":-2, "ab":-3, "ba":-3, "aa":2, "bb":3}
s1 = "babaab"
s2 = "ababab"
print(Needleman(s1, s2, costs))'''





def get_spanning_tree():
    species = json.load(open("organisms.json"))
    nodes = []
    names = {}
    #Create a node for each species (store in nodes)
    ctr = 0
    for each in species:
        nodes.append(TreeNode(each))
        names[each] = ctr
        ctr+=1
    
    #create a Union Find structure
    djset = UFFast(len(nodes))
    roots = []
    #set the roots of each of the components to the leaf nodes
    for x in range(len(nodes)):
        roots.append(nodes[x])
    #Load/Compute all pairwise similarities
    table = json.load(open("table.json"))['table']
    #sort pairs
    sort = []
    for pair in table:
        sort.append((pair, table[pair]))
    sort.sort(key = lambda sort: sort[1], reverse=True)
    sortedTable = sort
    #list of the animal pairs as indexes in Nodes
    pairs = []
    for each in sortedTable:
        both = each[0].split("|")
        animal1 = names[both[0]]
        animal2 = names[both[1]]
        pairs.append(((animal1, animal2), each[1]))
    
    #For each pair compare roots
    for pair in pairs:
        if not djset.find(pair[0][0], pair[0][1]):
            newnode = TreeNode(pair[1])
            newnode.left = roots[djset.root(pair[0][0])]
            newnode.right = roots[djset.root(pair[0][1])]
            
            
            djset.union(pair[0][0], pair[0][1])
            nodes.append(newnode)
            
            roots[djset.root(pair[0][1])] = newnode
    
    T = PhyloTree()
    T.root = nodes[len(nodes)-1]
    plt.figure(figsize=(10, 14)) # This makes the figure tall enough to show all animals
    plt.title("Original")
    T.draw()
    shuffleTree(T)
    
def shuffleTree():
    species = json.load(open("organisms.json"))
    nodes = []
    names = {}
    #Create a node for each species (store in nodes)
    ctr = 0
    for each in species:
        nodes.append(TreeNode(each))
        names[each] = ctr
        ctr+=1
    
    #create a Union Find structure
    djset = UFFast(len(nodes))
    roots = []
    #set the roots of each of the components to the leaf nodes
    for x in range(len(nodes)):
        roots.append(nodes[x])
    #Load/Compute all pairwise similarities
    table = json.load(open("table.json"))['table']
    #sort pairs
    sort = []
    for pair in table:
        sort.append((pair, table[pair]))
    sort.sort(key = lambda sort: sort[1], reverse=True)
    sortedTable = sort
    #list of the animal pairs as indexes in Nodes
    pairs = []
    for each in sortedTable:
        both = each[0].split("|")
        animal1 = names[both[0]]
        animal2 = names[both[1]]
        pairs.append(((animal1, animal2), each[1]))
    
    #For each pair compare roots
    ctr = 0
    for pair in pairs:
        if not djset.find(pair[0][0], pair[0][1]):
            newnode = TreeNode(pair[1])
            if ctr %3 == 0:
                newnode.left = roots[djset.root(pair[0][0])]
                newnode.right = roots[djset.root(pair[0][1])]
                djset.union(pair[0][0], pair[0][1])
                roots[djset.root(pair[0][1])] = newnode
            else:
                newnode.left = roots[djset.root(pair[0][1])]
                newnode.right = roots[djset.root(pair[0][0])]
                djset.union(pair[0][1], pair[0][0])
                roots[djset.root(pair[0][0])] = newnode

            
            nodes.append(newnode)
        ctr+=1
            
    
    T = PhyloTree()
    T.root = nodes[len(nodes)-1]
    plt.figure(figsize=(10, 14)) # This makes the figure tall enough to show all animals
    plt.title("Shuffled")
    T.draw()

get_spanning_tree()









