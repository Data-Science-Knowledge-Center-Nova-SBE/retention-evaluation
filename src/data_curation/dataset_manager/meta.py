
import db

def create_meta():
    db.execute("""CREATE TABLE IF NOT EXISTS dataset_manager (id INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY, datetime TEXT, pipeline VARCHAR(256), n_rows INTEGER(32), n_columns INTEGER(32), columns TEXT, null_percentage TEXT, docs LONGTEXT,
    hash VARCHAR(256), table_name VARCHAR(128));""")


def get_meta():
    create_meta()
    return db.get_dataframe("dataset_manager")
