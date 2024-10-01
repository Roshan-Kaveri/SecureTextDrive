from flask import Flask , session
from views import views
from flask_mail import *
from mail_config import mail
from mail_settings import *
from flask import *

app = Flask(__name__)
app.register_blueprint(views, url_prefix="/")
app.secret_key = 'abcdlala'

app.config['MAIL_SERVER'] = MAIL_SERVER
app.config['MAIL_PORT'] = MAIL_PORT
app.config['MAIL_USERNAME'] = MAIL_USERNAME
app.config['MAIL_PASSWORD'] = MAIL_PASSWORD
app.config['MAIL_USE_TLS'] = MAIL_USE_TLS
app.config['MAIL_USE_SSL'] = MAIL_USE_SSL

mail.init_app(app)

if __name__ == '__main__':
    app.run(debug=True, port=8000)

