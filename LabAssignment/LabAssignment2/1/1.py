import numpy as np
#create 1d array from 2 to 26
M = np.arange(2,27)
print(M)
print("\n")

#reshape as a 5x5
M=  M.reshape(5,5)
print(M)
print("\n")

#set value of inner elements of matrix to 0
M[1:4,1:4] = 0
print(M)
print("\n")

#M^2
M= M@M
print(M)
print("\n")

#magnitude of vector v  v: v is first row of the matrix M
M = M[0,]
M = np.sqrt(M@M)
print(M)

