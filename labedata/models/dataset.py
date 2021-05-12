from abc import ABCMeta, abstractmethod
from ..db import get_db
import pandas as pd
import uuid 
from slugify import slugify
from .csv_dataset import CSVDataset
from typing import List, Union
from .dataset_factory import DatasetFactory

class Dataset(DatasetFactory):
    def __init__(self, **data):
        self.dataset_id = data["dataset_id"]
        self.title  = data["title "]
        self.slug = data["slug"]
        self.slug_id = data["slug_id"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.author_id  = data["author_id "]
        self.data_field  = data["data_field "]
        self.data_field_type  = data["data_field_type "]
        self.label_field  = data["label_field "]
        self.label_field_type = data["label_field_type"]
        self.input_path  = data["input_path "]
        self.output_path = data["output_path"]
        self.dataset_format = data["dataset_format"]
        self.user_based_labeling = data["user_based_labeling"]
        self.allow_modify_data = data["allow_modify_data"]
        self.allow_upsert_data = data["allow_upsert_data"]
        self.allow_delete_data = data["allow_delete_data"]

    def user_id_to_colname(self, user_id) -> str:
        # TODO USE hashing to not expose internal ids
        return user_id + "_" + self.slug

    @abstractmethod
    @staticmethod
    def perform_file_processing(data) -> str:
        # shall output output_path
        raise NotImplemented

    @abstractmethod
    def get_entity(self, entity_id) -> Dict[str, Any]:
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
