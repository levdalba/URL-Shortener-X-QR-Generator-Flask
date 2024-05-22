import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Create a new figure and axis
fig, ax = plt.subplots(figsize=(10, 6))


# Function to add a text box with an arrow
def add_box(ax, text, xy, width=1.8, height=1, text_offset=(0.5, 0.5)):
    rect = patches.FancyBboxPatch(
        (xy[0] - width / 2, xy[1] - height / 2),
        width,
        height,
        boxstyle="round,pad=0.3",
        edgecolor="black",
        facecolor="lightgrey",
    )
    ax.add_patch(rect)
    ax.text(xy[0], xy[1], text, ha="center", va="center", fontsize=10)


# Add client-side (browser) box
add_box(ax, "Browser\n(Client)", (1, 2.5))

# Add Flask server box
add_box(ax, "Flask Server", (4, 2.5))

# Add arrows to indicate flow
arrowprops = dict(facecolor="black", arrowstyle="->")

# Arrow from Browser to Flask Server
ax.annotate("", xy=(2.5, 2.5), xytext=(1.8, 2.5), arrowprops=arrowprops)
ax.text(2.15, 2.65, "Send URL", fontsize=9, ha="center")

# Arrow from Flask Server to Browser
ax.annotate("", xy=(1.8, 2), xytext=(2.5, 2), arrowprops=arrowprops)
ax.text(2.15, 1.85, "Receive Short URL", fontsize=9, ha="center")

# Set limits and remove axes
ax.set_xlim(0, 6)
ax.set_ylim(1, 4)
ax.axis("off")

# Display the diagram
plt.show()
from flask import Flask, render_template, request, flash, redirect, url_for, session
from urllib.parse import urlparse
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "your_secret_key"


class UserRepo:
    def __init__(self):
        self.users = {}
        self.id_counter = 1

    def add_user(self, username, password):
        if username in self.users:
            return False
        user_id = self.id_counter
        self.users[username] = {
            "id": user_id,
            "username": username,
            "password": generate_password_hash(password),
        }
        self.id_counter += 1
        return True

    def get_user(self, username):
        return self.users.get(username)


user_repo = UserRepo()


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if user_repo.add_user(username, password):
            flash("User created successfully, please login")
            return redirect(url_for("login"))
        else:
            flash("Username already exists")
    return render_template("signup.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = user_repo.get_user(username)
        if user and check_password_hash(user["password"], password):
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            return redirect(url_for("home"))
        else:
            flash("Invalid username or password")
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("user_id", None)
    session.pop("username", None)
    flash("You have been logged out")
    return redirect(url_for("home"))


# URL shortener
@app.route("/shorten_url", methods=["POST"])
def shorten_url():
    long_url = request.form["long_url"]
    if is_valid_url(long_url):
        return render_template("home.html", long_url=long_url)
    else:
        flash("Invalid URL")
        return redirect(url_for("home"))


# Checker for URL
def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


if __name__ == "__main__":
    app.run(debug=True)
