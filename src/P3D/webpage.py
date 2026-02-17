from dash import Dash, dash_table, dcc, Input, Output, html, State
import plotly.graph_objects as go
import numpy as np
import numexpr as ne
from typing import List, Union, Dict, Callable
import sympy as sp
import re
import random
import string
from sympy.parsing.sympy_parser import (
    parse_expr,
    standard_transformations,
    implicit_multiplication_application,
    convert_xor,
)

class Webpage(Dash):
    """A Dash webpage, extends :dash:`dash.Dash<dash>`"""
    def __init__(self, **kwargs):
        """Creates A Dash webpage"""
        super().__init__(**kwargs)
    
class Graph(dcc.Graph):
    """Graph component for webpage, extends :dcc:`dash.dcc.Graph<graph>`"""
    def __init__(self, figure: go.Figure = None, id:str = None, height: float = None, **kwargs):
        """
        Creates a graph component for webpage

        Parameters
        ----------
        figure
            The :class:`plotly.graph_objects.Figure` to use in this graph
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
        if figure:
            kwargs['figure'] = figure
        if id:
            kwargs['id'] = id
        super().__init__(style = style, **kwargs)

class DataTable(dash_table.DataTable):
    """Table component for webpage, extends |table|_"""
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
        if id:
            kwargs['id'] = id
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
        super().__init__(columns=column_data, data=row_data, style_table= style_table, **kwargs)

class TextArea(dcc.Textarea):
    """A text input area, extends :dcc:`dash.dcc.TextArea<textarea>`"""
    _symbols = {'sin', 'cos', 'ln', 'pi', 'exp', 'log'}
    _transforms = standard_transformations + (convert_xor, implicit_multiplication_application)
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
        if value:
            kwargs['value'] = value
        if id:
            kwargs['id'] = id
        super().__init__(style = style, **kwargs)

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
        names = set(re.findall(r"[A-Za-z_]\w*", text)) - TextArea._symbols
        local_dict = {name: sp.Symbol(name) for name in names}
        text = parse_expr(text, local_dict, TextArea._transforms)
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
    
    def create_Markdown(self, app : Dash, id:str = None, height:float = None, **kwargs) -> dcc.Markdown:
        """
        Creates a markdown area that renders all text in this into a nice format.

        Parameters
        ----------
        app
            the :dash:`dash.Dash<dash>` app that will have both the textarea and the markdown area
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
        if id:
            kwargs['id'] = id
        markdown_area = dcc.Markdown(children = '', mathjax=True, style=style, **kwargs)
        @app.callback(
            Output(markdown_area.id, 'children'),
            Input(self.id, 'value')
        )
        def edit(data):
            try: 
                return f'${TextArea.latex(data)}$'
            except:
                return ''
        return markdown_area
    
class Slider(dcc.Slider):
    """A text input area, extends :dcc:`dash.dcc.Slider<slider>`"""
    def __init__(self, min: float = 0, max: float = 1, value : float = None, step: float = None, marks : Union[dict, None] = dict(), id: str = None, **kwargs):
        """
        Creates A Dash Slider
        
        Parameters
        ----------
        min, max
            bounds on the slider
        value
            initial value for slider
        step
            spacing between each step on slider
        marks
            optional dictionary to provide exact steps and labels; set to None for no labels at all
        id
            the unique id to identify this slider with
        """
        kwargs["updatemode"] =  kwargs.get("updatemode", "drag")
        if id:
            kwargs['id'] = id
        if value:
            kwargs['value'] = value
        kwargs['step'] = step
        kwargs["tooltip"] = kwargs.get("tooltip", {
                "always_visible": False
            })
        super().__init__(min = min, max = max, marks = marks, **kwargs)

class Button(html.Button):
    """A button, extends :html:`dash.html.Button<button>`"""
    def __init__(self, text:str = '', id: str = None, **kwargs):
        """
        Creates a Button
        
        Parameters
        ----------
        text
            text to display on button
        id
            the unique id to identify this button with
        """
        if id:
            kwargs['id'] = id
        if "children" in kwargs.keys():
            children = kwargs['children']
        else:
            children = text
        super().__init__(children = children, **kwargs)
    
    def on_click(self, app: Dash, func: Callable, outputs: List[List[str]] = [], other_inputs: List[List[str]] = [], states: List[List[str]] = [], starting_call: bool = False):
        """
        What to do when button is clicked
        
        Parameters
        ----------
        app
            the :dash:`dash.Dash<dash>` app that has this button and handles this event
        func
            the actual function to be used on click. The function arguments, in the given order, have to be:\n
            \t the number of times this button has ben clicked (1 argument)\n
            \t other provided inputs (1 argument for each, in order)\n
            \t any provided states (1 argument for each, in order)\n
            `func` should return one value for each output given, in order
        outputs
            List of outputs. Each element should be in the style ['component_id', 'component_property']
        states, other_inputs
            List of any states to use or additional inputs. Both states and inputs are used as arguments, but this event will be called whenever any input is modified, but not when any state is modified. Same style as `outputs`
        starting_call
            whether to call this event on load of the webpage
        """
        @app.callback(
            *[Output(output[0], output[1]) for output in outputs],
            Input(self.id, 'n_clicks'),
            *[Input(input[0], input[1]) for input in other_inputs],
            *[State(state[0], state[1]) for state in states],
            prevent_initial_call = not starting_call
        )
        def callback(*args):
            return func(*args)
        
