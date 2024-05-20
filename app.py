from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/shorten_url', methods=['POST'])
def shorten_url():
    long_url = request.form['long_url']
    return render_template('home.html', long_url=long_url)


if __name__ == '__main__':
    app.run(debug=True)
