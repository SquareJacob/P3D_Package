import P3D.webpage as p3w
from dash import Input, Output
import numpy as np

app = p3w.Webpage()

interval = p3w.Interval(app, id='int', ms = 500, value = 5, step = 3)
button = p3w.Button('Set to 5', id = 'btn')
app.layout = [
    interval, interval.value, #Notice that both interval and its value need to be in layout
    p3w.TextArea('bee', id='1'),
    p3w.TextArea('boo', id='2'),
    p3w.TextArea('bro', id='3'),
    p3w.TextArea('ble', id='4'),
    button,
    p3w.Slider(-5, 5, 3, step = 0.01, id='slider', marks = {i: str(i) for i in np.linspace(-5, 5, 21)})
]

#function for on_tick
def funny(value, text3, text4): #value is always first argument, then other_inputs, then states
    return f"{np.round(value, 5)}, wow!", f"{text3} or {text4}" #outputs in order
            #np.round is used to deal with slight errors in floats by rounding to 5 decimal places
            #If you are curious, remove it, and and then let the page run while slowly changing the slider
            #You will see values that show the floating point error

interval.on_tick(
    app = app,
    func = funny, 
    outputs = [['1', 'value'], ['2', 'value']], 
    other_inputs = [['3', 'value']], 
    states = [['4', 'value']], 
    starting_call = True #Setting this to true will cause the on_click function to be triggered on page load
)

#This makes it so that when the button is clicked, the value in interval is set to 5
def click(n_clicks):
    return 5
button.on_click(app, func = click, outputs = [[interval.value_id, 'data']])
#Notice that to update the value, we cannot update interval.value directly for immediate updates
#We have to use callbacks with interval.value_id

#this callback sets the step of the interval to be equal to the value of the slider
@app.callback(Input("slider", "value"))
def stepper(v):
    interval.step = v



app.run(debug=True)