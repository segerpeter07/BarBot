from flask import Flask
from flask import render_template
from flask import request
from flask import url_for
from flask import redirect

app = Flask(__name__)


@app.route('/', methods = ['GET', 'POST'])
def home():
    return render_template('drinkbuttons.html')

@app.route('/drinkresults', methods = ['GET','POST'])
def drink():
    if request.method=='POST':
        mixer=request.form['mixers']
        alcohol=request.form['alcohol']
        if mixer and alcohol:
            return render_template('drinksresults.html',mixer=mixer, alcohol=alcohol)
if __name__ == '__main__':
    app.run()
