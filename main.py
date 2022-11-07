import numpy as np

def zero(value):
    if(abs(value) < 1e-4):
        value = 0.0
    return value

class Tableau:

    def __init__(self):
        self.c = []
        self.A = []
        self.b = []
        self.optimalValue = 0
        self.baseColumns = []
        self.dimensions = (0,0)
        self.plClassification = ''

    # Queremos saber a coluna que vai entrar na base e que linha dessa coluna vai ser pivoteada, ademais, checamos para verificar a pl não é ilimitada
    def findPivot(self):
        for i in range(0, self.dimensions[1]):  # Checking every column
            ilimitada = False
            pivotColumn = i
            pivotLine = 0
            if(self.c[i] < 0):  # Is the value can be a pivot candidade
                aux = self.c.copy()
                aux = np.delete(aux, [i])
                if(np.all(self.A[:, i] <= 0) and (np.all(aux >= 0) or i < self.dimensions[1] - self.dimensions[0])):  # Check to se if the variable value are all negative or igual to 0
                    ilimitada = True
                    break
                if(self.c[i] < 0):
                    minValue = 100  # Max value for the restrictions values
                    for j in range(0, self.dimensions[0]):  # Checking every line so we can find the minimum value that wil be the new pivot
                        if(self.A[j][i] != 0):
                            valueLine = self.b[j] / self.A[j][i]
                            if(valueLine < minValue and valueLine >= 0 and self.A[j][i] > 0):
                                minValue = valueLine
                                pivotLine = j
                    break

        return pivotColumn, pivotLine, ilimitada

    def canonizeTableau(self):
        for i in range(0, self.dimensions[0]):  # For every base variable
            
            if (self.A[i][self.baseColumns[i]] != 0):  # If the pivot for this variable is diferent than 0
                value = self.A[i][self.baseColumns[i]].copy()
                self.A[i, :] /= value  # Divide the entire line by the pivot value, so now pivot = 1
                self.b[i] /= value
            
            for j in range(0, self.dimensions[0]):  # For each line
                if (i != j):  # If it's not the base variable line
                    value = self.A[j][self.baseColumns[i]].copy()
                    self.A[j, :] -= value * self.A[i, :]  # So we have the rest of the pivot colums = 0
                    self.b[j] -= value * self.b[i]

            value = self.c[self.baseColumns[i]]
            self.c -= value * self.A[i, :]  # So now the variable is a real base (respective c = 0)
            self.optimalValue -= value * self.b[i]
    
        vfunc = np.vectorize(zero)
        self.A = vfunc(self.A)
        self.c = vfunc(self.c)
        self.b = vfunc(self.b)
        self.optimalValue = vfunc(self.optimalValue)

    def findX(self):
        x = np.zeros(self.dimensions[1] - self.dimensions[0])
        for i in range(0, len(self.b)): 
            if(self.baseColumns[i] < self.dimensions[1] - self.dimensions[0]):
                x[self.baseColumns[i]] = self.b[i]

        return x

def simplex(restrictions, bVector, optimalVector, baseVariables):
    tableau = Tableau()
    tableau.A = restrictions.copy()
    tableau.b = bVector.copy()
    tableau.c = optimalVector * -1
    tableau.baseColumns = baseVariables.copy()
    tableau.dimensions = (restrictions.shape[0], restrictions.shape[1])
    tableau.optimalValue = 0

    tableau.canonizeTableau()
    while(np.any(tableau.c < 0)):
        pivotColumn, pivotLine, ilimitada = tableau.findPivot()
        if (ilimitada):
            tableau.plClassification = 'ilimitada'
            solution = tableau.findX()
            return tableau.optimalValue, solution, tableau.plClassification, tableau.baseColumns
        tableau.baseColumns[pivotLine] = pivotColumn
        tableau.canonizeTableau()
  
    solution = tableau.findX()
    if(tableau.optimalValue < 0):
        tableau.plClassification = 'inviavel'
    else:
        tableau.plClassification = 'otima'
        
    tableau.baseColumns.sort()
    tableau.baseColumns =tableau.baseColumns[:tableau.dimensions[0]]
    return tableau.optimalValue, solution, tableau.plClassification, tableau.baseColumns

def auxiliarPl(originalA, originalB):
    auxiliarA = originalA.copy()
    auxiliarB = originalB.copy()
    auxiliarA = np.concatenate((auxiliarA, np.eye(originalA.shape[0], dtype = float)), axis = 1)
    auxiliarC = np.concatenate((np.zeros(originalA.shape[1]), np.full(originalA.shape[0], -1)))
    auxiliarBaseVariables = list(range(originalA.shape[1], originalA.shape[0] + originalA.shape[1]))
    
    return auxiliarA, auxiliarB, auxiliarC, auxiliarBaseVariables

def printArray(array):
    for i in range(len(array)):
        print('{:.7f}'.format(array[i]), end=' ')
    print()

N, M = input().split()
N = int(N)
M = int(M)

cInput = input().split()
optimalVectorInput = np.array(cInput, dtype = float)
optimalVectorInput = np.concatenate((np.array(cInput, dtype = float), np.zeros(N)))

restrictionsInput = []
for i in range(0, N):
    restrictionsInput.append(input().split())
restrictionsInput = np.array(restrictionsInput, dtype = float)
folgaVariables = np.eye(N, dtype = float)

baseInput = np.array(restrictionsInput[:, -1])

restrictionsInput = np.concatenate((np.array(restrictionsInput[:, :-1]), folgaVariables), axis = 1)

baseVariablesInput = list(range(M, M + N))

bNegativo = False

if(np.any(baseInput < 0)):
    bNegativo = True
    for i in range(0, N):
        if(baseInput[i] < 0):
            baseInput[i] *= -1
            restrictionsInput[i][:] *= -1

auxiliarA, auxiliarB, auxiliarC, auxiliarBaseVariables = auxiliarPl(restrictionsInput, baseInput)

auxiliarOptimalValue, auxiliarSolution, auxiliarPlClassification, auxiliarFinalBaseVariables = simplex(auxiliarA, auxiliarB, auxiliarC, auxiliarBaseVariables)

if(auxiliarOptimalValue < 0):
    print(auxiliarPlClassification)
else:
    if(bNegativo):
        for i in range(len(auxiliarFinalBaseVariables)):
            if(auxiliarFinalBaseVariables[i] > M + N):
                auxiliarFinalBaseVariables[i] = auxiliarFinalBaseVariables[i] - (M + N)
        baseVariablesInput = auxiliarFinalBaseVariables
    else:
        baseVariablesInput = list(range(M, M + N))
    FinalOptimalValue, FinalSolution, FinalPlClassification, FinalFinalBaseVariables = simplex(restrictionsInput, baseInput, optimalVectorInput, baseVariablesInput)
    vfunc = np.vectorize(zero)
    solution = vfunc(FinalSolution)
    optimalValue = vfunc(FinalOptimalValue)
    print(FinalPlClassification)
    if(FinalPlClassification == 'ilimitada'):
        printArray(FinalSolution)
    if(FinalPlClassification == 'otima'):
        print('{:.7f}'.format(FinalOptimalValue))
        printArray(FinalSolution)