import hashlib
import random
import string
from datetime import datetime
import pandas as pd
import db
from . import get_meta


def save(name, df, docs, train='N/A', fold='N/A', group='N/A', save_duplicate=True):
    """
    Saves a DataFrame and the documentation

    :param name:
    :param df:
    :param docs:
    :return:
    """

    # get meta
    meta = get_meta()

    # calc hash
    hash = hashlib.sha256(pd.util.hash_pandas_object(df, index=False).values).hexdigest()

    if save_duplicate:
        # check if hash already exists
        if hash in list(meta["hash"]):
            print("Dataset already saved")
            return None

    # calc id, table name, shape and date
    id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    table_name = "dataset_" + str(id)
    shape = df.shape

    # object to save
    data = {
        "pipeline": "'" + name + "'",
        "datetime": "'" + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "'",
        "n_rows": shape[0],
        "n_columns": shape[1],
        "columns": "'" + str(list(df.columns)).replace("'", "") + "'",
        "docs": "'" + docs.save().to_json() + "'",
        "hash": "'" + hash + "'",
        "table_name": "'" + table_name + "'",
        "train": "'" + train + "'",
        "fold": "'" + fold + "'",
        "group": "'" + group + "'",
    }

    # save
    save_row(data)

    # save table
    print(f"saving table {table_name}...")
    db.dataframe_to_table(df, table_name)


def save_row(data):
    query = """
    INSERT INTO dataset_manager (datetime, pipeline, n_rows, n_columns, columns, docs, hash, table_name, train, fold, cv_group)
    VALUES ({}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {})""".format(data["datetime"],
                                                      data["pipeline"],
                                                      data["n_rows"],
                                                      data["n_columns"],
                                                      data["columns"],
                                                      data["docs"],
                                                      data["hash"],
                                                      data["table_name"],
                                                      data["train"],
                                                      data["fold"],
                                                      data["group"])
    db.execute(query)
