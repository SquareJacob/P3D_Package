from dash import Dash, dash_table, dcc, Input, Output
import plotly.graph_objects as go
import numpy as np
import numexpr as ne
from typing import List, Union, Dict
import sympy as sp
import re
from sympy.parsing.sympy_parser import (
    parse_expr,
    standard_transformations,
    implicit_multiplication_application,
    convert_xor,
)

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
        style = {}
        if not height is None:
            style['height'] = f'{int(100 * height)}vh'
        if "style" in kwargs.keys():
            style = style | kwargs["style"]
        super().__init__(figure = figure, id = id, style = style, **kwargs)

class DataTable(dash_table.DataTable):
    """Table component for webpage"""
    def __init__(self, columns:List[str] = [], data: List[Union[List, Dict]] = [], id:str = None, height: float = None, column_ids:Union[Dict[Union[str, int], str], List[str]] = {}, properties: Dict[str, any] = {}, **kwargs):
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
            the unique id to identify this table with
        height
            the proportion of the height of the window to take up; 0 to 1
        column_ids
            ids to use instead of default ids.
            Can specify column by its name or index.
            Alternatively list of ids, in same order as names
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
        if isinstance(column_ids, list):
            column_ids = {
                i : cID for i, cID in enumerate(column_ids)
            }
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
        style_table = {}
        if not height is None:
            style_table['height'] = f'{int(100 * height)}vh'
        if "style_table" in kwargs.keys():
            style_table = style_table | kwargs["style_table"]
        super().__init__(columns=column_data, data=row_data, id = tID, style_table= style_table, **kwargs)

class TextArea(dcc.Textarea):
    """A text input area"""
    symbols = {'sin', 'cos', 'ln', 'pi', 'exp', 'log'}
    transforms = standard_transformations + (convert_xor, implicit_multiplication_application)
    def __init__(self, value:str = None, id:str = None, height:float = None, **kwargs):
        """
        Creates A text input area

        
        Parameters
        ----------
        value
            The initial text inside of this textbox
        id
            the unique id to identify this textarea with
        height
            the proportion of the height of the window to take up; 0 to 1
        """
        style = {}
        if not height is None:
            style['height'] = f'{int(100 * height)}vh'
        if "style" in kwargs.keys():
            style = style | kwargs["style"]
        super().__init__(value = value, id = id, style = style, **kwargs)

    @staticmethod
    def convert(text:str, as_string: bool = True) -> Union[str, sp.Expr]:
        """
        Converts a normal math expression to a Python math expression

        Parameters
        ----------
        text
            the text to convert
        as_string
            whether to return the raw sympy expression output, or the string output
        """
        names = set(re.findall(r"[A-Za-z_]\w*", text)) - TextArea.symbols
        local_dict = {name: sp.Symbol(name) for name in names}
        text = parse_expr(text, local_dict, TextArea.transforms)
        return str(text) if as_string else text
    
    @staticmethod
    def evaluate(text:str, variables:Dict[str, any]) -> any:
        """
        Evaluates a normal math expression using the values
        of the variables given.

        Parameters
        ----------
        text
            the math expression to evaluate
        variables
            dictionary of variables names and their values
        """
        variables['pi'] = np.pi
        return ne.evaluate(TextArea.convert(text), variables)
    
    @staticmethod
    def latex(text) -> str:
        """
        Converts a normal math expression into a latex formula

        Parameters
        ----------
        text
            the math expression to convert        
        """
        return sp.latex(TextArea.convert(text, as_string = False))
    
    def create_Markdown(self, app : Dash, id:str, height:float = None, **kwargs) -> dcc.Markdown:
        """
        Creates a markdown area that renders all text in this into a nice format.

        Parameters
        ----------
        app
            the app that will have both the textarea and the markdown area
        id
            the unique id to identify this markdown with
        height
            the proportion of the height of the window to take up; 0 to 1
        """
        style = {}
        if not height is None:
            style['height'] = f'{int(100 * height)}vh'
        if "style" in kwargs.keys():
            style = style | kwargs["style"]
        markdown_area = dcc.Markdown(children = '', mathjax=True, id = id, style=style, **kwargs)
        @app.callback(
            Output(id, 'children'),
            Input(self.id, 'value')
        )
        def edit(data):
            try: 
                return f'${TextArea.latex(data)}$'
            except:
                return ''
        return markdown_area