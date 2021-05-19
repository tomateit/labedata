from flask import (
    current_app, Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from pathlib import Path
from werkzeug.utils import secure_filename
from .db import get_db
from .models.dataset_factory import DatasetFactory as Dataset
from .forms import NewDatasetForm
from .auth import login_required

# DATASET MANAGEMENT
bp = Blueprint("dataset", __name__, url_prefix="/dataset")

@bp.route("/new", methods=["GET", "POST"])
@login_required
def dataset_new():
    error=None
    form=NewDatasetForm()
    #!TODO validate user access
    if request.method == "POST":
        #!TODO validate form
        # file will be saved anyway
        thefile = request.files["dataset"]
        filename = secure_filename(thefile.filename)
        input_path = Path(current_app.config["INPUT_DIR"], filename)
        print("File will be saved as", input_path)
        thefile.save(input_path)
        request["input_path"] = filename
        # then dataset will be created
        ds = Dataset.create(request)
        return redirect(url_for(f"dataset/{ds.dataset_id}"))
    else:
        return render_template("dataset_new.html", form=form)

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
    next_entity = Dataset.fetch_by_id(dataset).next_entity_for_user_id(g.user.user_id)
    return redirect(entity_page, dataset=dataset, entity=next_entity)


@bp.route("/<string:dataset>/<uuid:entity>", methods=["GET", "POST", "PATCH", "PUT", "DELETE"])
@login_required
def entity_page(dataset, entity):
    #!TODO validate that user was assigned to this dataset
    # GET and PUT do not redirect, show requested (possibly modified) entity again
    # POST (UPSERT) redirects to newly created entity
    # DELETE and PATCH redirect to NEXT
    if request.method == "GET":
        entity = Dataset.fetch_by_id(dataset).get_entity(entity)
        return render_template("dataset_entity", entity=entity)

    if request.method == "POST":
        entity = Dataset.fetch_by_id(dataset).upsert_entity(request.form)
        return render_template("dataset_entity", entity=entity)
    
    # main labeling action
    if request.method == "PATCH":
        Dataset.fetch_by_id(dataset).label_entity(entity, label, user=g.user.user_id)
        return redirect(url_for("next_entity"))

    if request.method == "PUT":
        entity = Dataset.fetch_by_id(dataset).modify_entity(entity, request.form)
        return render_template("dataset_entity", entity=entity)

    if request.method == "DELETE":
        Dataset(dataset).delete_entity(entity)
        return redirect(url_for("next_entity"))

