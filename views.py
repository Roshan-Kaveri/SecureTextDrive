from flask import  Blueprint , render_template , request , session, jsonify , redirect , url_for , flash
from flask_mail import Message
from otp_utils import generate_otp, send_otp_email, otp_storage
from mail_config import mail
import psycopg2

views = Blueprint(__name__ , "views")

# Database connection details
hostname = 'postgresql-ascscs.alwaysdata.net'
database = 'ascscs_securedrive'
username = 'ascscs'
pwd = '@7sdDgVUuhCXjD6'
port_id = 5432

#signup
@views.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        print("POST request received")  # Check if the POST request is being processed

        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        action = request.form.get('action')

        print(f"Email: {email}, Password: {password}, Action: {action}")  # Log form data

        # Check for the signup action
        if action == 'signup':
            # Check if passwords match
            if password != confirm_password:
                print("Passwords do not match")
                return render_template('signup.html', error="Passwords do not match")


            # Database insertion logic
            try:
                print("Connecting to database...")
                conn = psycopg2.connect(
                    host=hostname,
                    dbname=database,
                    user=username,
                    password=pwd,
                    port=port_id
                )
                cur = conn.cursor()

                # Check if the email already exists
                print("Checking if email exists...")
                cur.execute('SELECT * FROM USERS WHERE email = %s', (email,))
                if cur.fetchone() is not None:
                    print("Email already exists")
                    return render_template('signup.html', error="Email already exists")


                # Insert new user into the database
                print("Inserting user into database...")
                insert_script = 'INSERT INTO USERS(email, password, auth) VALUES(%s, %s, %s)'
                insert_values = (email, password, True)
                cur.execute(insert_script, insert_values)
                conn.commit()

                cur.close()
                conn.close()

                flash('Signup Successful! You can now log in.', 'success')
                return redirect(url_for('views.login'))

            except Exception as error:
                print("Database error:", error)
                return render_template('signup.html', error="An error occurred during signup")


    return render_template('signup.html')

@views.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        try:
            # Connect to the database
            conn = psycopg2.connect(
                host=hostname,
                dbname=database,
                user=username,
                password=pwd,
                port=port_id
            )
            cur = conn.cursor()

            # Check if the email and password match any entry in the database
            cur.execute('SELECT email, password, auth FROM USERS WHERE email = %s AND password = %s', (email, password))
            user = cur.fetchone()

            cur.close()
            conn.close()
            print("user = ", user)

            if user:
                # Store email and auth in session
                session['email'] = user[0]
                session['auth'] = bool(user[2])  # Convert auth to a boolean

                if session['auth']:
                    flash('Login Successful! OTP sent.', 'success')
                    gen_otp(user[0])  # Ensure gen_otp is defined correctly
                    return redirect(url_for('views.auth'))
                else:
                    flash('Login Successful!', 'success')
                    return redirect(url_for('views.homes'))
            else:
                flash('Invalid email or password', 'error')
                return render_template('login.html', error="Invalid credentials")

        except Exception as error:
            print("Database error:", error)
            flash("An error occurred during login", 'error')
            return render_template('login.html', error="Database error")

    return render_template('login.html')

@views.route('/forgot_password', methods=['GET', 'POST'])
def fpass():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Dummy authentication logic
        if email == 'aha' and password == 'a':
            flash('Login Successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password', 'error')
    return render_template('forgot_pass.html')

def gen_otp(email):
    if not email:
        return jsonify({"error": "Email address is required"}), 400

    otp = generate_otp()
    otp_storage[email] = otp  # Store the OTP with the email as the key
    session['email'] = email  # Store the email in the session to use for verification

    # Send the OTP via email using the imported `mail` instance
    if send_otp_email(mail, email, otp):
        return redirect(url_for('views.auth'))
    else:
        return jsonify({"error": "Failed to send OTP email"}), 500

@views.route('/auth', methods=['GET', 'POST'])
def auth():
    print("auth route hit")  # Check if the route is called
    email = session.get('email')
    print("Session email:", email)  # Check if email is retrieved from session

    if not email:
        print('Session expired, please log in again.', 'error')

        return redirect(url_for('views.login'))

    if request.method == 'POST':
        print("POST request received")  # Verify form submission
        entered_otp = ''.join([
            request.form.get('number1', '').strip(),
            request.form.get('number2', '').strip(),
            request.form.get('number3', '').strip(),
            request.form.get('number4', '').strip(),
            request.form.get('number5', '').strip(),
            request.form.get('number6', '').strip()
        ])
        print("Entered OTP:", entered_otp)  # Check entered OTP

        if len(entered_otp) != 6 or not entered_otp.isdigit():
            flash('Invalid OTP format. Please enter all 6 digits.', 'error')
            return render_template('auth.html')

        stored_otp = otp_storage.get(email)
        print("Stored OTP:", stored_otp, "OTP Storage:", otp_storage)  # Check OTP storage

        if stored_otp == entered_otp:
            otp_storage.pop(email, None)
            flash('OTP verified successfully!', 'success')
            return redirect(url_for('views.homes'))
        else:
            print("Invalid OTP")
            # Stay on the same page and pass the error message
            return render_template('auth.html', error="Invalid OTP. Please try again.")


    return render_template('auth.html')


@views.route('/', methods=['GET', 'POST'])
def homes():
    email = session.get('email')
    auth = session.get('auth')
    return render_template('home.html', email=email, auth=auth)