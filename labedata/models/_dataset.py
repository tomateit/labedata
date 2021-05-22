from abc import ABCMeta, abstractmethod
from ..db import get_db
import pandas as pd
import uuid 
from slugify import slugify
from typing import List, Union, Dict, Any
# from numbers import Number # for futhrt typings


class Dataset(metaclass=ABCMeta):
    fields = [
        "dataset_id",
        "title",
        "slug",
        "slug_id",
        "author_id",
        "created_at",
        "updated_at",
        "input_path",
        "output_path",
        "dataset_format",
        "data_field",
        "data_field_type",
        "label_field",
        "label_field_type",
        "user_based_labeling",
        "allow_modify_data",
        "allow_upsert_data",
        "allow_delete_data"]
    """
    Abstract blueprint of a stored dataset
    """
    def __init__(self, **data):
        self.dataset_id = data["dataset_id"]
        self.title  = data["title"]
        self.slug = data["slug"]
        self.slug_id = data["slug_id"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.author_id  = data["author_id"]
        self.data_field  = data["data_field"]
        self.data_field_type  = data["data_field_type"]
        self.label_field  = data["label_field"]
        self.label_field_type = data["label_field_type"]
        self.input_path  = data["input_path"]
        self.output_path = data["output_path"]
        self.dataset_format = data["dataset_format"]
        self.user_based_labeling = data["user_based_labeling"]
        self.allow_modify_data = data["allow_modify_data"]
        self.allow_upsert_data = data["allow_upsert_data"]
        self.allow_delete_data = data["allow_delete_data"]

    def user_id_to_colname(self, user_id) -> str:
        # TODO USE hashing to not expose internal ids
        return user_id + "_" + self.slug

    def save(self):
        db = get_db()
        placeholder = str((("?",)*len(Dataset.fields))).replace("'", "") # utilizing tuple (?, ?...) shape
        print(placeholder)
        db.execute(f"INSERT INTO datasets {str(tuple(Dataset.fields))} VALUES {placeholder};",
            [getattr(self, key) for key in Dataset.fields]
        )
        db.commit()

    # def __repr__(self):
    #     content = " \n ".join([
    #         f"{key}: {value}" for key, value in 
    #             zip(
    #                 Dataset.fields, 
    #                 [getattr(self, key) for key in Dataset.fields]
    #             )
    #     ])
    #     return f"DatasetMeta class { {content} }"

    def __repr__(self):
        content = " \n ".join([
            f"{key}: {value}" for key, value in self.__dict__.items()
        ])
        return f"DatasetMeta class { {content} }"

    def items(self):
        return self.__dict__.items()

    @staticmethod
    @abstractmethod
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
