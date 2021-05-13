
import os
from labedata import create_app
import logging
from dotenv import load_dotenv
load_dotenv()

if __name__ == "__main__":
    try:
        app = create_app()
        app.run(os.environ.get("IP"), os.environ.get("PORT"), debug=True)
    except Exception as e:
        logging.exception(e)
    finally:
        pass
        # print("CLOSING FILES")
        # halt_time = datetime.datetime.now().isoformat()
        # pd.DataFrame(data).to_csv(f"data_chunk_{halt_time}.csv", index=False, quoting=csv.QUOTE_NONNUMERIC)
        # fout_.close()