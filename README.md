# **URL Shortener and QR Code Generator**

This group project is a simple web application built with Flask that allows users to shorten URLs and generate QR codes for given URL.

The application uses Gunicorn as the WSGI server and employs Tailwind CSS for styling.


---

## **Features**

Shorten URLs: Input a long URL to receive a shortened version.

Generate QR Codes: Convert any URL into a scannable QR code.

User Authentication: Users can log in or sign up to manage their shortened URLs and QR codes.

Responsive Design: The application is designed to work well on both desktop and mobile devices.



## **Tech Stack**

Backend: Python, Flask

Frontend: HTML, CSS (Tailwind CSS)

Database: Dictionary [Database setup can be added if applicable]

Server: Gunicorn

## **Requirements**

**Before running the application, ensure you have the following installed:**
```bash
Python 3.x
Pip
```

1. **Install Dependencies**
You can install the required packages using the following command:

```bash
pip install -r requirements.txt
```

2. **Requirements File**
The requirements.txt file includes the following packages:

```bash
Flask
gunicorn
qrcode==7.3.1
Pillow==8.2.0
```

3. **Procfile**
The Procfile is used for deployment with Gunicorn. It should contain the following line:

```bash
web: gunicorn -b :$PORT app:app
```

## **Usage**

**Clone this repository to your local machine:**
```bash
git clone https://github.com/yourusername/URL-Shortener-Flask.git
cd URL-Shortener-Flask
```

**Install the required dependencies:**
```bash
pip install -r requirements.txt
```

**Run the application in Terminal**
```bash
python app.py
```

**Open your web browser and go to:**
```bash
http://127.0.0.1:5000
```

## **Folder Structure**
```bash
URL-Shortener-Flask/
│
├── app.py            # Main application file
├── Procfile          # For deployment with Gunicorn
├── requirements.txt  # List of required Python packages
├── templates/        # HTML templates for rendering pages
│   ├── home.html
│   ├── login.html
│   └── signup.html
```

## **Contributing**

Contributions are welcome! Please feel free to submit a pull request or open an issue to discuss improvements or bugs.
