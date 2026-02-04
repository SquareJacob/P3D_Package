import numpy as np
import P3D.graphing as p3g

x = np.linspace(0, 1, 101)
X, Y = np.meshgrid(x, x, indexing='ij')

fig = p3g.Figure(data = [p3g.Surface(X, Y, X + Y)])
n = 101 # Number of slider steps
S = np.round(np.linspace(0, 1, n), 4) #all s values for sliders, Round this so it looks nice on slider

def RREF(Ab):
    Ab = Ab.copy() #Make copy so that actual input is not modified
    p = 0 #Current column that we are looking for pivot in
    N = Ab.shape[1] - 1 #Last column to look for pivots in; don't want pivots in b column
    # Loop to put into REF
    for i in range(min(Ab.shape[0], N)): #Loop through smaller dimension
        while Ab[i, p] == 0: #pivot can't be 0
            m = np.nonzero(Ab[i:, p])[0] #Find first nonzero below this
            if len(m) == 0: #If there is no nonzero below this-
                p += 1 #-then move onto next column
                if p >= N: #If that was last column, then we are in REF
                    break
                continue # Repeat this process on this next column
            m = m[0] + i # Get the first nonzero. Add i since thats what we started in np.nonzero
            Ab[[i, m], :] = Ab[[m, i], :] #Switch rows
        if p >= N: #If beyond last column, then we are in REF
            break
        Ab[i, p:] /= Ab[i, p] # Make pivot equal to 1
        for j in range(i + 1, Ab.shape[0]): # Set everything below pivot to 0
            Ab[j, p:] -= Ab[j, i] * Ab[i, p:] # Everything before pivot is already 0
    # Put into RREF, top to bottom
    for i in range(1, Ab.shape[0]): # First row has nothing above it; skip
        p = np.nonzero(Ab[i, :-1])[0] # First nonzero is pivot
        if(len(p) == 0): #This row has no pivots, and thus no row below this will either
            break
        p = p[0] #Get first nonzero
        for j in range(0, i): #Make everything above pivot 0
            Ab[j, p:] -= Ab[j, p] * Ab[i, p:] # Everything before pivot is already 0
    return Ab

Ab = np.array([
    [1, 1, -1, 0],
    [0, 1, -1, -1]
], dtype = np.float64) #this makes sure the matrix is not integers
slider_traces = []

for s in S: #Loop through each s value
    Ab[1, 0] = -s #Change Ab to reflect this s value
    rref = RREF(Ab)
    c = [np.nonzero(rref[i, :])[0][0] for i in range(rref.shape[0])] #Get pivot columns
    if 0 not in c: #x is free variable
        x = np.linspace(0, 1, 101)
        y = np.ones_like(x) * rref[0, -1]
        z = np.ones_like(x) * rref[1, -1]
    elif 1 not in c: #y is free variable
        y = np.linspace(0, 1, 101)
        x = rref[0, -1] - rref[0, 1] * y
        z = np.ones_like(x) * rref[1, -1]
    else: #z is free variable
        z = np.linspace(-1, 3, 101)
        x = rref[0, -1] - rref[0, 2] * z
        y = rref[1, -1] - rref[1, 2] * z
    slider_traces.append([p3g.Surface(X, Y, 1 - s * X + Y), p3g.Line(x, y, z, line = dict(width = 10))])

fig.add_slider(S, slider_traces)
fig.update_bounds([1, 0], [1, 0], [-1, 3])
fig.show()