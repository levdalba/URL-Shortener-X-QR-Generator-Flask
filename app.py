from flask import Flask, render_template, request, flash, redirect, url_for, session
from urllib.parse import urlparse
from werkzeug.security import generate_password_hash, check_password_hash
app = Flask(__name__)
app.secret_key = 'your_secret_key'


class UserRepo:
    def __init__(self):
        self.users = {}
        self.id_counter = 1

    def add_user(self, username, password):
        if username in self.users:
            return False
        user_id = self.id_counter
        self.users[username] = {
            'id': user_id,
            'username': username,
            'password': generate_password_hash(password)
        }
        self.id_counter += 1
        return True

    def get_user(self, username):
        return self.users.get(username)


user_repo = UserRepo()


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_repo.add_user(username, password):
            flash('User created successfully, please login')
            return redirect(url_for('login'))
        else:
            flash('Username already exists')
    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = user_repo.get_user(username)
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password')
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    flash('You have been logged out')
    return redirect(url_for('home'))


#URL shortener
@app.route('/shorten_url', methods=['POST'])
def shorten_url():
    long_url = request.form['long_url']
    if is_valid_url(long_url):
        return render_template('home.html', long_url=long_url)
    else:
        flash('Invalid URL')
        return redirect(url_for('home'))


#Checker for URL
def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


if __name__ == '__main__':
    app.run(debug=True)
