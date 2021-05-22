import uuid 
from abc import ABCMeta, abstractmethod
import pandas as pd
from slugify import slugify
from typing import List, Union, Optional
from datetime import datetime
from ..db import get_db
from ._csv_dataset import CSVDataset
from ._dataset import Dataset

TYPE_TO_CLASS = {"csv": CSVDataset}

meta_fields = [
        "author_id", 
        "input_path", 
]
incoming_dataset_fields = ["title", 
        "data_field", 
        "data_field_type", 
        "label_field", 
        "label_field_type",
        "dataset_format" ,
        "user_based_labeling",
        "allow_modify_data",
        "allow_upsert_data",
        "allow_delete_data"]

class DatasetFactory():
    '''
    Factory class  
    '''
    @staticmethod
    def fetch_by_id(dataset_id)-> Union[Dataset, None]:
        # assert dataset_id is not None, "Must provide dataset_id" Nonsensical test
        #!TODO set id length validation
        #!TODO validate SQL injection
        db = get_db()
        dataset_meta_response = db.execute(
            f"SELECT *\
            FROM datasets WHERE dataset_id = ?",
            (dataset_id,)
        ).fetchone()
        if not dataset_meta_response:
            print(f"Dataset not found: {dataset_id}")
            return None
        DATASET_CLASS = TYPE_TO_CLASS[dataset_meta_response["dataset_format"]]
        dataset_meta = DATASET_CLASS(**dataset_meta_response)
        return dataset_meta

    @staticmethod
    def fetch_by_author_id(author_id) -> List:
        db = get_db()
        return db.execute(
            f"SELECT dataset_id, title, created_at, username\
             FROM datasets dss JOIN users u ON dss.author_id = ?\
             ORDER BY dss.updated_at DESC",
             (author_id,)
        ).fetchall()

    @staticmethod
    def create(**data) -> Dataset:
        #! 1. validate request meta
        # ewww
        global meta_fields
        meta_fields_precence = map(lambda key: key in data, meta_fields)
        if not all(meta_fields_precence): raise Exception(f"Missing field: {field: present for field, present in zip(meta_fields, meta_fields_precence)}")
        #! 2. validate dataset fields
        global incoming_dataset_fields
        # more ewww
        dataset_fields_precence = map(lambda key: key in data, incoming_dataset_fields)
        if not all(dataset_fields_precence): raise Exception(f"Missing field: {field: present for field, present in zip(incoming_dataset_fields, dataset_fields_precence)}")
        

        DATASET_CLASS = TYPE_TO_CLASS[data["dataset_format"]]
        # GENERATE ID 
        data["dataset_id"] = str(uuid.uuid4())
        # GENERATE dataset slug
        data["slug"] = slugify(data["title"], max_length=20, word_boundary=True, separator="_")
        data["slug_id"] = data["slug"] + "_" + data["dataset_id"].replace("-", "_")

        #! 3. process dataset input file and save to output_path
        data["output_path"] = DATASET_CLASS.perform_file_processing(data)
        data["created_at"] = datetime.now()
        data["updated_at"] = datetime.now()
        #! 4. create new entity
        DATASET = DATASET_CLASS(**data)
        DATASET.save()
        #! return Dataset instance
        print("Success")
        return DATASET

    