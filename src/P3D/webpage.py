from dash import Dash, dash_table, dcc, html, Input, Output, callback
import plotly.graph_objects as go
import numpy as np
from typing import List, Union, Dict

class Webpage(Dash):
    def __init__(self, **kwargs):
        """ """
        super().__init__(**kwargs)
    
class Graph(dcc.Graph):
    def __init__(self, figure: go.Figure = None, id:str = None, height: float = None, **kwargs):
        """ """
        style = {'height': f'{int(100 * height)}vh'}
        if "style" in kwargs.keys():
            style = style | kwargs["style"]
        super().__init__(figure = figure, id = id, style = style, **kwargs)

class DataTable(dash_table.DataTable):
    def __init__(self, columns:List[str] = None, data: List[Union[List, Dict]] = None, id:str = None, height: float = None, properties: Dict[str, any] = None, **kwargs):
        """ """
        column_data = []
        for i, name in columns:
            column = dict(id = name, name = name)
            for property, value in properties.items():
                if isinstance(value, list):
                    column[property] = (name in value) or (i in value)
                else:
                    column[property] = value
            column_data.append(column)
        row_data = []
        for row in data:
            frow = {}
            if isinstance(row, list):
                for i in len(row):
                    frow[name[i]] = row[i]
            elif isinstance(row, dict):
                frow = row
            row_data.append(frow)
        style_table = {'height': f'{int(100 * height)}vh'}
        if "style_table" in kwargs.keys():
            style_table = style_table | kwargs["style_table"]
        super().__init__(columns=column_data, data=row_data, id = id, style_table= style_table, **kwargs)