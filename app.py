from flask import Flask , session
from views import views
from flask_mail import *
from mail_config import mail
from mail_settings import * 

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

@app.route('/email')
def index():
    msg = Message('subject', sender = 'support@hmmbo.com', recipients=['mumbosmp8@gmail.com','Sriramavate2@gmail.com'])
    msg.body = 'OTP BOLO BHAI'
    mail.send(msg)
    return "Mail Sent, Please check the mail id"

if __name__ == '__main__':
    app.run(debug=True, port=8000)

