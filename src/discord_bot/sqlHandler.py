"""
This includes all the functions required for handling all database related functionality
"""
import logging
import os
# import sqlite3
import  mysql.connector
from mysql.connector import Error
# Discord settings
from discord_bot.settings import (SQL_HOST, SQL_USERNAME, SQL_PASSWORD)
log = logging.getLogger(__name__)

# Connecting to database
connection = None

try:
    conn = mysql.connector.connect(
        host=SQL_HOST,
        user=SQL_USERNAME,
        passwd=SQL_PASSWORD
    )

    log.info("Connection to MySQL DB successful")
except Error as e:
    log.error("Unable to connect to sql")
    log.exception(e)
    exit(-1)

# Initalize cursor
c = conn.cursor()

def sqlLogging(func):
    """
    Logging for all sql functionality
    """
    def inner(sql, *params):
        log.debug(sql, params)
        func()


def init_db() -> None:
    """
    Sets up the database with correct tables using information from schema
    """
    for filename in os.listdir("./migrations"):
        if filename.endswith(".sql"):
            with open(f"./migrations/{filename}", "r") as schema_file:
                schema = schema_file.read()
            conn.executescript(schema)
            conn.commit()


@sqlLogging
def select(sql: str, *params) -> list:
    """
    Selects information from a database
    """
    c.execute(sql, params)
    return c.fetchall()


@sqlLogging
def execute(sql: str, *params) -> None:
    """
    Executes an sql statement and catches integraty errors
    """
    try:
        c.execute(sql, params)
        conn.commit()
    except Exception as e:
        conn.rollback()
        log.exception(e)
