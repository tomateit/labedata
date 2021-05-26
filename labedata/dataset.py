from flask import (
    current_app, Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from pathlib import Path
from werkzeug.utils import secure_filename
from .db import get_db
from .models.dataset_factory import incoming_dataset_fields, DatasetFactory as Dataset
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
        #? Maybe consider appending hash
        filename = g.user["user_id"] + "-" + secure_filename(thefile.filename)
        input_path = Path(current_app.config["INPUT_DIR"], filename)
        print("File will be saved as", input_path)
        thefile.save(input_path)
        # then dataset will be created
        #TODO proper form validation
        converted_form = { key: form[key].data for key in incoming_dataset_fields}
        ds = Dataset.create(**converted_form, input_path=filename, author_id=g.user["user_id"])
        return redirect(url_for(f"dataset.dataset", dataset_id=ds.dataset_id))
    else:
        return render_template("dataset_new.html", form=form)

@bp.route("/<string:dataset_id>", methods=["GET", "PATCH", "DELETE"])
@login_required
def dataset(dataset_id):
    #TODO! Only author can access and modify dataset meta
    ds = Dataset.fetch_by_id(dataset_id)
    print(f"REquested dataset {dataset_id}, got {ds}")
    if not ds:
        return redirect(url_for("index"), code=404)
    if request.method == "GET":
        return render_template("dataset.html", dataset=ds)
    # if request.method == "PATCH":
    #     ds.patch(request.form)
    #     return redirect(url_for(f"dataset/{ds.dataset_id}"))
    if request.method == "DELETE":
        # only author can delete dataset
        # validate it here, model do not track permissions
        ds.delete()
        return redirect(url_for("index"), 308) # this wont work cuz the request was from fetch

@bp.route("/<string:dataset_id>/next", methods=["GET"])
@login_required
def next_entity(dataset_id):
    next_entity_id = Dataset.fetch_by_id(dataset_id).next_entity_for_user_id(g.user["user_id"])
    print(f"Next entity {'exists' if next_entity_id else 'not found'}")
    if next_entity_id:
        return redirect(url_for("dataset.entity_page", dataset_id=dataset_id, entity_id=next_entity_id))
    else:
        print("No more entitiles left")
        return redirect(url_for("index"), 303)


@bp.route("/<string:dataset_id>/<string:entity_id>", methods=["GET", "POST", "PATCH", "PUT", "DELETE"])
@login_required
def entity_page(dataset_id, entity_id):
    ds = Dataset.fetch_by_id(dataset_id)
    if not ds:
        print(f"Dataset {dataset_id} not found")
        return redirect(url_for("index"), code=404)
    #!TODO validate that user was assigned to this dataset
    # GET and PUT do not redirect, show requested (possibly modified) entity again
    # POST (UPSERT) redirects to newly created entity
    # DELETE and PATCH redirect to NEXT
    if request.method == "GET":
        entity = ds.get_entity(entity_id)
        return render_template("dataset_entity.html", entity=entity, dataset=ds)

    # if request.method == "POST":
    #     entity = ds.upsert_entity(request.form)
    #     return render_template("dataset_entity.html", entity=entity, dataset=ds)
    
    # main labeling action
    if request.method == "PATCH":
        request_body = request.json
        print("REQ:", request_body)
        ds.label_entity(entity_id, request_body["label_field"], user_id=g.user["user_id"])
        return redirect(url_for("dataset.next_entity", dataset_id=dataset_id), 303)

    # if request.method == "PUT":
    #     entity = ds.modify_entity(entity_id, request.form)
    #     return render_template("dataset_entity.html", entity=entity, dataset=ds)

    # if request.method == "DELETE":
    #     ds.delete_entity(entity_id)
    #     return redirect(url_for("dataset.next_entity", dataset_id=dataset_id), 303)

