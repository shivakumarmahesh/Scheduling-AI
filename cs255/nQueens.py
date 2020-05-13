import numpy as np
global N
N = 4

def printSolution(board): 
    for i in range(N): 
        for j in range(N): 
            print (board[i][j], end = " ") 
        print() 

def isSafe(board, row, col):

    #Check this row on the left.
    for i in range(col):
        if board[row][i] == 1:
            return False
    #Check upper diagonal on the left side.
    for i,j in zip(range(row, -1, -1),
                   range(col, -1, -1)):
        if board[i][j] == 1:
            return False
    #Check lower diagonal on the left side.
    for i,j in zip(range(row, 1, N),
                   range(col, -1, -1)):
        if board[i][j] == 1:
            return False
    
    return True

def solveNQueenUtil(board, col):
    #If all queens are placed return true
    if col >= N:
        return True
    #Consider this column and try placing this queen in each row one by one
    for i in range(N):
        #Place queen in this square
        if isSafe(board, i, col):
            board[i][col] = 1
            #recur to place the rest of the queens
            if solveNQueenUtil(board, col + 1):
                return True
            #If there is no solution then remove the queen from board[i][col]
            board[i][col] = 0 #This enables backtracking

    #If no queens can be placed in any rows of this column then return False
    return False

def nQueens(): 
    board = [ [0, 0, 0, 0], 
              [0, 0, 0, 0], 
              [0, 0, 0, 0], 
              [0, 0, 0, 0] ] 
  
    if solveNQueenUtil(board, 0) == False: 
        print ("Solution does not exist") 
        return False
  
    printSolution(board) 

nQueens()