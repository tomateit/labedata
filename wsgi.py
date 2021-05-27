"""
Labeling application root file
"""
# import logging
from dotenv import load_dotenv
from labedata import create_app
load_dotenv()

if __name__ == "__main__":
    # try:
    APP = create_app()
    APP.run(
        host=os.environ.get("IP", "0.0.0.0"),
        port=os.environ.get("PORT", 8080),
        debug=True)
    # except Exception as ex:
    #     logging.exception(ex)
    # finally:
    #     pass
