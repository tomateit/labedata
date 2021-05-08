from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from labedata.auth import login_required
from labedata.db import get_db

bp = Blueprint('index', __name__)


@bp.route("/", methods=["GET", "POST"])
@login_required
def index():
    user = g.user
    datasets = Dataset.fetch_by_author_id(user["user_id"])
    return render_template('index.html', user=user, datasets=datasets)
