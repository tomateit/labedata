from ._dataset import Dataset
from contextlib import contextmanager
import pandas as pd
from typing import Union, Dict, Any
import uuid
from flask import current_app
from pathlib import Path


class CSVDataset(Dataset):
    @staticmethod
    def perform_file_processing(data)->str:
        input_location = Path(current_app.config["INPUT_DIR"], data["input_path"])
        output_filename = f"{data['slug_id']}.csv"
        output_location = Path(current_app.config["OUTPUT_DIR"], output_filename)
        dataframe = pd.read_csv(input_location, usecols=[data["data_field"], data["label_field"]])
        dataframe.rename(columns = {data["data_field"]: "data_field", data["label_field"]: "label_field"}, inplace = True)
 
        dataframe.drop_duplicates(subset=["data_field"], inplace=True)
        dataframe = dataframe.assign(label_field=pd.NA)
        #!TODO ensure data_field and label_field fit *_field_type

        dataframe["entity_id"] = [str(uuid.uuid4()) for _ in range(len(dataframe))]
        dataframe.set_index("entity_id", inplace=True)
        #!TODO properly save file to output directory
        dataframe.to_csv(output_location)
        return output_filename

    @contextmanager
    def __get_dataset(self)-> pd.DataFrame:
        #TODO line-wise CSV reading
        try:
            # print(f"Opening dataset at {location}")
            dataset = pd.read_csv(self.get_location(), index_col="entity_id")
            yield dataset
        finally:
            #? wut
            # print(f"Saving dataset to {location}")
            dataset.to_csv(self.get_location())
            # update updated_at in dataset meta

    def get_location(self) -> Path:
        return Path(current_app.config["OUTPUT_DIR"], f"{self.slug_id}.csv")

    def next_entity_for_user_id(self, user_id):
        with self.__get_dataset() as dataset:
            if self.user_based_labeling:
                print("Requested next entity for dataset w/per-user labeling")
                column_name = self.user_id_to_colname(user_id)
                # 1. ensure dataset is ready for user-based labeling
                # i.e. it has column for the user_id
                if column_name not in dataset.cols:
                    dataset[column_name] = pd.NA
                try:
                    return dataset[dataset[column_name].isna()].head(1).index.item()
                except IndexError:
                    return None
            else:
                print("Requested next entity for commonly-labeled dataset")
                try:
                    index = dataset[dataset["label_field"].isna()].head(1).index.item()
                    return index
                except IndexError:
                    return None

    def get_entity(self, entity_id) -> Dict[str, Any]:
        with self.__get_dataset() as dataset:
            return {
                "data_field": dataset.loc[entity_id, "data_field"],
                "entity_id": entity_id
            }

    def label_entity(self, entity_id, label, user_id) -> None:
        with self.__get_dataset() as dataset:
            if self.user_based_labeling:
                column_name = self.user_id_to_colname(user_id)
                dataset.at[entity_id, column_name] = label
            else:
                dataset.at[entity_id, "label_field"] = label

    # def modify_entity(self, entity_id, new_data) -> None:
    #     assert self.allow_modify_data is True, "Modifications on this dataset are not allowed"
    #     with self.__get_dataset() as dataset:
    #         dataset.at[entity_id, "data_field"] = new_data


    # def upsert_entity(self, new_data, label) -> str:
    #     assert self.allow_upsert_data is True, "Upsertions on this dataset are not allowed"
    #     with self.__get_dataset() as dataset:
    #         try:
    #             # if such data exists - modify nothing
    #             indx = dataset.index[dataset["data_field"] == new_data].item()
    #             return indx
    #         except ValueError:
    #             new_indx = str(uuid.uuid4())
    #             dataset = dataset.append(pd.DataFrame({
    #                 "data_field": new_data, 
    #                 "label_field": label, "entity_id" : new_indx}, index_col="entity_id"))
    #             return new_indx
            


    # def delete_entity(self, entity_id) -> None:
    #     assert self.allow_delete_data is True, "Deletions on this dataset are not allowed"
    #     with self.__get_dataset() as dataset:
    #         dataset.drop(index=entity_id, inplace=True) # KeyError if no such index
