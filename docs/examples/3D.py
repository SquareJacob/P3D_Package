import P3D.graphing as p3g
import numpy as np

x = np.linspace(-1, 1, 100)
X, Y = np.meshgrid(x, x, indexing='ij')


t = np.linspace(0, 10 * np.pi, 1000)

fig = p3g.Figure(data = [
    p3g.Line(x = np.cos(t), y = np.sin(t), z = t / (2 * np.pi)), #Line can make 2d or 3d depending on if z is provided
    p3g.Surface(x = X, y = Y, z = X ** 2 + Y ** 2) #z=x^2+y^2
])

# Sets the bounds on the figure; this function works for both 2D and 3D figures
fig.update_bounds(
    # We do not specify x, meaning it will be unaffected
    y = [1, -1], # Having the upper bound first reverses direction
    z = [-1, 11]
)

fig.show()