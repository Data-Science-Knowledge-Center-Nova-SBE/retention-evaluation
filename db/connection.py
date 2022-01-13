import mysql.connector
from sqlalchemy import create_engine

# requires an environment.py with the variables on environment_example.py
import environment

CONNECTOR = None
def get_connector():
    global CONNECTOR
    if CONNECTOR is None:
        CONNECTOR = mysql.connector.connect(
            host=environment.HOST,
            user=environment.USER,
            passwd=environment.PASSWORD,
            database=environment.DATABASE
        )
    return CONNECTOR

def get_connection():
    return get_connector().cursor()


def execute(query):
    """
    Execute any SQL query to the database

    :param query: SQL query
    :return: result from the database
    """
    connection = get_connection()
    connection.execute(query)
    return connection


def get_engine():
    url = "mysql://{}:{}@{}/{}".format(environment.USER,
                                       environment.PASSWORD,
                                       environment.HOST,
                                       environment.DATABASE)
    engine = create_engine(url)
    return engine
