import db
from src.modeling.model_manager.create import create_meta


def get_meta():
    create_meta()
    return db.get_dataframe("model_manager")
