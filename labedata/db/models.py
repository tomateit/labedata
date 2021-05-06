from abc import ABCmeta

class IUserStorage(metaclass=ABCmeta):

    
class IDataSetStorage(metaclass=ABCmeta):
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