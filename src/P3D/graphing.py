import plotly.graph_objects as go
import numpy as np
from typing import List, Union


class Figure(go.Figure):
    """Assumes a 3D figure"""
    def __init__(self, data:List[go.Trace] = None, **kwargs):
        """Assumes a 3D figure"""
        super().__init__(data = data, **kwargs)
        self.update_layout(
            scene_aspectmode='cube',
        )

    def update_bounds(self, x:List[float] = None, y:List[float] = None, z:List[float] = None):
        self.update_layout(
            scene = dict(
                xaxis=dict(range=x),
                yaxis=dict(range=y),
                zaxis=dict(range=z),
            )
        )

    def add_slider(self, slider_values:List[float], traces:List[Union[go.Trace, List[go.Trace]]], initial_step:int = 0, prefix:str = "t: "):
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
    def __init__(self, x, y, z, showscale = False, **kwargs):
        """ """
        super().__init__(x = x, y = y, z = z, showscale = showscale, **kwargs)

class Line(go.Scatter3d):
    """Assumes a 3D line"""
    def __init__(self, x, y, z, **kwargs):
        """Assumes a 3D line"""
        super().__init__(x = x, y = y, z = z, mode='lines', **kwargs)