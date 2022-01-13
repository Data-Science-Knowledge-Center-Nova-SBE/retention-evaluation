import hashlib
import random
import string
from datetime import datetime
import pandas as pd
import db
from src.modeling.shap_manager.meta import get_meta


def save(df, save_duplicate=True):
    """
    Saves a DataFrame and the documentation

    :param df:
    :param save_duplicate:
    :return:
    """

    # get meta
    meta = get_meta()

    # calc hash
    hash = hashlib.sha256(pd.util.hash_pandas_object(df, index=False).values).hexdigest()

    if save_duplicate:
        # check if hash already exists
        if hash in list(meta["hash"]):
            print("shap table already saved")
            return None

    # calc id, table name, shape and date
    id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    table_name = "shap_" + str(id)
    shape = df.shape

    # object to save
    data = {
        "datetime": "'" + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "'",
        "n_rows": shape[0],
        "n_columns": shape[1],
        "columns": "'" + str(list(df.columns)).replace("'", "") + "'",
        # "docs": "'" + docs.save().to_json() + "'",
        "hash": "'" + hash + "'",
        "table_name": "'" + table_name + "'"
    }

    # save
    save_row(data)

    # save table
    print(f"saving table {table_name}...")
    db.dataframe_to_table(df, table_name)


def save_row(data):
    query = """
    INSERT INTO shap_manager (datetime, n_rows, n_columns, columns, hash, table_name)
    VALUES ({}, {}, {}, {}, {}, {})""".format(data["datetime"],
                                              data["n_rows"],
                                              data["n_columns"],
                                              data["columns"],
                                              data["hash"],
                                              data["table_name"])
    db.execute(query)
