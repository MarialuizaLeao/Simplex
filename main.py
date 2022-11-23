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
        self.certificate = []
        self.vero = []
        self.optimalValue = 0
        self.baseColumns = []
        self.dimensions = (0,0)
        self.plClassification = ''

    # Queremos saber a coluna que vai entrar na base e que linha dessa coluna vai ser pivoteada, ademais, checamos para verificar a pl não é ilimitada
    def findPivot(self):
        for i in range(0, self.dimensions[1]):  # Checking every column
            ilimitada = False
            pivotColumn = i  # What column the pivot is
            pivotLine = 0  # The line of the new pivot
            if(self.c[i] < 0):  # If the value can be a pivot candidate
                aux = self.c.copy()
                aux = np.delete(aux, [i])
                if(np.all(self.A[:, i] <= 0) and (np.all(aux >= 0) or i < self.dimensions[1] - self.dimensions[0])):  # Check to se if the variable value are all negative or igual to 0
                    ilimitada = True  # The problem is unbounded so we dont continue trying to find a new pivot
                    break
                if(self.c[i] < 0):
                    minValue = 100  # Max value for the restrictions values
                    for j in range(0, self.dimensions[0]):  # Checking every line so we can find the minimum value that wil be the new pivot
                        if(self.A[j][i] != 0):
                            valueLine = self.b[j] / self.A[j][i]
                            if(valueLine < minValue and valueLine >= 0 and self.A[j][i] > 0):  # If we find a new lower value we have a new pivot
                                minValue = valueLine  # Update the minimum value
                                pivotLine = j  # Update the pivot line variable
                    break  # Found the new pivot so we can return

        return pivotColumn, pivotLine, ilimitada

    # Put all the bases in canonical form
    def canonizeTableau(self):
        for i in range(0, self.dimensions[0]):  # For every base variable
            if (self.A[i][self.baseColumns[i]] != 0):  # If the pivot for this variable is diferent than 0
                value = self.A[i][self.baseColumns[i]].copy()
                self.A[i, :] /= value  # Divide the entire line by the pivot value, so now pivot = 1
                self.b[i] /= value
                self.vero[i, :] /= value    
            for j in range(0, self.dimensions[0]):  # For each line
                if (i != j):  # If it's not the base variable line
                    value = self.A[j][self.baseColumns[i]].copy()
                    self.A[j, :] -= value * self.A[i, :]  # So we have the rest of the pivot colums = 0
                    self.b[j] -= value * self.b[i]
                    self.vero[j, :] -= value * self.vero[i, :]
            value = self.c[self.baseColumns[i]]
            self.c -= value * self.A[i, :]  # So now the variable is a real base (respective c = 0)
            self.optimalValue -= value * self.b[i]
            self.certificate -= value * self.vero[i, :]
        vfunc = np.vectorize(zero)  # Round all the zeros according to the precision 
        self.A = vfunc(self.A)
        self.c = vfunc(self.c)
        self.b = vfunc(self.b)
        self.optimalValue = vfunc(self.optimalValue)
        self.certificate = vfunc(self.certificate)
        self.vero = vfunc(self.vero)

    # Find the solution in the tableau
    def findX(self):
        x = np.zeros(self.dimensions[1] - self.dimensions[0])  # The size occording to the original number of variables in the problem
        for i in range(0, len(self.b)): 
            if(self.baseColumns[i] < self.dimensions[1] - self.dimensions[0]):  # If the base is a original variable
                x[self.baseColumns[i]] = self.b[i]

        return x

def simplex(restrictions, bVector, optimalVector, baseVariables, vero):
    tableau = Tableau()  # Initiate the tableu with the receving values
    tableau.A = restrictions.copy()
    tableau.b = bVector.copy()
    tableau.c = optimalVector * -1
    tableau.baseColumns = baseVariables.copy()
    tableau.dimensions = (restrictions.shape[0], restrictions.shape[1])
    tableau.optimalValue = 0
    tableau.certificate = np.zeros(tableau.dimensions[0])
    tableau.vero = vero.copy()
    tableau.canonizeTableau()  # Make sure that all the bases columns really have pivots
    while(np.any(tableau.c < 0)):  # While c still have negative values
        pivotColumn, pivotLine, ilimitada = tableau.findPivot()  # Find the variable that will enter the base
        if (ilimitada):  # If we find that the problem is unbounded
            tableau.plClassification = 'ilimitada'
            solution = tableau.findX()  # Find the solution that we have in the moment
            return tableau.certificate, tableau.optimalValue, solution, tableau.plClassification, tableau.baseColumns
        tableau.baseColumns[pivotLine] = pivotColumn  # Add the new pivot column found to the bases list
        tableau.canonizeTableau()  # Put the tableau in canonical form for the new base value
    solution = tableau.findX()  # Find the tableau's solution
    if(tableau.optimalValue < 0):  # If the optimal value is negative, the problem is unsolvable
        tableau.plClassification = 'inviavel'
    else:
        tableau.plClassification = 'otima'
        
    return tableau.certificate, tableau.optimalValue, solution, tableau.plClassification, tableau.baseColumns

