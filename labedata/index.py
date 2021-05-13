from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from .models.dataset_factory import DatasetFactory as Dataset
from .auth import login_required
from .db import get_db

bp = Blueprint('index', __name__)

@bp.route("/", methods=["GET"])
@login_required
def index():
    user = g.user
    datasets = Dataset.fetch_by_author_id(user["user_id"])
    # fetch assigned datasets
    return render_template('index.html', user=user, datasets=datasets)
