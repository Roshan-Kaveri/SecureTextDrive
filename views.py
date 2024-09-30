from flask import  Blueprint , render_template , request , session, jsonify , redirect , url_for , flash
from flask_mail import Message
from otp_utils import generate_otp, send_otp_email, otp_storage
from mail_config import mail

views = Blueprint(__name__ , "views")



@views.route("/profile")
def profile():
    args = request.args
    name = args.get('name')
    return render_template("index.html", name=name)

@views.route("/json")
def get_json():
    return jsonify({'name': 'tim', 'coolness': 10})

@views.route("/data")
def get_data():
    data = request.json
    return jsonify(data)

@views.route("/go-home")
def go_home():
    return redirect(url_for("views.home"))


@views.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Dummy authentication logic
        if email == 'aha' and password == 'a':
            flash('Login Successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password', 'error')

    return render_template('login.html')

@views.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Dummy authentication logic
        if email == 'aha' and password == 'a':
            flash('Login Successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password', 'error')

    return render_template('signup.html')    

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

@views.route('/generate-otp', methods=['GET'])
def generate_otp_for_email():
    email = request.args.get('email')

    if not email:
        return jsonify({"error": "Email address is required"}), 400

    otp = generate_otp()
    otp_storage[email] = otp  # Store the OTP with the email as the key
    session['email'] = email  # Store the email in the session to use for verification

    # Send the OTP via email using the imported `mail` instance
    if send_otp_email(mail, email, otp):
        return redirect(url_for('views.auth'))  # Redirect to the OTP verification page
    else:
        return jsonify({"error": "Failed to send OTP email"}), 500


@views.route('/auth', methods=['GET', 'POST'])
def auth():
    if request.method == 'POST':
        email = session.get('email')  # Retrieve email from session
        if not email:
            return "Session expired, please try again.", 400

        # Concatenate all the OTP input fields into a single string
        entered_otp = ''.join([
            request.form.get('number1', ''),
            request.form.get('number2', ''),
            request.form.get('number3', ''),
            request.form.get('number4', ''),
            request.form.get('number5', ''),
            request.form.get('number6', '')
        ])

        # Verify OTP
        stored_otp = otp_storage.get(email)
        if stored_otp == entered_otp:
            return "OTP verified successfully!", 200
        else:
            return "Invalid OTP, please try again.", 400

    return render_template('auth.html')

@views.route('/', methods=['GET', 'POST'])
def homes():
      return render_template('home.html');     