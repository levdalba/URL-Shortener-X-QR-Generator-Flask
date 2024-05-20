from flask import Flask, render_template, request, flash, url_for, redirect
from urllib.parse import urlparse

app = Flask(__name__)
app.config['SECRET_KEY'] = 'anything'


@app.route('/')
def home():
    return render_template('home.html')


if __name__ == '__main__':
    app.run(debug=True)
