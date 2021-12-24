import logging
import os
from discord import Intents
from discord.ext import commands
from sql.prefix import SqlClass

from settings import (TOKEN, DEBUG)

log = logging.getLogger(__name__)

# Creating client
sql = SqlClass()
def get_prefix(client, message):
    return sql.get_prefix(message.guild.id)[0][0]

# add discord bot perms
intents = Intents.default()
client = commands.Bot(command_prefix=get_prefix, intents=intents)

# Load extensions
log.debug("Loading default extensions...")
if DEBUG is True:
    log.info("=== DEBUG MODE ENABLED ===")

# loads all cogs
for folders in os.listdir('./commands'):
    try:
        logging.debug(f'loading {folders}...')
        client.load_extension(f'commands.{folders}')
    except Exception as e:
        log.error(type(e))
        log.error(e)


# prints when bot has started up
@client.event
async def on_ready():
    guilds = [guild.id for guild in client.guilds]

    db_guilds = [db_guilds[0] for db_guilds in sql.get_guilds()]

    # Every guild that isn't in the database
    lst = [g for g in guilds if g not in db_guilds]

    sql.add_guilds(lst, ".")

    # Every guild that the bot has been removed from
    lst = [db_g for db_g in db_guilds if db_g not in guilds]

    sql.remove_guilds(lst)
    log.info("bot ready")


@client.event
async def on_guild_join(guild):
    sql.add_guild(guild.id, ".")


@client.event
async def on_guild_remove(guild):
    sql.remove_guild(guild.id)


@client.before_invoke
async def before_invoke(ctx):
    # logging for when any command is ran
    log.info(f'{ctx.author} used {ctx.command} at {ctx.message.created_at}')


log.info('Starting bot')
client.run(TOKEN)
