from . import execute


def get_tables():
    return [x[0] for x in execute("SHOW TABLES")]



def delete_table(table_name):
    print(f"deleting table {table_name}")
    query = "DROP TABLE {};".format(table_name)
    execute(query)

def delete_by_ids(table_name, ids):
    query = "DELETE FROM {} WHERE ID IN {};".format(table_name, str(tuple(ids)))
    execute(query)


def get_last_id(table_name):
    query = """
    SELECT
    LAST_INSERT_ID()
    FROM
    {}
    """.format(table_name)

    return execute(query)
