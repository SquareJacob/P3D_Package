import P3D.webpage as p3w
from dash import html

app = p3w.Webpage()

upload = p3w.Upload(id = 'upload-data', height = 0.1, multiple=False)
app.layout= [
    upload,
    html.Div(id ='text')
]
def use_file(contents, filename, last_modified):
    return f'The file \'{filename}\' was last updated {last_modified} seconds after 1970'
    
upload.on_upload(app, use_file, outputs = [['text', 'children']])


app.run(debug = True)