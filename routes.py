from flask import Flask, render_template, request
from wtforms import Form, TextField, validators

app = Flask(__name__)

#insert db classes here

class information(Form):
    #barebones example of how to use wtf forms
    team_number = TextField('Team Number', [validators.Length(min=2,max=4)])


@app.route('/')
def front_page():
    data = information(request.form)
    #using validators with the forms
    #if data.validate():
    return render_template('index.html', title='Home', data=data)


app.run(debug=True)
