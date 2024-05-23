import string
import random
from flask import Flask, render_template, request, redirect, url_for, flash, session
import re
import qrcode
from io import BytesIO
import base64

app = Flask(__name__)
app.secret_key = "your_secret_key"

# In-memory databases to store user credentials and URL mappings
users = {}
url_mapping = {}


def generate_short_url():
    """Generate a random string of 6 characters prefixed with 'fatnik'."""
    prefix = "fatnik"
    suffix = "".join(random.choices(string.ascii_letters + string.digits, k=6))
    return prefix + suffix


def is_valid_url(url):
    """Simple URL validation."""
    regex = re.compile(
        r"^(?:http|ftp)s?://"  # http:// or https://
        r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|"  # domain...
        r"localhost|"  # localhost...
        r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|"  # ...or ipv4
        r"\[?[A-F0-9]*:[A-F0-9:]+\]?)"  # ...or ipv6
        r"(?::\d+)?"  # optional port
        r"(?:/?|[/?]\S+)$",
        re.IGNORECASE,
    )
    return re.match(regex, url) is not None


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username in users:
            flash("Username already exists.", "error")
        else:
            users[username] = password
            flash("Signup successful! Please login.", "success")
            return redirect(url_for("login"))
    return render_template("signup.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username in users and users[username] == password:
            session["username"] = username
            flash("Login successful!", "success")
            return redirect(url_for("home"))
        else:
            flash("Invalid username or password.", "error")
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("username", None)
    flash("You have been logged out.", "success")
    return redirect(url_for("home"))


@app.route("/shorten_url", methods=["POST"])
def shorten_url():
    if "username" not in session:
        flash("Please log in to shorten URLs.", "error")
        return redirect(url_for("login"))

    long_url = request.form.get("long_url")
    if long_url:
        if is_valid_url(long_url):
            short_url = generate_short_url()
            url_mapping[short_url] = long_url
            flash(f"Shortened URL: {request.host_url}{short_url}", "success")
        else:
            flash("Invalid URL. Please enter a valid URL.", "error")
    else:
        flash("Please enter a URL.", "error")
    return redirect(url_for("home"))


@app.route("/generate_qr", methods=["POST"])
def generate_qr():
    url = request.form["qr_url"]
    if not url:
        flash("URL is required!", "error")
        return redirect(url_for("home"))

    if not is_valid_url(url):
        flash("Invalid URL. Please enter a valid URL.", "error")
        return redirect(url_for("home"))

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill="black", back_color="white")
    img_io = BytesIO()
    img.save(img_io, "PNG")
    img_io.seek(0)

    # Convert image to base64
    img_base64 = base64.b64encode(img_io.getvalue()).decode("utf-8")

    return render_template("home.html", qr_code=img_base64)


@app.route("/<short_url>")
def redirect_to_long_url(short_url):
    long_url = url_mapping.get(short_url)
    if long_url:
        return redirect(long_url)
    else:
        flash("Invalid URL.", "error")
        return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
