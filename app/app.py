import os
import config

app = Flask(__name__)
app.config.from_object(os.environ.get('FLASK_ENV') or 'config.DevelopementConfig')

from . import views

from flask import Flask
from flask import Flask, render_template, request
import pandas as pd
import datetime
import csv
import os
import pathlib


app = Flask(__name__)

launch_time = datetime.datetime.now().isoformat()
fout_ = open(f"./output/train_data_results.csv", "w")
csv_writer = csv.writer(fout_)

data = pd.read_csv("./data_chunk_2020-12-09T14:49:08.148942.csv")
data = data[["label", "text"]].to_dict("records")


@app.route("/", methods=["GET", "POST"])
def index_page(result=""):

    if request.method == "POST":
        result = request.form["result"]
        print("FORM:", result)
        r_ = data.pop(0)
        r_["accessed"] = result
        csv_writer.writerow(r_.values())
    else:
        print("First run")

    if not len(data):
        return render_template("index.html", 
            data="Большое спасибо за труд! На сегодня всё."
        )
    else :
        d = data[0]["text"]
        return render_template("index.html", data=d, count_left=str(len(data)))



