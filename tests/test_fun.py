from pathlib import Path
import discord
import pytest
import discord.ext.test as dpytest
import re


@pytest.mark.asyncio
@pytest.mark.command("fun")
async def test_bottom(bot):
    await dpytest.message("!bottomify")
    assert dpytest.verify().message().content("bottom")

    await dpytest.message("!bottomify bottom Hello world!")
    assert dpytest.verify().message().content("`💖✨✨,,👉👈💖💖,👉👈💖💖🥺,,,👉👈💖💖🥺,,,👉👈💖💖✨,👉👈✨✨✨,,👉👈💖💖✨🥺,,,,👉👈💖💖✨,👉👈💖💖✨,,,,👉👈💖💖🥺,,,👉👈💖💖👉👈✨✨✨,,,👉👈`")

    await dpytest.message("!bottomify decode `💖✨✨,,👉👈💖💖,👉👈💖💖🥺,,,👉👈💖💖🥺,,,👉👈💖💖✨,👉👈✨✨✨,,👉👈💖💖✨🥺,,,,👉👈💖💖✨,👉👈💖💖✨,,,,👉👈💖💖🥺,,,👉👈💖💖👉👈✨✨✨,,,👉👈`")
    assert dpytest.verify().message().content("Hello world!")

@pytest.mark.asyncio
@pytest.mark.command("fun")
async def test_hug(bot):
    await dpytest.message("!hug")
    assert dpytest.verify().message().content("*hugs back*")

    guild = bot.guilds[0]
    author = guild.members[0]
    await dpytest.message(f"!hug <@{author.id}>")
    assert dpytest.verify().message().content("https://imgur.com/xTJdcbg")

    await dpytest.message(f"!hug <@{bot.user.id}>")
    assert dpytest.verify().message().content("A hug from TestUser0_0_nick!")
    message = dpytest.get_message()
    assert re.match("https:\/\/imgur.com\/(\w|\d){7}", message.content) is not None

@pytest.mark.skip(reason="urbandict module fails")
@pytest.mark.asyncio
@pytest.mark.command("fun")
async def test_urban_dictionary(bot):
    await dpytest.message("!urbandictionary")
    assert dpytest.verify().message().content("You did not specifiy a word.")

    searchTerm = "urbandictionary"
    await dpytest.message(f"!urbandictionary {searchTerm}")
    emb = dpytest.get_embed()
    assert emb.title == f"Urban Dictionary {searchTerm.title()}"
    assert emb.description == "An urban description"


@pytest.mark.asyncio
@pytest.mark.command("fun")
async def test_uwu(bot):
    await dpytest.message("!uwu abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZtheTheTHEthTH\n ")
    message = dpytest.get_message()
    match = re.match("([A-KM-QS-Za-km-qs-z]){52}deTheDEdD (UwU|xwx|DwD|ÚwÚ|uwu|☆w☆|✧w✧|♥w♥|uw ︠u|\(uwu\)|OwO|owo|Owo|owO|\( ͡° ͜ʖ ͡°\))", message.content)
    assert match is not None

@pytest.mark.skip(reason="Broken implementation")
@pytest.mark.asyncio
@pytest.mark.command("fun")
async def test_xkcd(bot):
    await dpytest.message("!xkcd")
    emb = dpytest.get_embed()

    