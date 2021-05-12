from abc import ABCmeta, abstractmethod
from ..labedata.db import get_db
import pandas as pd
import uuid 
from slugify import slugify
from csv_dataset import CSVDataset

TYPE_TO_CLASS = {"csv": CSVDataset}

class DatasetFactory(metaclass=ABCmeta):
    '''
    Factory class
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
    @staticmethod
    def new(self, dataset_id=None, data=None):
        assert (data is not None) or (dataset_id is not None), "Either data or dataset_id must be provided"
        if data is None:
            data = db.execute(
                f"SELECT *\
                FROM datasets WHERE dataset_id = ${dataset_id}"
            ).fetchone()
        return TYPE_TO_CLASS[data["dataset_format"]]

        for key, value in data.items():
            self[key] = value

    @staticmethod
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
    def create(data) -> Dataset:
        #! 1. validate request meta
        meta_fields = ["input_path", "dataset_format"]
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

        DATASET_CLASS = TYPE_TO_CLASS[dataset_format]
        # GENERATE ID 
        data["dataset_id"] = str(uuid.uuid4())
        # GENERATE dataset slug
        data["slug"] = slugify(title, max_length=20, word_boundary=True, separator="_")
        data["slug_id"] = slug + dataset_id.replace("-", "_")

        #! 3. process dataset input file and save to output_path
        output_path = DATASET_CLASS.perform_file_processing(data)
        
            
        #! 4. create new entity
        
        #! return Dataset instance
        

class Dataset(DatasetFactory, metaclass=ABCmeta):
    @abstractmethod
    @staticmethod
    def perform_file_processing(data) -> str:
        # shall output output_path
        raise NotImplemented

    @abstractmethod
    def get_entity(self, entity_id) ->  -> Dict[str, Any]:
    # returns dict with "data_field" and "label_field" keys
        raise NotImplemented

    @abstractmethod
    def label_entity(self, entity_id, label) -> None:
        raise NotImplemented

    @abstractmethod
    def modify_entity() -> None:
    # check modifications are allowed
        raise NotImplemented

    @abstractmethod
    def upsert_entity() -> str:
    # outputs new entity id
    # check upserts are allowd
        raise NotImplemented

    @abstractmethod
    def delete_entity() -> None:
    # check deletions are allowd
        raise NotImplemented

    @abstractmethod
    def next_entity_for_user_id(self, user_id)->  Union[str, None]:
        raise NotImplemented
