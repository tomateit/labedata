from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from werkzeug.utils import secure_filename

from labedata.db import get_db
from labedata.db.models import Dataset

bp = Blueprint('dataset', __name__, url_prefix='/dataset')

# DATASET MANAGEMENT

@bp.route("/new", methods=["GET", "POST"])
def dataset_new():
    #!TODO validate user access
    if request.method == 'POST':
        f = request.files['dataset']
        filepath = "../input/"+ secure_filename(f.filename)
        request["filepath"] = filepath
        f.save(filepath)
        ds = Dataset.from_form(request)
        return redirect(url_for(f"dataset/{ds.dataset_id}"))
    else:
        return render_template('dataset_new.html', error=error)

@bp.route("/<string:dataset_id>", methods=["GET", "PATCH", "DELETE"])
def dataset(dataset_id):
    #TODO! Only author can access and modify dataset meta
    ds = Dataset.by_id(dataset_id)
    if not ds:
        return redirect(404)
    if request.method == "GET":
        return render_template('dataset.html', dataset=ds)
    if request.method == "PATCH":
        ds.patch(request.form)
        return redirect(url_for(f"dataset/{ds.dataset_id}"))
    if request.method == "DELETE":
        # only author can delete dataset
        error = ds.delete(g.user)
        i

@bp.route("/<string:dataset>/<uuid:entity>", methods=["GET", "POST", "PATCH", "DELETE"])
def entity_page(dataset, entity):
    #!TODO validate that user was assigned to this dataset
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