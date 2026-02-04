import P3D.webpage as p3w
from dash import Input, Output

app = p3w.Webpage()

app.layout = [
    p3w.Slider(min=0, max=100, step = 5, id = 'slider', value = 50, marks = None),
    p3w.TextArea(id = 'text')
]
@app.callback(Output("text", "value"), Input("slider", "value"))
def show(v):
    return f"slider value: {v}"

app.run(debug=True)