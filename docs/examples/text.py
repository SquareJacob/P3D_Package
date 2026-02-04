import P3D.webpage as p3w
import P3D.graphing as p3g
import plotly.graph_objects as go
import numpy as np
from dash import Input, Output

x = np.linspace(-1, 1, 101)
fig = p3g.Figure(data = p3g.Line(x = x, y = x))

app = p3w.Webpage()
textarea = p3w.TextArea(value = 'x^2', id = 'rawInput', height = 0.1)
app.layout = [
    p3w.Graph(fig, id = 'graph', height = 0.7),
    textarea,
    textarea.create_Markdown(app = app, id = 'niceInput', height = 0.1)
]

@app.callback(
    Output('graph', 'figure'),
    Input('rawInput', 'value')
)
def render(data):
    try:
        fig.update_traces(y = p3w.TextArea.evaluate(data, {'x': x}))
    except:
        pass
    return fig

app.run(debug=True)