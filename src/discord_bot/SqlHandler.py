"""sqlHandler.py: Handles the SQL database."""
import logging
import os
# import sqlite3
import  mysql
# Connections
from mysql.connector.connection import MySQLConnection
from mysql.connector.cursor import MySQLCursor
# Errors
from mysql.connector.errors import InterfaceError
from mysql.connector.errors import ProgrammingError
from mysql.connector.errors import IntegrityError
from mysql.connector.errors import OperationalError

# Discord settings
from discord_bot.settings import (SQL_HOST, SQL_USERNAME, SQL_PASSWORD, SQL_PORT, SQL_DATABASE)
log = logging.getLogger(__name__)


def sql_logging(func):
    """
    Logging for all sql functionality
    """
    def inner(sql, *params):
        # Checking whether params have been given for logging module
        log.debug("%s %s", sql, params)

        return func(sql, params)
    return inner


@sql_logging
def select(sql: str, params = tuple()) -> list:
    """
    Selects information from a database
    """
    # pylint: disable=invalid-name
    with SqlHandler() as db:
        db.c.execute(sql, params)
        data = db.c.fetchall()
    return data


@sql_logging
def execute(sql: str, params = tuple()) -> None:
    """
    Executes an sql statement and catches integraty errors
    """
    # pylint: disable=invalid-name
    with SqlHandler() as db:
        try:
            db.c.execute(sql, params)
            db.conn.commit()
        except IntegrityError as database_error:
            db.conn.rollback()
            log.error("%s %s", database_error, sql)

class SqlHandler:
    """
    Sql Context Handler
    """
    conn: MySQLConnection = None

    def __init__(self, connection: MySQLConnection = None):
        # Connecting to database using static variable containing connection
        if connection is not None:
            SqlHandler.conn = connection

        if SqlHandler.conn is None:
            # Try and connect to Sql database
            log.info("Connecting to Sql database")
            try:
                SqlHandler.conn = mysql.connector.connect(
                    user=SQL_USERNAME,
                    password=SQL_PASSWORD,
                    host=SQL_HOST,
                    port=SQL_PORT,
                    database=SQL_DATABASE
                )
                log.info("Connection to MySQL DB successful")
                self.migrate()
            except InterfaceError as couldnt_connect:
                log.error("Couldn't connect to MySQL DB")
                log.exception(couldnt_connect)
                raise couldnt_connect
        else:        
            SqlHandler.conn.ping(reconnect=True)

    def __del__(self):
        pass

    def __enter__(self):
        # self.conn = SqlHandler.conn
        # pylint: disable=attribute-defined-outside-init, invalid-name
        self.c: MySQLCursor = self.conn.cursor()
        return self 

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.c.reset()
        self.c.close()

    def __str__(self) -> str:
        string = f"SqlHandler <{hex(self.__hash__())}>:\n"
        string += f"\tConnection: {SqlHandler.conn.__str__()}"
        return string


    def migrate(self, conn: MySQLConnection = None):
        """
        Migrates the database to the latest version
        """
        path_to_migrations  = f"{os.path.dirname(__file__)}/migrations/"
        version: int
        schema_version: int = len(os.listdir(path_to_migrations)) - 1
        conn: MySQLConnection = SqlHandler.conn if conn is None else conn

        # get current migration version
        c: MySQLCursor = conn.cursor()
        try:
            c.execute("SELECT version FROM meta")
            version = c.fetchone()[0]
            conn.commit()
        except ProgrammingError:
            conn.rollback()
            version = -1

        if version < schema_version:
            log.info("Migrating database")

            # get all migrations
            while version < schema_version:
                version += 1
                log.info("Migrating to version %d", version)

                with open(f"{path_to_migrations}v{version}.sql", "r", encoding="utf-8") as f:
                    sql = f.read()

                result = c.execute(sql, multi=True)
                # consume iter
                for _ in result:
                    pass

                conn.commit()

            # update meta table
            c.execute("UPDATE meta SET version = %s", (version,))
            conn.commit()
            log.info("Migration complete")

if __name__=="__main__":
    data = select("SELECT * FROM meta")
    print(data)