from flask import Flask, render_template, request, flash, redirect, url_for
from urllib.parse import urlparse

app = Flask(__name__)
app.secret_key = 'your_secret_key'


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/shorten_url', methods=['POST'])
def shorten_url():
    long_url = request.form['long_url']
    if is_valid_url(long_url):
        return render_template('home.html', long_url=long_url)
    else:
        flash('Invalid URL')
        return redirect(url_for('home'))


def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


if __name__ == '__main__':
    app.run(debug=True)
