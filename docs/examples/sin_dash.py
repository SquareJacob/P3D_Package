"""
Program that draws 3 modifiable sin waves.
"""
import P3D.graphing as p3g
import P3D.webpage as p3w
from dash import Input, Output
import numpy as np

x = np.linspace(0, 2 * np.pi, 1001)
# Make a figure with 3 lines
# The name here will used to reference each line later
# What we put in y does not matter, as will be explained later
fig = p3g.Figure(data = [p3g.Line(x = x, y = 100000000 * x, name = str(i)) for i in range(3)])
# Notice we did not have to pre-calculate and store any additional lines like before

app = p3w.Webpage() # This will be the webpage

app.layout = [
    p3w.Graph(fig, id = 'graph', height = 0.7), # Put the figure in a graph. height is proportion of window's height
    p3w.DataTable( #Automatic scroll functionality
        columns = ['freq', 'amp'], # This says we will have 2 columns, and the names they will display
        column_ids = ['f', 'a'], # The ids for our 2 columns
        id = 'table',
        data = [ # Initial data we want in the table; how number of rows is determined
            [0, 2],
            [1, 1],
            [2, 0.5]
        ],
        height = 0.2, # Proportion of window's height. In other words, this will be 20% as tall as the window
        properties = {
            'editable' : ['f'] # Which columns we want to be editable, indicated by id
        }
    )
]

#callback defines a function (editFigure) that is called whenever an Input changes
@app.callback(
    Output('graph', 'figure'), #'graph' is the id we put in p3w.Graph
    Input('table', 'data') #'table' is id the id we put in p3w.DataTable
    # Since the data in the table is the input, whenever that changes, the below function is called
    # Note that on startup, when the data is set, this is also called
)
def editFigure(data): #data parameter is the data input above
    for i in range(3):
        # data is a list of rows; each row has values based upon column id
        # In other words, we get cell data by data[row number][column id]
        # since cell data is typed, it will be a string. We use float() to convert it to numbers
        # We select the line to update based upon name
        fig.update_traces(y = float(data[i]['a']) * np.sin(x * float(data[i]['f'])), selector=dict(name = str(i)))
        # Initial y data at very beginning does not matter; will be overridden by this
    # The output (figure in graph) is set by return value
    return fig


app.run(debug = True) #Starts the application. using 'debug=True' means it will tell us any errors that happen