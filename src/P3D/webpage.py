from dash import Dash, dash_table, dcc, html, Input, Output, callback
import plotly.graph_objects as go
import numpy as np
from typing import List, Union, Dict

class Webpage(Dash):
    """A Dash webpage"""
    def __init__(self, **kwargs):
        """Creates A Dash webpage"""
        super().__init__(**kwargs)
    
class Graph(dcc.Graph):
    """Graph component for webpage"""
    def __init__(self, figure: go.Figure = None, id:str = None, height: float = None, **kwargs):
        """
        Creates a graph component for webpage

        Parameters
        ----------
        figure
            The figure to use in this graph
        id
            the unique id to identify this graph with
        height
            the proportion of the height of the window to take up; 0 to 1
        """
        style = {'height': f'{int(100 * height)}vh'}
        if "style" in kwargs.keys():
            style = style | kwargs["style"]
        super().__init__(figure = figure, id = id, style = style, **kwargs)

class DataTable(dash_table.DataTable):
    """Table component for webpage"""
    def __init__(self, columns:List[str] = [], data: List[Union[List, Dict]] = [], id:str = None, height: float = None, column_ids:Dict[Union[str, int], str] = {}, properties: Dict[str, any] = {}, **kwargs):
        """
        Creates a table component for webpage

        Parameters
        ----------
        columns
            List of columns to use. 
            Each element is the column's name and default id
        data
            Each element of list is one row of the table.
            Element can be a list of values based upon column order,
            or a dictionary of values with keys as column ids
        id
            the unique id to identify this graph with
        height
            the proportion of the height of the window to take up; 0 to 1
        column_ids
            ids to use instead of default ids.
            Can specify column by its name or index
        properties
            Assigns properties to columns.
            Each key is a property, and each value is what columns has that property.
            Value can be True, meaning to apply to all columns.
            Value can be a list of indices and/or ids to choose columns.
            Common properties are editable, renamable, deletable, and clearable.
        """
        column_data = []
        ids = []
        tID = id
        for i, name in enumerate(columns):
            if i in column_ids.keys():
                id = column_ids[i]
            elif name in column_ids.keys():
                id = column_ids[name]
            else:
                id = name
            column = dict(id = id, name = name)
            ids.append(id)
            for property, value in properties.items():
                if isinstance(value, list):
                    column[property] = (id in value) or (i in value)
                else:
                    column[property] = value
            column_data.append(column)
        row_data = []
        for row in data:
            frow = {}
            if isinstance(row, list):
                for i in range(len(row)):
                    frow[ids[i]] = row[i]
            elif isinstance(row, dict):
                frow = row
            row_data.append(frow)
        style_table = {'height': f'{int(100 * height)}vh'}
        if "style_table" in kwargs.keys():
            style_table = style_table | kwargs["style_table"]
        super().__init__(columns=column_data, data=row_data, id = tID, style_table= style_table, **kwargs)