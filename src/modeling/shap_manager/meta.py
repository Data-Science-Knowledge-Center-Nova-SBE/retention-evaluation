import db


def create_meta():
    db.execute("""CREATE TABLE IF NOT EXISTS shap_manager (id INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY, datetime TEXT, n_rows INTEGER(32), n_columns INTEGER(32), columns TEXT,
    hash VARCHAR(256), table_name VARCHAR(128));""")


def get_meta():
    create_meta()
    return db.get_dataframe("shap_manager")
