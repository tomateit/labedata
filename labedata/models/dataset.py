from abc import ABCmeta, abstractmethod
from ..labedata.db import get_db
import pandas as pd
import uuid 
from slugify import slugify

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

    @abstractmethod
    def label_entity(self, entity_id, label) -> None:
        raise NotImplemented

    @abstractmethod
    def modify_entity() -> None:
    # check modifications are allowed
        raise NotImplemented

    @abstractmethod
    def upsert_entity() -> None:
    # check upserts are allowd
        raise NotImplemented

    @abstractmethod
    def delete_entity() -> None:
    # check deletions are allowd
        raise NotImplemented

    @abstractmethod
    def next_entity_for_user_id(self, user_id)->  Union[str, None]:
        raise NotImplemented
    # @staticmethod
    # def fetch_by_id(dataset_id):
    #     return Datset(dataset_id)

    def user_id_to_colname(self, user_id) -> str:
        # TODO USE hashing to not expose internal ids
        return user_id + "_" + self.slug

    @staticmethod
    def fetch_by_author_id(author_id):
        db = get_db()
        return db.execute(
            f"SELECT title, created_at, username\
             FROM datasets dss JOIN user u ON dss.author_id = ${author_id}\
             ORDER BY dss.updated_at DESC"
        ).fetchall()

    @staticmethod
    def new(data) -> Dataset:
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
            # ensure it has index
            # save file to output directory
        #! 4. create new entity
        # GENERATE ID 
        dataset_id = str(uuid.uuid4())
        # GENERATE dataset slug
        slug = slugify(title, max_length=20, word_boundary=True, separator="_")
        web_id = slug + dataset_id.replace("-", "_")
        #! return Dataset instance
        


