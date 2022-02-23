"""
This includes all the functions required for handling all database related functionality
"""
import logging
import os
# import sqlite3
import  mysql.connector
from mysql.connector import Error
# Discord settings
from discord_bot.settings import (SQL_HOST, SQL_USERNAME, SQL_PASSWORD, SQL_PORT, SQL_DATABASE)
log = logging.getLogger(__name__)

# Connecting to database
conn = None

try:
    conn = mysql.connector.connect(
        user=SQL_USERNAME,
        password=SQL_PASSWORD,
        host=SQL_HOST,
        port=SQL_PORT,
        database=SQL_DATABASE
    )

    log.info("Connection to MySQL DB successful")
except Error as e:
    log.error("Unable to connect to sql")
    log.exception(e)
    exit(1)

# Initalize cursor
c = conn.cursor()


def sqlLogging(func):
    """
    Logging for all sql functionality
    """
    def inner(sql, *params):
        # Checking whether params have been given for logging module
        log.debug(f"{sql} {params}")
        
        return func(sql, params)
    return inner


def init_db() -> None:
    """
    Sets up the database with correct tables using information from schema
    """
    log.debug("Initalising database")
    for filename in os.listdir(f"{os.path.dirname(__file__)}/migrations"):
        if filename.endswith(".sql"):
            log.debug("Updating %s", filename)
            with open(f"{os.path.dirname(__file__)}/migrations/{filename}", "r") as schema_file:
                schema = schema_file.read()
            
            for result in c.execute(schema, multi=True):
                comment = result.statement.split('\n',1)[0]
                log.debug(comment)
    
    conn.commit()
                            


@sqlLogging
def select(sql: str, params) -> list:
    """
    Selects information from a database
    """
    c.execute(sql, params)
    return c.fetchall()


@sqlLogging
def execute(sql: str, params) -> None:
    """
    Executes an sql statement and catches integraty errors
    """
    try:
        c.execute(sql, params)
        conn.commit()
    except Exception as e:
        conn.rollback()
        log.exception(e)

if __name__=="__main__":
    # testing db code
    init_db()