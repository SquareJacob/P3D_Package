from dash import Dash, dash_table, dcc, html, Input, Output, callback
import plotly.graph_objects as go
import numpy as np

class Webpage(Dash):
    def __init__(self, **kwargs):
        """ """
        super().__init__(**kwargs)