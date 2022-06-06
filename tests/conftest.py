"""Minimal conftest"""
import glob
import os
import discord.ext.test as dpytest
import pytest
from discord.ext import commands
import discord

import discord_bot

import logging

log = logging.getLogger(__name__)

@pytest.fixture
def bot(event_loop):
    """Create the bot test environment to use with every test"""
    client = commands.Bot(
        command_prefix="!", event_loop=event_loop, intents=discord.Intents.all()
    )

    # Load extensions
    log.debug("Loading default extensions...")

    # loads all cogs
    for folders in os.listdir(f"{os.path.dirname(discord_bot.__file__)}/commands"):
        try:
            log.debug(f'loading {folders}...')
            client.load_extension(f'discord_bot.commands.{folders}')
        except Exception as e:
            log.error(type(e))
            log.error(e)

    dpytest.configure(client)
    return client


@commands.command()
async def ping(ctx):
    """Send message to a channel where !ping was called"""
    await ctx.send("pong")


def pytest_sessionfinish():
    """Clean up files"""
    files = glob.glob('./dpytest_*.dat')
    for path in files:
        try:
            os.remove(path)
        except Exception as e:
            print(f"Error while deleting file {path}: {e}")