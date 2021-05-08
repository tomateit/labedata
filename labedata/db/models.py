from abc import ABCmeta
from .labedata.db import get_db
import pandas as pd
import uuid 
from slugify import slugify
class User():

    
class Dataset():
    '''
    /-- meta
    dataset name
    uploaded date
    last updated
    /-- data labeling
    target_field
    target_field_type
    label_field
    label_field_type
    user_based_labeling
    /-- data cleaning
    allow_modify
    allow_upsert    
    '''
    def __init__(self, dataset_id=None, data=None):
        assert (data is not None) or (dataset_id is not None), "Either data or dataset_id must be provided"
        if data is None:
            data = db.execute(
                f"SELECT *\
                FROM datasets WHERE dataset_id = ${dataset_id}"
            ).fetchone()

        for key, value in data.items():
            self[key] = value


    def next_entity_for_user_id(self, user_id):
        db = get_db()
        if self.user_based_labeling:
            db.execute(
                f"SELECT X, label\
                FROM {self.tablename} WHERE assessed_by_{user_id} IS NULL\
                ORDER BY assessed_count ASC"
            ).fetchone()
        else:
            return db.execute(
                f"SELECT X, label\
                FROM {self.tablename} WHERE assessed IS NULL"
            ).fetchone()
    # @staticmethod
    # def fetch_by_id(dataset_id):
    #     return Datset(dataset_id)

    @staticmethod
    def fetch_by_author_id(author_id):
        db = get_db()
        return db.execute(
            f"SELECT title, created_at, username\
             FROM datasets dss JOIN user u ON dss.author_id = ${author_id}\
             ORDER BY dss.updated_at DESC"
        ).fetchall()

    @staticmethod
    def new(data):
        #! 1. validate request meta
        meta_fields = ["file_path", "file_format"]
        #! 2. validate dataset fields
        dataset_fields = ["title", 
            "author_id", 
            "data_field", 
            "data_field_type", 
            "label_field", 
            "label_field_type", 
            "user_based_labeling",
            "allow_modify_data",
            "allow_upsert_data",
            "allow_delete_data"]
        #! 3. process dataset input file
        if data["file_format"] == "csv":
            file_ = pd.read_csv(data["file_path"], usecols=[data["data_field"], data["label_field"]])
            # ensure data+label uniqueness (for further upsertion checks)
            file_.drop_duplicates(inplace=True)
        #! 4. create new entity
        # GENERATE ID 
        dataset_id = str(uuid.uuid4())
        # GENERATE TABLENAME
        tablename = slugify(title, max_length=20, word_boundary=True, separator="_") + dataset_id.replace("-", "_")
        #! return Dataset instance
        


