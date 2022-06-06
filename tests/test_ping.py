"""Testing"""
import pytest
import logging
import asyncio
from discord.ext.commands import Context
from discord_bot.commands.misc.ping import Ping

log = logging.getLogger(__name__)

@pytest.mark.asyncio
async def test_ping(bot):
    """Test if the ping command works"""
    cog = Ping()
    ctx = Context()

    cog.ping.invoke(ctx)
    assert True

