"""
This a program with a slider for variable a, with 2 curves:
y = a * sin(x)
y = sin(a * x)
"""
import P3D.graphing as p3g
import numpy as np

x = np.linspace(-10, 10, 200)

fig = p3g.Figure()

A = np.linspace(0, 1, 21) # Array of all values of a for the slider

# make the frames
frames = []
for a in A:
    # Each frame has 2 traces. 
    # We do not need to make them invisible; that will be handled by the function below.
    frames.append([
        p3g.Line(x = x, y = a * np.sin(x)), #y = a * sin(x)
        p3g.Line(x = x, y = np.sin(a * x))  #y = sin(a * x)
    ])
# Each element of frames is a list of lines we want visible on that frame

fig.add_slider( #Behold! The function that makes this way simpler!
    slider_values = np.round(A, 4), # Round to make it nicer, 
    traces = frames,
    initial_step =  0, # We want the first frame visible at start
    prefix = "a: "
)

fig.show()