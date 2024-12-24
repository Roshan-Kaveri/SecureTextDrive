import os

from flask import Flask , session
# FrontENd

from views import views

from flask import *

app = Flask(__name__)
app.register_blueprint(views, url_prefix="/")
app.secret_key = 'abcdlala'

from flask import Flask, session
from views import views


# No need to run app.run() on Vercel; Vercel will handle it.
# app = app  # This ensures Vercel recognizes it as the main app instance


# if __name__ == '__main__':
#     app.run(debug=True, port=5000)


if __name__ == "__main__":
    from waitress import serve

    app.run(debug=True, host="0.0.0.0", port=5000)
    serve(app, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))