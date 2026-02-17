import P3D.webpage as p3w

app = p3w.Webpage()

button = p3w.Button(text = 'wow', id ='b') #Changing 'wow' will change text on button
app.layout = [
    button,
    p3w.TextArea('bee', id='1'),
    p3w.TextArea('boo', id='2'),
    p3w.TextArea('bro', id='3'),
    p3w.TextArea('ble', id='4')
]

#function for on_click
def funny(n_clicks, text3, text4): #n_clicks is always first argument, then other_inputs, then states
    return f"{n_clicks}, wow!", f"{text3} or {text4}" #outputs in order

button.on_click(
    app = app, 
    func = funny, 
    outputs = [['1', 'value'], ['2', 'value']], 
    other_inputs = [['3', 'value']], 
    states = [['4', 'value']], 
    starting_call = False #Setting this to true will cause the on_click function to be triggered on page load
)

app.run(debug=True)