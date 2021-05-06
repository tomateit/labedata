import os
import config
import datetime
import pathlib

from flask import Flask, render_template, request
from flask import abort, redirect, url_for, session

from . import views

app = Flask(__name__)
app.config.from_object(os.environ.get('FLASK_ENV') or 'config.DevelopementConfig')
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/' #! replace


launch_time = datetime.datetime.now().isoformat()



# from flask import make_response
# @app.route("/login", methods=["GET", "POST"])
# def login(result=""):
#     error = None
#     if request.method == 'POST':
#         username, password = request.form['username'], request.form['password']
#         error = validate_credentials(username, password)
#         if error is None:
#             session['username'] = username
#             # resp = make_response(render_template("index.html"))
#             # resp.set_cookie('username', 'the username')
#             return redirect(url_for('index_page'))
#             return resp
#     # the code below is executed if the request method
#     # was GET or the credentials were invalid
#     return render_template('login.html', error=error)










