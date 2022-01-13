from . import get_connector, get_engine
import pandas as pd


def get_dataframe(table_name, limit=None):

    # limit query
    limit_query=""
    if limit:
        limit_query="limit {}".format(limit)

    # create query
    query = "SELECT * FROM {} {}".format(table_name, limit_query)

    # get dataframe from sql query
    df = pd.read_sql(query, con=get_connector())

    return df

def dataframe_to_table(df, table_name):
    df.to_sql(table_name,
              con=get_engine(),
              index=False,
              if_exists='replace')
