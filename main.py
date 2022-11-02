import numpy as np

class Tableu:

    def __init__(self):
        self.c = []
        self.A = []
        self.b = []

# Queremos saber a coluna que vai entrar na base e que linha dessa coluna vai ser pivoteada, ademais, checamos para verificar a pl não é ilimitada
def findPivot(A, b, c):
    N = A.shape[0]
    M = A.shape[1]
    pivotColum = -1000
    pivotLine = -1000
    ilimitada = False
    for i in range(0, M):  # Passando por cada coluna
        if(c[i] < 0):  # Esse valor pode ser pivoteado
            if(np.all(A[:, i] <= 0)):  # Se todas as linhas da coluna i são negativos ou iguais à zero
                ilimitada = True
                break
            minValue = 1000
            for j in range(0, N):  # Passando por cada linha
                if(A[j][i] > 0):
                    valueLine = b[j] / A[j][i]
                if(valueLine < minValue):
                    minValue = valueLine
            pivotColum = i
            pivotLine = j
            break

    return pivotColum, pivotLine, ilimitada

def canonizeTableu(A, b, c, pivotColum, pivotLine):
    N = A.shape[0]
    M = A.shape[1]

    if (A[pivotLine][pivotColum] != 1):
        A[pivotLine, :] /= A[pivotLine][pivotColum]
        b[pivotLine] /= A[pivotLine][pivotColum]
    
    for i in range(0, N):  # Para cada linha
        if (i != pivotLine and A[i][pivotColum] != 0):
            operation = A[i][pivotColum] * A[pivotLine, :]
            A[i, :] -= operation
            b[i] -= (b[pivotLine] * A[i][pivotColum])

    if(c[pivotColum] != 0):
        operation = A[pivotLine, :] * c[pivotColum]
        c -= operation

    return A, b, c

def isPivot(column):
    M = column.shape[i]
    onlyOne = False
    isPivot = False
    columnPivot = 0
    for i range(0, M):
        if (column[i] != 0 or column[i] != 1):
            return False, 0
        else:
            if(column[i] == 1):
                if (!onlyOne):
                    onlyOne = True
                    columnPivot = i
                else:
                    return False, 0
    isPivot = True
    return isPivot, columnPivot

def findX(A, c, b):
    N = A.shape[0]
    M = A.shape[1]
    x = np.zeros(len(c) - N)
    for i in range(0, len(c) - N): 
        isAPovotColumn, pivotLine = isPivot(A[:, i])
        if(c[i] == 0 and isAPivotColumn):
            solution[i] = b[pivotLine]

    return x