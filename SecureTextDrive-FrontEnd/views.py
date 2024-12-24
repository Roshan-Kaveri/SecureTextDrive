import binascii
import hashlib
import os
import re

import rsa
from flask import send_file
from io import BytesIO
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from flask import Blueprint, render_template, request, Response,  session, flash, redirect, url_for, jsonify
import requests
from rsa_utils import generate_rsa_key_pair, rsa_encrypt, serialize_public_key,serialize_private_key
from password_encrypter import encrypt , decrypt
from rsa_utils import rsa_decrypt

views = Blueprint('views', __name__)

# Backend server URL
server_url = 'https://stdapi.hmmbo.com/api'

# Signup route
@views.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        password = encrypt(request.form.get('password'),23)
        confirm_password = encrypt(request.form.get('confirm_password'),23)

        if len(password) <= 5:
            return render_template('signup.html', error=f'Password size should be greater than 5')


        # Send signup request to backend
        try:
            response = requests.post(f'{server_url}/signup', json={
                "email": email,
                "password": password,
                "confirm_password": confirm_password
            })

            if response.status_code == 200:
                flash('Signup Successful! You can now log in.', 'success')
                return redirect(url_for('views.login'))
            else:
                error_data = response.json()
                return render_template('signup.html', error=error_data.get("error", "Unknown error"))
        except requests.exceptions.RequestException as e:
            return render_template('signup.html', error=f'Failed to connect to the server: {str(e)}')

    return render_template('signup.html')

# Login route
@views.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = encrypt(request.form.get('password'), 23)


        # Send login request to backend
        try:
            response = requests.post(f'{server_url}/login', json={
                "email": email,
                "password": password
            })

            if response.status_code == 200:
                user_data = response.json()

                # Store user details in session

                session['auth'] = user_data.get('auth')

                if session['auth']:  # Check if auth is 1
                    session['un_email'] = user_data.get('email')
                    flash('Login Successful! OTP sent.', 'success')
                    return render_template('auth.html')  # Open auth.html directly
                else:
                    session['email'] = user_data.get('email')
                    flash('Login Successful!', 'success')
                    return redirect(url_for('views.homes'))  # Redirect to homes if auth is not 1

            else:
                error_data = response.json()
                return render_template('login.html', error=error_data.get("error", "Unknown error"))

        except requests.exceptions.RequestException as e:
            return render_template('login.html', error=f'Failed to connect to the server: {str(e)}')

    return render_template('login.html')

# Forgot Password route
@views.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        # Get the email from the submitted form
        email = request.form.get('email')

        if email:
            # Send forgot password request to backend
            try:
                response = requests.post(f'{server_url}/forgot_password', json={"email": email})

                if response.status_code == 200:
                    # Check if the response indicates email was found
                    response_data = response.json()
                    if response_data.get("email_found") == "true":
                        flash('OTP sent to your email!', 'success')  # Success message
                        return render_template('forgot_pass.html', message="OTP sent to your email!", message_type="success")

                    else:
                        # Email not found in the database
                        flash('No email found!', 'error')  # Error message
                        return render_template('forgot_pass.html', message="No email found", message_type="error")
                else:
                    error_data = response.json()
                    return render_template('forgot_pass.html', message=error_data.get("error", "Unknown error"), message_type="error")
            except requests.exceptions.RequestException as e:
                return render_template('forgot_pass.html', message=f'Failed to connect to the server: {str(e)}', message_type="error")

        # Error if email is not provided
        return render_template('forgot_pass.html', message='Email not provided', message_type="error")

    # If it's a GET request, just render the form again
    return render_template('forgot_pass.html')



# Home route
@views.route('/', methods=['GET', 'POST'])
def homes():
    email = session.get('email')
    auth = session.get('auth')

    try:
        # Make a POST request to retrieve files
        response = requests.post(f'{server_url}/retrieve_file', json={
            "email": email,
            "auth": auth  # Include authentication status in the request
        })

        if response.status_code == 200:
            data = response.json()
            file_list = data.get('files', [])  # Extract the list of files (name and content)

            # Store file_list in session or pass to the frontend as context
            session['file_list'] = file_list

            # You can now render the homepage template and pass the file list to the frontend
            return render_template('home.html',  email=email, auth=auth, file_list=file_list)

        else:
            # Handle errors returned by the server
            error_data = response.json()
            error_message = error_data.get("error", "Failed to retrieve files.")
            return render_template('home.html',  email=email, auth=auth, file_list=[])

    except requests.exceptions.RequestException as e:
        # Handle network-related errors
        return render_template('home.html', email=email, auth=auth, file_list=[])

    except requests.exceptions.RequestException as e:
        return {"error": f'Failed to connect to the server: {str(e)}'}, 500

    return render_template('home.html', email=email, auth=auth, file_list=file_list)
