import uuid 
from abc import ABCMeta, abstractmethod
import pandas as pd
from slugify import slugify
from typing import List, Union

from ..db import get_db
from ._csv_dataset import CSVDataset
from ._dataset import Dataset

TYPE_TO_CLASS = {"csv": CSVDataset}

class DatasetFactory():
    '''
    Factory class  
    '''
    @staticmethod
    def fetch_by_id(self, dataset_id)-> Union[Dataset, None]:
        assert dataset_id is not None, "Must provide dataset_id"
        db = get_db()
        dataset_meta = db.execute(
            f"SELECT *\
            FROM datasets WHERE dataset_id = ${dataset_id}"
        ).fetchone()
        CLASS = TYPE_TO_CLASS[data["dataset_format"]]
        return CLASS(**data)

    @staticmethod
    def fetch_by_author_id(author_id) -> List:
        db = get_db()
        return db.execute(
            f"SELECT title, created_at, username\
             FROM datasets dss JOIN users u ON dss.author_id = ?\
             ORDER BY dss.updated_at DESC",
             (author_id,)
        ).fetchall()

    @staticmethod
    def create(data) -> Dataset:
        #! 1. validate request meta
        meta_fields = [] # ??
        #! 2. validate dataset fields
        dataset_fields = ["title", 
            "author_id", 
            "data_field", 
            "data_field_type", 
            "label_field", 
            "label_field_type",
            "input_path", "dataset_format" ,
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
        data["output_path"] = DATASET_CLASS.perform_file_processing(data)
        
        #! 4. create new entity
        db = get_db()
        #! return Dataset instance
        return DATASET_CLASS(**data)

    