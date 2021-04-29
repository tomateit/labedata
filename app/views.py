from app import app
from flask import render_template, request, redirect, url_for, flash, make_response, session
from flask_login import login_required, login_user, current_user, logout_user
from .forms import LoginForm



@app.route('/')
def index():
    return render_template('index.html', name='user1')

# @app.route('/login/', methods=['post', 'get'])
# def login():
#     if current_user.is_authenticated:
# 	return redirect(url_for('admin'))
#     form = LoginForm()
#     if form.validate_on_submit():
# 	user = db.session.query(User).filter(User.username == form.username.data).first()
# 	if user and user.check_password(form.password.data):
# 	    login_user(user, remember=form.remember.data)
# 	     return redirect(url_for('admin'))
# 	flash("Invalid username/password", 'error')
# 	return redirect(url_for('login'))
#     return render_template('login.html', form=form)


# @app.route('/logout/')
# @login_required
# def logout():
#     logout_user()
#     flash("You have been logged out.")
#     return redirect(url_for('login'))




@app.route('/task', methods=['POST', 'GET'])
def article():
    if request.method == 'POST':
	res = make_response("")

	res.headers['location'] = url_for('task')
	return res, 302

    return render_template('task.html')



