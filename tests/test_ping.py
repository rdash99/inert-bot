import discord
import pytest
import discord.ext.test as dpytest

@pytest.mark.asyncio
@pytest.mark.command("misc")
async def test_edit_cog(bot):
    guild = bot.guilds[0]
    member = guild.members[0]
    dm = await member.create_dm()
    await dpytest.message("!ping", dm)

    assert dpytest.verify().message().content("`pong`")
    assert dpytest.verify().message().content("`Pong! Latency is 0ms. API Latency is 0ms`")
