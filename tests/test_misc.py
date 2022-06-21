from pathlib import Path
import discord
import pytest
import discord.ext.test as dpytest

@pytest.mark.asyncio
@pytest.mark.command("misc")
async def test_ping(bot):
    await dpytest.message("!ping")

    assert dpytest.verify().message().content("`pong`")
    assert dpytest.verify().message().content("`Pong! Latency is 0ms. API Latency is 0ms`")

@pytest.mark.asyncio
@pytest.mark.command("misc")
async def test_pfp(bot):
    embed = discord.Embed(color=discord.Color.gold())
    embed.set_image(url='https://cdn.discordapp.com/embed/avatars/1.png')
    
    await dpytest.message("!pfp")

    assert dpytest.verify().message().embed(embed)

@pytest.mark.asyncio
@pytest.mark.command("misc")
async def test_help(bot):
    await dpytest.message("!help")
    # TODO: update test to verify help command once help command is more in depth
    assert dpytest.verify().message().contains().content("```md\n**Categories**")

@pytest.mark.asyncio
@pytest.mark.command("misc")
@pytest.mark.skip(reason="recolor code is broken rn. gl ben")
async def test_recolor(bot):
    path_ = Path(__file__).resolve().parent / 'data/1x1.png'
    file_ = discord.File(path_)
    await dpytest.message("!recolor fff 50", file=file_)
    
