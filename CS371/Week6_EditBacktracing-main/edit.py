import numpy as np

def edit(s1, s2):
    """
    An iterative, dynamic programming version of the string
    edit distance

    Parameters
    ----------
    s1: string of length M
        The first string to match
    s2: string of length N
        The second string to match
    
    Returns
    -------
    cost: int
        The cost of an optimal match
    paths: list of lists
        Each list 
    """
    M = len(s1)
    N = len(s2)
    # Create a 2D array with M+1 rows and N+1 columns
    # to store the costs
    table = np.zeros((M+1, N+1))
    # Fill in the base cases
    table[0, :] = np.arange(N+1)
    table[:, 0] = np.arange(M+1)

    # Make 2D array that stores the optimal moves
    moves = []
    for i in range(M+1):
        moves.append([])
        for j in range(N+1):
            moves[i].append([0])
    # Fill in the base cases
    for j in range(N):
        moves[0][j] = 1 # Move left if we're at the top row
    for i in range(M):
        moves[i][0] = 2 # Move up if we're at the left column
    
    # Do the dynamic programming to fill in the table and moves
    for i in range(1, M+1):
        for j in range(1, N+1):
            cost1 = table[i, j-1] + 1 # Delete the last character from s2
            cost2 = table[i-1, j] + 1 # Delete the last character from s1
            cost3 = table[i-1, j-1] # Match or swap both characters at the end
            if s1[i-1] != s2[j-1]:
                cost3 += 1
            table[i][j] = min(cost1, cost2, cost3)
            moves[i][j] = np.argmin(np.array([cost1, cost2, cost3]))+1
    cost = int(table[-1, -1])

    ## TODO: Extract an optimal sequence of moves.
    ## Backtrace from i = M, j = N, following the arrows, until you get to [0, 0]
    row = M
    column = N
    listOfMoves = []
    while row != 0 and column != 0:
        listOfMoves.append([row, column])
        x = moves[row][column]
        print(x, row, column)
        if x == 3:
            row-=1
            column-=1
        elif x == 2:
            column-=1
        else:
            row-=1
    listOfMoves.append([row, column])
        
    print(listOfMoves)
    return cost

print("Cost = ", edit("school", "fools"))