# Return the auxiliar pl
def auxiliarPl(originalA, originalB):
    auxiliarA = originalA.copy()
    auxiliarB = originalB.copy()
    auxiliarA = np.concatenate((auxiliarA, np.eye(originalA.shape[0], dtype = float)), axis = 1)  # Add the matrix
    auxiliarC = np.concatenate((np.zeros(originalA.shape[1]), np.full(originalA.shape[0], -1)))  # Put all the original's variables c's as 0 and the auxiliar as -1
    auxiliarBaseVariables = list(range(originalA.shape[1], originalA.shape[0] + originalA.shape[1]))  # New base as the auxiliar matrix columns
    
    return auxiliarA, auxiliarB, auxiliarC, auxiliarBaseVariables

def printArray(array):
    for i in range(len(array)):
        print('{:.7f}'.format(array[i]), end=' ')
    print()

N, M = input().split()
N = int(N)  # Number of restrictions
M = int(M)  # Number of variables

cInput = input().split()
optimalVectorInput = np.array(cInput, dtype = float)

restrictionsInput = []
for i in range(0, N):
    restrictionsInput.append(input().split())
restrictionsInput = np.array(restrictionsInput, dtype = float)
compensatingVariables = np.eye(N, dtype = float)
veroMatrix = np.eye(N, dtype = float)

baseInput = np.array(restrictionsInput[:, -1])  # b vector

if(np.array_equal(restrictionsInput[:, (N - 1):-1], compensatingVariables)):  # If the original problem already has a base
    baseVariablesInput = list(range(M - N, M))  # The bases are the compensating variables
else: 
    baseVariablesInput = list(range(M, M + N))  # The bases are the compensating variables

restrictionsInput = np.concatenate((np.array(restrictionsInput[:, :-1]), compensatingVariables), axis = 1)
optimalVectorInput = np.concatenate((np.array(cInput, dtype = float), np.zeros(N)))  # Optimal value for compensating variables

bNegativo = False

if(np.any(baseInput < 0)):  # Check to see if any b value is negative
    bNegativo = True  # If a value is negative we multiply the entire line by -1
    for i in range(0, N):
        if(baseInput[i] < 0):
            baseInput[i] *= -1
            restrictionsInput[i][:] *= -1
            veroMatrix[i][:] *= -1

auxiliarA, auxiliarB, auxiliarC, auxiliarBaseVariables = auxiliarPl(restrictionsInput, baseInput)  # Create the auliar matrix for the problem

auxiliarCertificate, auxiliarOptimalValue, auxiliarSolution, auxiliarPlClassification, auxiliarFinalBaseVariables = simplex(auxiliarA, auxiliarB, auxiliarC, auxiliarBaseVariables, veroMatrix.copy())  # Solve the auxiliar problem

if(auxiliarOptimalValue < 0):  # If auxiliar's optimal value is negative, then the problem is unsolvable
    print(auxiliarPlClassification)
    printArray(auxiliarCertificate)
else:
    if(bNegativo):  # If the original problem had negative b values, we'll use the base variables found by the auxiliar matrix
        auxiliarFinalBaseVariables.sort()
        auxiliarFinalBaseVariables = auxiliarFinalBaseVariables[:N + M]
        for i in range(len(auxiliarFinalBaseVariables)):
            if(auxiliarFinalBaseVariables[i] > M + N):
                auxiliarFinalBaseVariables[i] = auxiliarFinalBaseVariables[i] - (M + N)
        baseVariablesInput = auxiliarFinalBaseVariables
    FinalCertificate, FinalOptimalValue, FinalSolution, FinalPlClassification, FinalFinalBaseVariables = simplex(restrictionsInput, baseInput, optimalVectorInput, baseVariablesInput, veroMatrix)  # Solve the original problem
    vfunc = np.vectorize(zero)
    solution = vfunc(FinalSolution)
    optimalValue = vfunc(FinalOptimalValue)
    print(FinalPlClassification)
    if(FinalPlClassification == 'ilimitada'):  # If unbounded, print only the result
        printArray(FinalSolution)
    if(FinalPlClassification == 'otima'):  # In this case, print optimal value and result
        print('{:.7f}'.format(FinalOptimalValue))
        printArray(FinalSolution)
        printArray(FinalCertificate)
        