###
@views.route('/logout', methods=['GET'])
def logout():
    # Clear the session to log the user out
    session.clear()
    flash('You have been logged out successfully.', 'success')
    return redirect(url_for('views.homes'))  # Redirect to the home page or login page
@views.route('/api/toggle_2fa', methods=['POST'])
def toggle_2fa():
    email = request.json.get('email')

    # Check if the email exists in the session
    if email != session.get('email'):
        return jsonify({"error": "Unauthorized access."}), 403

    # Send the toggle request to the backend server running on port 8000
    try:
        response = requests.post(f'{server_url}/toggle_2fa', json={  # Corrected the backend route to /toggle_2fa
            "email": email
        })

        if response.status_code == 200:
            session['auth'] = not session['auth']  # Toggle the 2FA status in the session
            return jsonify({"message": "2FA status updated successfully."}), 200
        else:
            error_data = response.json()
            return jsonify({"error": error_data.get("error", "Failed to update 2FA status.")}), response.status_code

    except requests.exceptions.RequestException as e:
        return jsonify({"error": f'Failed to connect to the server: {str(e)}'}), 500

@views.route('/auth', methods=['GET', 'POST'])
def auth():
    # Your authentication logic here
    return render_template('auth.html')
# views.py
@views.route('/verify_otp', methods=['POST'])
def verify_otp():
    combined_otp = request.form.get('otp')  # Get the complete OTP

    # Send the OTP to the backend running at port 8000 for verification
    try:
        response = requests.post(f'{server_url}/auth', json={"otp": combined_otp,"email": session.get('un_email')})

        if response.status_code == 200:
            session['email'] = session.get('un_email')
            flash('Login successful!', 'success')
            return redirect(url_for('views.homes'))  # Redirect to home on success
        else:
            error_data = response.json()
            flash(error_data.get("error", "Invalid OTP. Please try again."), 'error')
            return redirect(url_for('views.login'))  # Redirect back to login on error

    except requests.exceptions.RequestException as e:
        flash(f'Failed to connect to the server: {str(e)}', 'error')
        return redirect(url_for('views.login'))  # Redirect back to login on error

# Route to handle file uploads from the frontend
@views.route('/api/upload_file', methods=['POST'])
def upload_file():
    email = session.get('email')
    auth = session.get('auth')

    if not email:
        return jsonify({"error": "User is not logged in"}), 403

    # Retrieve file data from request.json (as it's coming from the frontend as JSON)
    data = request.json
    filename = data.get('filename')
    file_content = data.get('content')

    # Debugging logs to verify data is being correctly received
    print(f"\nUploader Info\nEmail: {email}\nAuth: {auth}\nFilename: {filename}\n\n")

    if not filename or not file_content:
        return jsonify({"error": "Missing required fields"}), 400

    # Choose RSA key size based on auth (1 for 2048, else 1024)
    key_size = 2048 if auth == 1 else 1024
    encryption_method = "RSA"

    # Generate RSA key pair
    private_key, public_key = generate_rsa_key_pair(key_size)

    encrypted_content = rsa_encrypt(public_key, file_content)

    # Serialize the public key to send to the backend along with the encrypted content
    public_key_serialized = serialize_public_key(public_key)
    private_key_serialized = serialize_private_key(private_key)
    print("\n\nEncrypted file content is :\n",encrypted_content,"\n")

    (s_public_key, private_key) = rsa.newkeys(2048)
    digest = hashlib.sha256(encrypted_content).digest()
    signature = rsa.sign(digest, private_key, 'SHA-256')
    # Send the encrypted data and other details to the backend (running on port 8000)
    try:
        response = requests.post(f'{server_url}/upload_file', json={
            "email": email,
            "filename": filename,
            "content": encrypted_content.hex(),  # Send as hex for easy JSON transmission
            "public_key": public_key_serialized.decode('utf-8'),  # Send public key as a string
            "encryption_method": encryption_method,
            "key_size": key_size,
            "private_key":private_key_serialized.decode('utf-8'),
            "signature": signature.hex(),  # Convert signature to hex
            "digest": digest.hex(),  # Convert digest to hex
            "sign_public_key": s_public_key.save_pkcs1().decode('utf-8')
        })

        if response.status_code == 200:
            return jsonify({"message": f"File uploaded successfully with RSA encryption (key size: {key_size})"}), 200
        else:
            error_data = response.json()
            return jsonify({"error": error_data.get("error", "Failed to upload the file")}), response.status_code

    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Failed to connect to the backend: {str(e)}"}), 500

