"""conftest.py
builds and deletes pytest fixtures to allow
for the virtual bot to run. also imports the command being used
"""
import glob
import os
import pytest

import discord
from discord.ext import commands
from discord.ext import test

from pytest_mysql import factories
from getpass import getuser
from discord_bot.SqlHandler import SqlHandler

mysql_my_proc = factories.mysql_proc(
    port=None, user=getuser())
mysql_conn = factories.mysql('mysql_my_proc')

@pytest.fixture
def client(event_loop):
    """
    Creates a discord client for the bot to use.
    """
    c = discord.Client(loop=event_loop)
    test.configure(c)
    return c

@pytest.fixture
def bot(request, event_loop):
    """
    Builds a bot instance for testing.
    """
    intents = discord.Intents.default()
    # pylint: disable=assigning-non-slot
    intents.members = True
    b = commands.Bot("!", loop=event_loop, intents=intents)

    marks = request.function.pytestmark
    mark = None
    for mark in marks:
        if mark.name == "command":
            break

    if mark is not None:
        for extension in mark.args:
            b.load_extension(f".commands.{extension}", package="discord_bot")
            # b.load_extension(f"discord_bot.commands.{extension}")

    test.configure(b)
    return b


@pytest.fixture(autouse=True)
async def cleanup():
    """
    Cleanup after each test
    """
    yield
    await test.empty_queue()

@pytest.fixture
def mysql(mysql_conn):
    """
    Creates a mysql connection for the bot to use.
    """
    SqlHandler(mysql)
    return mysql_conn


def pytest_sessionfinish(session, exitstatus):
    """ Code to execute after all tests. """

    # dat files are created when using attachements
    print("\n-------------------------\nClean dpytest_*.dat files")
    file_list = glob.glob('./dpytest_*.dat')
    for file_path in file_list:
        try:
            os.remove(file_path)
        except Exception:
            print("Error while deleting file : ", file_path)
