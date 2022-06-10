"""conftest.py
builds and deletes pytest fixtures to allow
for the virtual bot to run. also imports the command being used
"""
import glob
import os
import pytest
import discord
import discord.ext.commands as commands
import discord.ext.test as test


@pytest.fixture
def client(event_loop):
    c = discord.Client(loop=event_loop)
    test.configure(c)
    return c


@pytest.fixture
def bot(request, event_loop):
    intents = discord.Intents.default()
    intents.members = True
    b = commands.Bot("!", loop=event_loop, intents=intents)

    marks = request.function.pytestmark
    mark = None
    for mark in marks:
        if mark.name == "cogs":
            break

    if mark is not None:
        for extension in mark.args:
            b.load_extension("tests.internal." + extension)

    test.configure(b)
    return b


@pytest.fixture(autouse=True)
async def cleanup():
    yield
    await test.empty_queue()


def pytest_sessionfinish(session, exitstatus):
    """ Code to execute after all tests. """

    # dat files are created when using attachements
    print("\n-------------------------\nClean dpytest_*.dat files")
    fileList = glob.glob('./dpytest_*.dat')
    for filePath in fileList:
        try:
            os.remove(filePath)
        except Exception:
            print("Error while deleting file : ", filePath)


# @pytest.fixture
# def bot(event_loop):
#     """Create the bot test environment to use with every test"""
#     client = commands.Bot(
#         command_prefix="!", event_loop=event_loop, intents=discord.Intents.all()
#     )

#     # Load extensions
#     log.debug("Loading default extensions...")

#     # loads all cogs
#     for folders in os.listdir(f"{os.path.dirname(discord_bot.__file__)}/commands"):
#         try:
#             log.debug(f'loading {folders}...')
#             client.load_extension(f'discord_bot.commands.{folders}')
#         except Exception as e:
#             log.error(type(e))
#             log.error(e)

#     dpytest.configure(client)
#     return client
