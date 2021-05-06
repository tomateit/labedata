


@app.route("/", methods=["GET", "POST"])
def index_page(result=""):
    if 'username' in session:
        return show_index_page()
    else:
        return redirect_to_login_form()