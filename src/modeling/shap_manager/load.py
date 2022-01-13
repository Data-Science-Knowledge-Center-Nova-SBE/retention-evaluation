import db
import environment
from src.modeling.shap_manager.meta import get_meta
import numpy as np


def load_dataset(table_name=environment.MAIN_TABLE, limit=None):

    print("Loading {} ".format(table_name))

    df = db.get_dataframe(table_name, limit=limit)
    df.replace("NULL",np.nan,inplace=True)

    return df


def load_dataset_by_id(id):
    table_name = get_table_name_by_id(id)

    if table_name == None:
        print("Id not found")
        return

    return load_dataset(table_name)


def get_table_name_by_id(id):
    meta = get_meta()
    table_name = meta[meta["id"] == id]["table_name"].iloc[0]

    return table_name
