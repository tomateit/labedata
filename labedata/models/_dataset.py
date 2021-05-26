from abc import ABCMeta, abstractmethod
import logging
import os
from pathlib import Path
from ..db import get_db
import pandas as pd
import uuid 
from slugify import slugify
from typing import List, Union, Dict, Any, Optional
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
        # "allow_modify_data",
        # "allow_upsert_data",
        # "allow_delete_data"
        ]
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
        # self.allow_modify_data = data["allow_modify_data"]
        # self.allow_upsert_data = data["allow_upsert_data"]
        # self.allow_delete_data = data["allow_delete_data"]

    def user_id_to_colname(self, user_id) -> str:
        # TODO USE hashing to not expose internal ids
        return user_id + "_" + self.slug

    def validate_form(form: Dict) -> Optional[str]:
        #TODO refactor to isolate form validation logic
        raise NotImplementedError

    def save(self):
        db = get_db()
        placeholder = str((("?",)*len(Dataset.fields))).replace("'", "") # utilizing tuple (?, ?...) shape
        query = f"INSERT INTO datasets {str(tuple(self.__dict__.keys()))}\
             VALUES {placeholder};"
        print(query)
        db.execute(query, tuple(self.__dict__.values()))
        db.commit()
        logging.info(f"Dataset meta '{self.dataset_id}' has been created")

    def delete(self):
        # Delete meta
        db = get_db()
        db.execute(f"DELETE FROM datasets WHERE dataset_id = ?;",
            (self.dataset_id, )
        )
        db.commit()
        logging.warning(f"Dataset meta '{self.dataset_id}' has been removed")
        # Delete input files
        input_location = Path(current_app.config["INPUT_DIR"], self.input_path)
        os.remove(input_location)
        logging.warning(f"Dataset input file '{input_location}' has been removed")
        # Delete output files
        output_location = self.get_location()
        os.remove(output_location)
        logging.warning(f"Dataset output file '{output_location}' has been removed")

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
        """
        Processes incoming file and saves into output direction.
        Returns:
            output_filename: constructed filename
        """
        raise NotImplemented

    @abstractmethod
    def get_location(self) -> Path:
        """Returns full file location depending on dataset format"""
        raise NotImplemented

    @abstractmethod
    def get_entity(self, entity_id) -> Dict[str, Any]:
        """
        Returns dict with fields:
            data_field
            label_field
            entity_id
        """
        raise NotImplemented

    @abstractmethod
    def label_entity(self, entity_id, label) -> None:
        """Modifies entity in dataset, sets its label to provided one"""
        raise NotImplemented

    # @abstractmethod
    # def modify_entity() -> None:
    # # check modifications are allowed
    #     raise NotImplemented

    # @abstractmethod
    # def upsert_entity() -> str:
    # # outputs new entity id
    # # check upserts are allowd
    #     raise NotImplemented

    # @abstractmethod
    # def delete_entity() -> None:
    # # check deletions are allowd
    #     raise NotImplemented

    @abstractmethod
    def next_entity_for_user_id(self, user_id)->  Union[str, None]:
        """Returns nonlabeled entity or None"""
        raise NotImplemented
