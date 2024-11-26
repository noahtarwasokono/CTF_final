from flask import Flask, render_template, request, redirect, url_for, flash, make_response
import base64
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Flask setup
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

# Helper functions for encoding and decoding cookie values
def encode_cookie_value(value):
    return base64.b64encode(value.encode('utf-8')).decode('utf-8')

def decode_cookie_value(encoded_value):
    return base64.b64decode(encoded_value).decode('utf-8')

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username == "admin" and password == "password":
            # Successful login
            response = make_response(redirect(url_for('cookie_page')))
            # Set the initial cookie using the value from the environment
            initial_value = os.getenv('INITIAL_COOKIE_VALUE')
            response.set_cookie('flag_cookie', encode_cookie_value(initial_value), httponly=True)
            return response
        else:
            flash('Incorrect username or password. Please try again.')
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/cookie_page', methods=['GET'])
def cookie_page():
    # Retrieve the cookie from the user's browser
    cookie = request.cookies.get('flag_cookie')

    if cookie:
        try:
            # Decode the cookie value
            decoded_cookie = decode_cookie_value(cookie)

            # Check if the cookie has been modified to the correct target value
            target_value = os.getenv('TARGET_COOKIE_VALUE')
            if decoded_cookie == target_value:
                # If the cookie value is correct, reveal the final flag
                final_flag = os.getenv('FINAL_FLAG')
                return f"Congratulations! You found the real flag: {final_flag}"
            else:
                # Inform the user that the cookie is incorrect
                return render_template('cookie.html', current_cookie_value=decoded_cookie)
        except Exception:
            # Handle invalid or tampered cookie values
            return "The cookie value is invalid. Please try again.", 400
    else:
        # Redirect to login if no cookie is set
        return redirect(url_for('login'))

@app.route('/cookie_instructions', methods=['GET'])
def cookie_instructions():
    # Provide instructions to the user on how to decode, modify, and encode the cookie
    return render_template('cookie_instructions.html')

if __name__ == '__main__':
    app.run(debug=True)








