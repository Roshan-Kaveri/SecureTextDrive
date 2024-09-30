from flask import  Blueprint , render_template , request , jsonify , redirect , url_for , flash

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

@views.route('/auth', methods=['GET', 'POST'])
def auth():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Dummy authentication logic
        if email == 'aha' and password == 'a':
            flash('Login Successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password', 'error')

    return render_template('auth.html')           

@views.route('/', methods=['GET', 'POST'])
def homes():
      return render_template('home.html');     