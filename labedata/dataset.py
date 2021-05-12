from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from werkzeug.utils import secure_filename

from labedata.db import get_db
from labedata.db.models import Dataset

bp = Blueprint("dataset", __name__, url_prefix="/dataset")

# DATASET MANAGEMENT

@bp.route("/new", methods=["GET", "POST"])
@login_required
def dataset_new():
    #!TODO validate user access
    if request.method == "POST":
        f = request.files["dataset"]
        input_path = "../input/"+ secure_filename(f.filename)
        f.save(filepath)
        request["input_path"] = input_path
        ds = Dataset.new(request)
        return redirect(url_for(f"dataset/{ds.dataset_id}"))
    else:
        return render_template("dataset_new.html", error=error)

@bp.route("/<string:dataset_id>", methods=["GET", "PATCH", "DELETE"])
@login_required
def dataset(dataset_id):
    #TODO! Only author can access and modify dataset meta
    ds = Dataset.fetch_by_id(dataset_id)
    if not ds:
        return redirect(404)
    if request.method == "GET":
        return render_template("dataset.html", dataset=ds)
    if request.method == "PATCH":
        ds.patch(request.form)
        return redirect(url_for(f"dataset/{ds.dataset_id}"))
    if request.method == "DELETE":
        # only author can delete dataset
        error = ds.delete(g.user)
        return redirect(url_for("index"))

@bp.route("/<string:dataset>/next", methods=["GET"])
@login_required
def next_entity(dataset):
    next_entity = Dataset(dataset).next_entity_for_user_id(g.user.user_id)
    return redirect(entity_page, dataset=dataset, entity=next_entity)


@bp.route("/<string:dataset>/<uuid:entity>", methods=["GET", "POST", "PATCH", "PUT", "DELETE"])
@login_required
def entity_page(dataset, entity):
    #!TODO validate that user was assigned to this dataset
    # GET and PUT do not redirect, show requested (possibly modified) entity again
    # POST (UPSERT) redirects to newly created entity
    # DELETE and PATCH redirect to NEXT
    if request.method == "GET":
        entity = Dataset(dataset).fetch_entity(entity)
        return render_template("processing/dataset_entity", entity=entity)

    if request.method == "POST":
        entity = Dataset(dataset).upsert_entity(request.form)
        return render_template("processing/dataset_entity", entity=entity)
    
    # main labeling action
    if request.method == "PATCH":
        Dataset(dataset).label_entity(entity, label, user=g.user.user_id)
        return redirect(url_for("next_entity"))

    if request.method == "PUT":
        entity = Dataset(dataset).modify_entity(entity, request.form)
        return render_template("processing/dataset_entity", entity=entity)

    if request.method == "DELETE":
        Dataset(dataset).delete_entity(entity)
        return redirect(url_for("next_entity"))

