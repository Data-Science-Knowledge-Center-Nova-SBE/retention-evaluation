from datetime import datetime
import pickle

from src.data_curation import dataset_manager
import db
import pathlib
import os
import random
import string

from src.modeling import model_manager
from src.modeling.model_manager import files
from src.modeling.model_manager.meta import create_meta
from src.util.hash import calc_file_hash

PATH = pathlib.Path(__file__).parent.absolute()


def in_quotes(value):
    return "'" + value + "'"


def save_pickle(name, object):
    print("saving", name)
    localpath = os.path.join(PATH, "temp_files", name)
    pickle.dump(object, open(localpath, "wb"))
    random_letters = ''.join(random.choice(string.ascii_lowercase) for i in range(10))
    filename = name + "_" + random_letters + ".pkl"

    hashcode = calc_file_hash(localpath)
    files.upload_file(localpath, filename)

    return hashcode, filename


def report_exists(model_manager_meta, y_test_hash, y_pred_hash, model_hash):
    same_hash = model_manager_meta[(model_manager_meta["model_hash"] == model_hash) & (model_manager_meta["y_test_hash"] == y_test_hash) &(model_manager_meta["y_pred_hash"] == y_pred_hash)]
    return len(same_hash) > 0


def model_exists(model_manager_meta, model_hash):
    same_hash = model_manager_meta[model_manager_meta["model_hash"] == model_hash]
    if len(same_hash)>0:
        return True, same_hash[0]["model_filename"]

    return False, None

def save(report,model_group='N/A'):
    # get model manager table
    data_manager_meta = dataset_manager.get_meta()
    model_manager_meta = model_manager.get_meta()

    # get columns
    columns = data_manager_meta[data_manager_meta["id"] == report.database_id]["columns"].iloc[0]

    # get feature importance
    feature_importance = in_quotes(str(report.feature_importance).replace("'", ""))

    # save files
    extra_features_test_hash, extra_features_test_filename = save_pickle("extra_features", report.extra_features_test)
    y_test_hash, y_test_filename = save_pickle("y_test", report.y_test)
    y_pred_hash, y_pred_filename = save_pickle("y_pred", report.y_pred)
    model_hash, model_filename = save_pickle("model", report.model)

    # check if hashes and model exists
    if report_exists(model_manager_meta, y_test_hash, y_pred_hash, model_hash):
        print("Report already saved")
        return

    # check if model exists
    exists, filename = model_exists(model_manager_meta, model_hash)
    if exists:
        print("Reusing model previously saved")
        model_filename = filename

    # object to save
    data = {
        "datetime": in_quotes(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
        "model_name": in_quotes(report.algorithm),
        "description": in_quotes(report.algorithm),
        "dataset_id": report.database_id,
        "accuracy": report.accuracy,
        "precision_at_k_10": report.precision_at_k_10,
        "precision_at_k_15": report.precision_at_k_15,
        "precision_at_k_20": report.precision_at_k_20,
        "precision": report.precision,
        "recall": report.recall,
        "f1": report.f1,
        "feature_importance": feature_importance,
        "n_columns": len(columns.split(",")),
        "columns": in_quotes(columns),
        "extra_features_test_hash": in_quotes(extra_features_test_hash),
        "extra_features_test_filename": in_quotes(extra_features_test_filename),
        "y_test_hash": in_quotes(y_test_hash),
        "y_test_filename": in_quotes(y_test_filename),
        "y_pred_hash": in_quotes(y_pred_hash),
        "y_pred_filename": in_quotes(y_pred_filename),
        "model_hash": in_quotes(model_hash),
        "model_filename": in_quotes(model_filename),
        'model_group': model_group
    }

    # save
    add_row(data)

    return data


def add_row(data):
    create_meta()
    query = f"""
    INSERT INTO model_manager (datetime, model_name, description, dataset_id, n_columns, columns, accuracy, precision_at_k_10, precision_at_k_15, precision_at_k_20, precision_, recall, f1, feature_importance, extra_features_test_hash, extra_features_test_filename,y_test_hash, y_test_filename, y_pred_hash, y_pred_filename, model_hash, model_filename, model_group)
    VALUES ({data["datetime"]}, {data["model_name"]}, {data["description"]}, {data["dataset_id"]}, {data["n_columns"]}, {data["columns"]}, {data["accuracy"]}, {data["precision_at_k_10"]}, {data["precision_at_k_15"]}, {data["precision_at_k_20"]}, {data["precision"]}, {data["recall"]}, {data["f1"]}, {data["feature_importance"]}, {data["extra_features_test_hash"]}, {data["extra_features_test_filename"]}, {data["y_test_hash"]},{data["y_test_filename"]},{data["y_pred_hash"]}, {data["y_pred_filename"]}, {data["model_hash"]}, { data["model_filename"]}, {data["model_group"]})"""
    db.execute(query)
