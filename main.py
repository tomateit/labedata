
import os
from app import app, db


if __name__ == "__main__":
    try:
        app.run(os.environ.get("IP"), debug=True)
    except Exception:
        print(Exception)
    finally:
        pass
        # print("CLOSING FILES")
        # halt_time = datetime.datetime.now().isoformat()
        # pd.DataFrame(data).to_csv(f"data_chunk_{halt_time}.csv", index=False, quoting=csv.QUOTE_NONNUMERIC)
        # fout_.close()