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
    APP.run(debug=True)
    # except Exception as ex:
    #     logging.exception(ex)
    # finally:
    #     pass
