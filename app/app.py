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

@app.route("/", methods=["GET", "POST"])
def index_page(result=""):
    if 'username' in session:
        return show_index_page()
    else:
        return redirect_to_login_form()

from flask import make_response
@app.route("/login", methods=["GET", "POST"])
def login_page(result=""):
    error = None
    if request.method == 'POST':
        username, password = request.form['username'], request.form['password']
        error = validate_credentials(username, password)
        if error is None:
            session['username'] = username
            # resp = make_response(render_template("index.html"))
            # resp.set_cookie('username', 'the username')
            return redirect(url_for('index_page'))
            return resp
    # the code below is executed if the request method
    # was GET or the credentials were invalid
    return render_template('login.html', error=error)


from werkzeug.utils import secure_filename
@app.route('/dataset/new', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['dataset']
        f.save('../input/'+ secure_filename(f.filename))
    else:
        return render_template('dataset_new.html', error=error)


@app.route("/dataset/<dataset>/<entity>", methods=["GET", "POST"])
def index_page(dataset, entity):

    if request.method == "POST":
        result = request.form["result"]
        print("FORM:", result)
        r_ = data.pop(0)
        r_["accessed"] = result
        csv_writer.writerow(r_.values())
    else:
        print("First run")

    if not len(data):
        return render_template("dataset_entity.html", 
            data="Большое спасибо за труд! На сегодня всё."
        )
    else :
        d = data[0]["text"]
        return render_template("dataset_entity.html", data=d, count_left=str(len(data)))



