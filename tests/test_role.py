import pytest
from discord.ext.commands import Context
from discord_bot.commands.admin.role import Role

cog = Role()
ctx = Context()

cog.addroles.invoke(ctx)