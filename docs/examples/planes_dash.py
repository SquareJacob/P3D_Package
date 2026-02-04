from dash import Dash, dash_table, dcc, Input, Output, callback
import plotly.graph_objects as go
import P3D.graphing as p3g
import P3D.webpage as p3w
import numpy as np

x = np.linspace(0, 1, 101)
X, Y = np.meshgrid(x, x, indexing='ij')
fig = p3g.Figure(data = [ # Create initial figure
    p3g.Surface(X, Y, X, name = "S1"), # What we put into z does not matter; will be changed with callback
    p3g.Surface(X, Y, X, name = "S2"),
    p3g.Line(x, x, x, line = dict(width = 10), name = "line") # All of x,y,z for line will be changed on callback                 
])
fig.update_layout(
    margin=dict(l=0, r=0, t=0, b=10)
)

#RREF function, which takes in augmented matrix Ab from Ax=b
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

app = p3w.Webpage()

app.layout = [
    p3w.Graph(fig, id='graph', height = 0.7),
    p3w.DataTable(
        id='table', height = 0.2,
        columns=['variable', 'Surface 1', 'Surface 2'],
        column_ids= {1: 'S1', 2: 'S2'},
        properties = {'editable': ['S1', 'S2']},
        data=[
            ['x slope', 1, -1],
            ['y slope', 1, 1],
            ['constant', 0, 1]
        ]
    )
]

@callback(
    Output('graph', 'figure'),
    Input('table', 'data')
)
def editTable(data):
    Ab = []
    for s in ['S1', 'S2']:
        # Z=aX+bY+C to -C=aX+bY-Z
        Ab.append([float(data[0][s]), float(data[1][s]), -1, -float(data[2][s])])
        fig.update_traces(selector=dict(name=s), z = Ab[-1][0] * X + Ab[-1][1] * Y - Ab[-1][-1])
    rref = RREF(np.array(Ab))
    c = []
    for i in range(rref.shape[0]):
        nz = np.nonzero(rref[i, :])[0]
        if len(nz):
            c.append(nz[0])
    if (len(c) == 2):
        if 0 not in c: #x is free variable
            x = np.array([0, 1])
            y = np.ones_like(x) * rref[0, -1]
            z = np.ones_like(x) * rref[1, -1]
        elif 1 not in c: #y is free variable
            y = np.array([0, 1])
            x = rref[0, -1] - rref[0, 1] * y
            z = np.ones_like(x) * rref[1, -1]
        else: #z is free variable
            z_lower = []
            z_upper = []
            for i in range(2):
                if rref[i, 2] > 0:
                    z_lower.append((rref[i, -1] - 1) / rref[i, 2])
                    z_upper.append(rref[i, -1] / rref[i, 2])
                elif rref[i, 2] < 0:
                    z_upper.append((rref[i, -1] - 1) / rref[i, 2])
                    z_lower.append(rref[i, -1] / rref[i, 2])
            z = np.array([max(z_lower), min(z_upper)])
            x = rref[0, -1] - rref[0, 2] * z
            y = rref[1, -1] - rref[1, 2] * z
        if np.all((x >= 0) & (x <= 1) & (y >= 0) & (y <= 1)):
            fig.update_traces(selector=dict(name="line"), x = x, y = y, z = z, visible = True)
            return fig
    fig.update_traces(selector=dict(name="line"), visible = False)
    return fig

app.run(debug=True)