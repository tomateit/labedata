from flask import Flask
from flask import Flask, render_template, request
import pandas as pd
import datetime
import csv

app = Flask(__name__)

launch_time = datetime.datetime.now().isoformat()
fout_ = open(f"train_data_results_{launch_time}.csv", "w")
csv_writer = csv.writer(fout_)

data = pd.read_csv("./train_data.csv")
data = data[["label", "text"]].to_dict("records")[:2]

@app.route("/", methods=["GET", "POST"])
def index_page(result=""):
    if not len(data):
        return render_template("index.html", 
            data="Большое спасибо за труд! На сегодня всё."
        )
    else :
        d = data[0]["text"]

    if request.method == "POST":
        result = request.form["result"]
        print("FORM:", result)
        r_ = data.pop(0)
        r_["accessed"] = result
        csv_writer.writerow(r_.values())
        return render_template("index.html", 
            data=d
        )
    else:
        print("First run")
        return render_template("index.html", 
            data=d
        )
    


# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=80, debug=False)


if __name__ == "__main__":
    try:
        app.run(debug=True)
    except Exception:
        print(Exception)
    finally:
        print("CLOSING FILES")
        halt_time = datetime.datetime.now().isoformat()
        pd.DataFrame(data).to_csv(f"data_chunk_{halt_time}.csv", index=False, quoting=csv.QUOTE_NONNUMERIC)
        fout_.close()