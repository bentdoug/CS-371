# Single list, each element is the ID of the corresponding object
class MyDisjointSet:
    def __init__(self, N):
        self.N = N
        self.parent = list(range(N))
        
    def root(self, i):
        while parent[i] != i:
            i=parent[i]
        return i
    
    def find(self, i, j):
        """
        Return true if i and j are in the same component, or
        false otherwise
        Parameters
        ----------
        i: int
            Index of first element
        j: int
            Index of second element
        """
        return root(i) == root(j)
    
    def union(self, i, j):
        """
        Merge the two sets containing i and j, or do nothing if they're
        in the same set
        Parameters
        ----------
        i: int
            Index of first element
        j: int
            Index of second element
        """
        root_i = root(i)
        root_j = root(j)
        if root_i != root_j:
            parent[root_j]