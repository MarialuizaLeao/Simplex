import numpy as np

def isPivot(column):
    M = column.shape[i]
    onlyOne = False
    isPivot = False
    columnPivot = 0
    for i in range(0, M):
        if (column[i] != 0 or column[i] != 1):
            return False, 0
        else:
            if(column[i] == 1):
                if (not onlyOne):
                    onlyOne = True
                    columnPivot = i
                else:
                    return False, 0
    isPivot = True
    return isPivot, columnPivot

class Tableu:

    def __init__(self):
        self.c = []
        self.A = []
        self.b = []

    # Queremos saber a coluna que vai entrar na base e que linha dessa coluna vai ser pivoteada, ademais, checamos para verificar a pl não é ilimitada
    def findPivot(self):
        N = self.A.shape[0]
        M = self.A.shape[1]
        pivotColumn = -1000
        pivotLine = -1000
        ilimitada = False
        for i in range(0, M):  # Passando por cada coluna
            if(self.c[i] < 0):  # Esse valor pode ser pivoteado
                if(np.all(self.A[:, i] <= 0)):  # Se todas as linhas da coluna i são negativos ou iguais à zero
                    ilimitada = True
                    break
                minValue = 1000
                for j in range(0, N):  # Passando por cada linha
                    if(self.A[j][i] > 0):
                        valueLine = self.b[j] / self.A[j][i]
                    if(valueLine < minValue):
                        minValue = valueLine
                pivotColumn = i
                pivotLine = j
                break

        return pivotColumn, pivotLine, ilimitada

    def canonizeTableu(self, pivotColum, pivotLine):
        N = self.A.shape[0]

        if (self.A[pivotLine][pivotColum] != 1):
            self.A[pivotLine, :] /= self.A[pivotLine][pivotColum]
            self.b[pivotLine] /= self.A[pivotLine][pivotColum]
        
        for i in range(0, N):  # Para cada linha
            if (i != pivotLine and self.A[i][pivotColum] != 0):
                operation = self.A[i][pivotColum] * self.A[pivotLine, :]
                self.A[i, :] -= operation
                self.b[i] -= (self.b[pivotLine] * self.A[i][pivotColum])

        if(self.c[pivotColum] != 0):
            operation = self.A[pivotLine, :] * self.c[pivotColum]
            self.c -= operation

    def findX(self):
        N = self.A.shape[0]
        M = self.A.shape[1]
        x = np.zeros(len(self.c) - N)
        for i in range(0, len(self.c) - N): 
            isAPivotColumn, pivotLine = isPivot(self.A[:, i])
            if(self.c[i] == 0 and isAPivotColumn):
                solution[i] = self.b[pivotLine]

        return x

def simplex(restrictions, base, optimalVector):
    tableu = Tableu()
    tableu.A = restrictions
    tableu.b = base
    tableu.c = optimalVector * -1
    N = tableu.A.shape[0]
    M = tableu.A.shape[1]
    while(np.any(tableu.c < 0)):
        pivotColumn, pivotLine, ilimitada = tableu.findPivot()
        if (ilimitada):
            optimalValue = 'ilimitada'
            solution = tableu.findX()
            return optimalValue, solution, tableu.b
        tableu.canonizeTableu(pivotColumn, pivotLine)
        
    solution = tableu.findX()
    optimalValue = tableu.c[-1]

    return optimalValue, solution, tableu.b


N, M = input().split()

cInput = input().split()
optimalVectorInput = np.array(cInput, dtype = float)
optimalVectorInput = np.concatenate((optimalVectorInput, np.zeros(N + 1)), axis = 1)

restrictionsInput = []
for i in range(0, N):
    restrictionsInput.append(input().split())
restrictionsInput = np.array(restrictionsInput, dtype = float)
folgaVariables = np.eye(N, dtype = float)

baseInput = np.array(restrictionsInput[:, -1])

restrictionsInput = np.concatenate((np.array(restrictionsInput[:, :-1]), folgaVariables), axis = 1)

for i in range(0, 1):
    if(baseInput[i] < 0):
        baseInput *= -1
        restrictionsInput[i] *= -1

optimalValue, solution, bVector = simplex(restrictionsInput, baseInput, optimalVectorInput)
