import logging
from flask import (
    current_app, 
    Blueprint, 
    flash, 
    g, 
    redirect, 
    render_template, 
    request, 
    session, 
    url_for,
    send_file
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
        logging.info(f"File will be saved as {input_path}")
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
    if not ds:
        logging.warning(f"Requested nonexistent dataset: {dataset_id}")
        return render_template("message.html", title="Ошибка 404", message="Такой датасет не найден"), 404
    if request.method == "GET":
        return render_template("dataset.html", dataset=ds)
    # if request.method == "PATCH":
    #     ds.patch(request.form)
    #     return redirect(url_for(f"dataset/{ds.dataset_id}"))
    if request.method == "DELETE":
        # only author can delete dataset
        if ds.author_id == g.user["user_id"]:
            logging.info(f"Got dataset deletion request for {dataset_id}")
            ds.delete()
            return redirect(url_for("index"), 308)
        else:
            logging.warning(f"Unauthorized dataset deletion request for {dataset_id} from user {g.user['user_id']}")
            return render_template("message.html", title="Нет прав", message="Вы не в праве делать такой запрос"), 403


@bp.route("/<string:dataset_id>/download", methods=["GET"])
@login_required
def download_output(dataset_id):
    ds = Dataset.fetch_by_id(dataset_id)
    logging.debug(f"Requested downloading {dataset_id}")
    if not ds:
        logging.warning(f"Requested nonexistent dataset: {dataset_id}")
        return render_template("message.html", title="Ошибка 404", message="Такой датасет не найден"), 404
    if request.method == "GET":
        output_path = ds.get_location()
        logging.info(f"Sending file from {output_path}")
        return send_file(output_path, as_attachment=True)


@bp.route("/<string:dataset_id>/next", methods=["GET"])
@login_required
def next_entity(dataset_id):
    next_entity_id = Dataset.fetch_by_id(dataset_id).next_entity_for_user_id(g.user["user_id"])
    logging.debug(f"Next entity in dataset {dataset_id} for user {g.user['user_id']} {'exists' if next_entity_id else 'not found'}")
    if next_entity_id:
        return redirect(url_for("dataset.entity_page", dataset_id=dataset_id, entity_id=next_entity_id))
    else:
        logging.info(f"No more entitiles left for user {g.user['user_id']}")
        return render_template("message.html", title="Разметка завершена", message="Все сущности размечены. Спасибо за работу!"), 303


@bp.route("/<string:dataset_id>/<string:entity_id>", methods=["GET", "POST", "PATCH", "PUT", "DELETE"])
@login_required
def entity_page(dataset_id, entity_id):
    ds = Dataset.fetch_by_id(dataset_id)
    if not ds:
        logging.warning(f"Requested nonexistent dataset: {dataset_id}")
        return render_template("message.html", title="Ошибка 404", message="Такой датасет не найден"), 404
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
        logging.debug("REQUEST BODY: {request_body}")
        ds.label_entity(entity_id, request_body["label_field"], user_id=g.user["user_id"])
        return redirect(url_for("dataset.next_entity", dataset_id=dataset_id), 303)

    # if request.method == "PUT":
    #     entity = ds.modify_entity(entity_id, request.form)
    #     return render_template("dataset_entity.html", entity=entity, dataset=ds)

    # if request.method == "DELETE":
    #     ds.delete_entity(entity_id)
    #     return redirect(url_for("dataset.next_entity", dataset_id=dataset_id), 303)