@views.route('/preview_file', methods=['POST'])
def preview_file():
    email = session.get('email')  # Retrieve the email from the session

    if not email:
        flash("You must be logged in to preview files.", "error")
        return redirect(url_for('views.login'))  # Redirect to login if not authenticated

    filename = request.json.get('filename')  # Retrieve filename from JSON payload

    if not filename:
        return jsonify({"error": "Filename is required."}), 400

    # Prepare the request to the backend API
    api_url = f'{server_url}/get_file_content'
    payload = {'email': email, 'filename': filename}

    try:
        # Make a POST request with the JSON payload
        response = requests.post(api_url, json=payload)

        if response.status_code == 200:
            # Extract the content, public key, and private key from the response
            data = response.json()
            encrypted_content = data['content']
            public_key = data['public_key']
            private_key = data['private_key']
            print("Encryption Details")
            print(f"Encrypted Content: {encrypted_content},\n Type: {type(encrypted_content)}\n\n")
            print(f"Public Key: {public_key}\n, Type: {type(public_key)}\n\n")
            print(f"Private Key: {private_key}\n, Type: {type(private_key)}\n\n")
            # Clean the encrypted content
            hex_content = encrypted_content.replace('\\x', '')  # Ensure this is necessary
            print('hex_content: ',hex_content,'\n\n')
            try:
                encrypted_bytes = bytes.fromhex(hex_content)  # Convert hex to bytes
                print('\nEncrypted_bytes',encrypted_bytes,'\n\n')
            except ValueError as e:
                flash("Invalid encrypted content format: " + str(e), "error")
                return redirect(url_for('views.homes'))

            # Load the private key
            try:
                private_key_obj = serialization.load_pem_private_key(
                    private_key.encode(),  # Convert private key to bytes
                    password=None
                )
            except ValueError as e:
                flash("Invalid private key format: " + str(e), "error")
                return redirect(url_for('views.homes'))

            # Decrypt the file content using the private key
            try:
                decrypted_content = rsa_decrypt(private_key_obj, encrypted_bytes)
                print('\nDecrypted file content:', decrypted_content,'\n\n')
            except Exception as e:
                flash(f"Decryption failed: {str(e)}", "error")
                return redirect(url_for('views.homes'))

            # Render a template and pass the decrypted content to it
            return jsonify({"message": f"{decrypted_content}"}), 200

        else:
            # Handle error response from backend
            error_data = response.json()
            flash(error_data.get("error", "Failed to retrieve file content."), "error")
            return redirect(url_for('views.homes'))
    except requests.exceptions.RequestException as e:
        flash(f"Failed to connect to the server: {str(e)}", "error")
        return redirect(url_for('views.homes'))

@views.route('/delete_file', methods=['POST'])
def delete_file():

    email = session.get('email')
    if not email:
        flash("You must be logged in to delete files.", "error")
        return redirect(url_for('views.login'))  # Redirect to login if not authenticated


    filename = request.json.get('filename')  # Retrieve filename from JSON payload
    if not filename:
        return jsonify({"error": "Filename is required."}), 400

    # Prepare the request to the backend API
    api_url = f'{server_url}/delete_file'
    payload = {'email': email, 'filename': filename}

    try:
        # Make a DELETE request with the JSON payload

        response = requests.post(api_url, json=payload)

        if response.status_code == 200:
            # Handle successful deletion
            data = response.json()
            flash(data.get("message", "File deleted successfully."), "success")
            return jsonify({"message": "File deleted successfully."}), 200

        else:
            # Handle error response from backend
            error_data = response.json()
            flash(error_data.get("error", "Failed to delete the file."), "error")
            return jsonify({"error": "Failed to delete the file."}), 400
    except requests.exceptions.RequestException as e:
        flash(f"Failed to connect to the server: {str(e)}", "error")
        return jsonify({"error": f"Failed to connect to the server: {str(e)}"}), 500
