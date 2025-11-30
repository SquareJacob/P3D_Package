import plotly.graph_objects as go
import numpy as np
from numpy.typing import NDArray
from typing import List, Union


class Figure(go.Figure):
    """A 3D graph"""
    def __init__(self, data:List[go.Trace] = None, **kwargs):
        """
        Creates a 3D figure

        Parameters
        ----------
        data
            List of traces for this figure to have
        """
        super().__init__(data = data, **kwargs)
        self.update_layout(
            scene_aspectmode='cube',
        )

    def update_bounds(self, x:List[float] = None, y:List[float] = None, z:List[float] = None) -> None:
        """
        Updates the bounds for this figure

        Parameters
        ----------
        x,y,z
            Bounds that can be updated, if provided, as a list of 2 numbers
        """
        self.update_layout(
            scene = dict(
                xaxis=dict(range=x),
                yaxis=dict(range=y),
                zaxis=dict(range=z),
            )
        )

    def add_slider(self, slider_values:List[float], traces:List[Union[go.Trace, List[go.Trace]]], initial_step:int = 0, prefix:str = "t: ") -> None:
        """
        Adds a new slider to this figure

        Parameters
        ----------
        slider_values
            List of N values the slider should have
        traces
            List of traces to add, and which slider value they should be visible on.
            Each element can be a list itself, meaning multiple traces are visible on that value
        initial_step
            Which step (0 to N-1) to start the slider on
        prefix
            how each step on the slider is labelled
        """
        steps = []
        N = len(self.data)
        A = sum([len(i) if isinstance(i, list) else 1 for i in traces])
        for i in range(len(slider_values)):
            step = dict(
                method="update",
                label = slider_values[i],
                args=[{"visible": [None] * N + [False] * A}]
            )
            if i < len(traces):
                if isinstance(traces[i], list):
                    for j in range(len(traces[i])):
                        traces[i][j].visible = i == initial_step
                        step["args"][0]["visible"][len(self.data)+j] = True
                    self.add_traces(traces[i])
                else:
                    traces[i].visible = i == initial_step
                    self.add_traces([traces[i]])
                    step["args"][0]["visible"][len(self.data)-1] = True
            steps.append(step)
        self.update_layout(
            sliders = list(self.layout.sliders) + [dict(steps = steps, active = initial_step, currentvalue={"prefix": prefix})]
        )

class Surface(go.Surface):
    """A 3D Surface"""
    def __init__(self, x:NDArray[np.floating], y:NDArray[np.floating], z:NDArray[np.floating], showscale:bool = False, **kwargs):
        """
        Creates a 3D surface

        Parameters
        ----------
        x,y,z
            2D arrays all of the same shape. 
            Each ordered triple is a point on the surface
        showscale
            Whether to show the colorbar on the side
        """
        super().__init__(x = x, y = y, z = z, showscale = showscale, **kwargs)

class Line(go.Scatter3d):
    """A 3D line"""
    def __init__(self, x:NDArray[np.floating], y:NDArray[np.floating], z:NDArray[np.floating], **kwargs):
        """
        Creates a 3D line

        Parameters
        ----------
        x,y,z
            1d arrays all of the same length.
            Each ordered triple is a point on the line
        """
        super().__init__(x = x, y = y, z = z, mode='lines', **kwargs)