class Interval(dcc.Interval):
    """A ticking interval, extends :dcc:`dash.dcc.Interval<interval>`"""
    def __init__(self, app: Dash, id: str = None, ms: int = 1000, disabled: bool = False, value:float = 0, max_intervals:int = -1, step:float = 1, **kwargs):
        """
        Creates an Interval
        
        Parameters
        ----------
        app
            the :dash:`dash.Dash<dash>` app that has this interval and will handle its ticking
        id
            the unique id to identify this button with
        ms
            the number of milliseconds between each tick
        disabled
            disabled means the interval does not begin ticking right away
        value
            initial value in interval
        max_intervals
            the max number of times this can tick. Set to -1 for infinite
        step
            how much to change value by at each tick
        """
        self.step:float = step
        self.value_id:str = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
        if id:
            kwargs['id'] = id
        super().__init__(interval = ms, disabled = disabled, max_intervals = max_intervals, **kwargs)
        self.value: dcc.Store = dcc.Store(id = self.value_id, data = value)
        @app.callback(
            Output(self.value_id, 'data', allow_duplicate=True),
            Input(self.id, 'n_intervals'),
            State(self.value_id, 'data'),
            prevent_initial_call = True
        )
        def tick(n, v):
            return v + self.step

    def on_tick(self, app: Dash, func: Callable, outputs: List[List[str]] = [], other_inputs: List[List[str]] = [], states: List[List[str]] = [], starting_call: bool = False):
        """
        What to do when this interval ticks
        
        Parameters
        ----------
        app
            the :dash:`dash.Dash<dash>` app that has this button and handles this event
        func
            the actual function to be used on click. The function arguments, in the given order, have to be:\n
            \t the current value stored in this interval (1 argument)\n
            \t other provided inputs (1 argument for each, in order)\n
            \t any provided states (1 argument for each, in order)\n
            `func` should return one value for each output given, in order
        outputs
            List of outputs. Each element should be in the style ['component_id', 'component_property']
        states, other_inputs
            List of any states to use or additional inputs. Both states and inputs are used as arguments, but this event will be called whenever any input is modified, but not when any state is modified. Same style as `outputs`
        starting_call
            whether to call this event on load of the webpage
        """
        @app.callback(
            *[Output(output[0], output[1]) for output in outputs],
            Input(self.value_id, 'data'),
            *[Input(input[0], input[1]) for input in other_inputs],
            *[State(state[0], state[1]) for state in states],
            prevent_initial_call = not starting_call
        )
        def callback(*args):
            return func(*args)

class Upload(dcc.Upload):
    """Allows for uploading files, extends :dcc:`dash.dcc.Upload<upload>`"""
    def __init__(self, height: float, width: float = None, id:str = None, multiple:bool = False, text:str = 'Drag and Drop or Select Files', **kwargs):
        """
        Creates an Upload component
        
        Parameters
        ----------
        height
            the proportion of the height of the window to take up; 0 to 1
        width
            the proportion of the width of the window to take up; 0 to 1
        multiple
            whether this can take in  multiple files
        id
            the unique id to identify this button with
        text
            text to display on this Upload component
        """
        if id:
            kwargs['id'] = id
        style = {
            'height': f'{int(100 * height)}vh',
            'lineHeight': f'{int(100 * height)}vh',
            'cursor': 'pointer',
            'textAlign': 'center',
            'borderWidth': '1px',
            'borderStyle': 'solid',
            'borderRadius': '5px'
        }
        if not width is None:
            style['width'] = f'{int(100 * width)}vh'
        if "style" in kwargs.keys():
            style = style | kwargs["style"]
        if "children" in kwargs.keys():
            children = kwargs['children']
        else:
            children = text
        super().__init__(style = style, multiple = multiple, children = children, **kwargs)

    def on_upload(self, app: Dash, func: Callable, outputs: List[List[str]] = [], other_states: List[List[str]] = [], starting_call: bool = False):
        """
        What to do when files are uploaded
        
        Parameters
        ----------
        app
            the :dash:`dash.Dash<dash>` app that has this button and handles this event
        func
            the actual function to be used on file upload. The function arguments, in the given order, have to be:\n
            \t the content of the file, or list of content if multiple is True\n
            \t the filename, or list of filenames if multiple is True\n
            \t the time file was last modified, given by seconds since 1970, or list if multiple is True\n
            \t any other provided states (1 argument for each, in order)\n
            `func` should return one value for each output given, in order
        outputs
            List of outputs. Each element should be in the style ['component_id', 'component_property']
        other_states
            List of any states to use or additional inputs. Both states and inputs are used as arguments, but this event will be called whenever any input is modified, but not when any state is modified. Same style as `outputs`
        starting_call
            whether to call this event on load of the webpage
        """
        @app.callback(
            *[Output(output[0], output[1]) for output in outputs],
            Input(self.id, "contents"),
            State(self.id, "filename"),
            State(self.id, "last_modified"),
            *[State(state[0], state[1]) for state in other_states],
            prevent_initial_call = not starting_call
        )
        def callback(*args):
            return func(*args)