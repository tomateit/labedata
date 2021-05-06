import os
import dotenv
app_dir = os.path.abspath(os.path.dirname(__file__))

class BaseConfig:
    SECRET_KEY = os.environ.get("SECRET_KEY")
    DATABASE=os.path.join(app_dir, "data", "labedata.sqlite")

class DevelopementConfig(BaseConfig):
    DEBUG = True



class TestingConfig(BaseConfig):
    DEBUG = True



class ProductionConfig(BaseConfig):
    DEBUG = False
