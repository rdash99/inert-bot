import logging
import os
from discord import Intents
from discord.ext import commands

# from sql.prefix import SqlClass
from discord_bot.sqlHandler import (init_db, select, execute)
from discord_bot.settings import (DISCORD_TOKEN, DEBUG)

# TODO: Move this to the config.json file
DEFAULT_PREFIX = "."
log = logging.getLogger(__name__)

# Creating client
init_db()
# sql = SqlClass()


def get_prefix(client, message):
    return select("select prefix from guilds where guild_id = %s", message.guild.id)[0][0]
    # return sql.get_prefix(message.guild.id)[0][0]


# add discord bot perms
intents = Intents.default()
client = commands.Bot(command_prefix=get_prefix, intents=intents)

# Load extensions
log.debug("Loading default extensions...")
if DEBUG is True:
    log.info("=== DEBUG MODE ENABLED ===")

# loads all cogs
for folders in os.listdir(f"{os.path.dirname(__file__)}/commands"):
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

    # db_guilds = sql.get_guilds()
    db_guilds = select("SELECT guild_id FROM guilds")
    db_guilds = [db_guilds[0] for db_guilds in db_guilds]

    # lst = []
    for guild in guilds:
        if guild not in db_guilds:
            execute("insert into guilds (`guild_id`, `prefix`) values (%s,%s)", guild, DEFAULT_PREFIX)

    # sql.add_guilds(lst, ".")

    # lst = []
    for db_guild in db_guilds:
        if db_guild not in guilds:
            # lst.append(db_guild)
            execute("delete from guilds where guild_id=%s", db_guild)

    # sql.remove_guilds(lst)
    log.info("bot ready")


@client.event
async def on_guild_join(guild):
    # sql.add_guild(guild.id, ".")
    execute("insert into guilds (`guild_id`, `prefix`) values (%s,%s)", guild.id, DEFAULT_PREFIX)


@client.event
async def on_guild_remove(guild):
    # sql.remove_guild(guild.id)
    execute("delete from guilds where guild_id=%s", guild.id)


@client.before_invoke
async def before_invoke(ctx):
    # logging for when any command is ran
    log.info(f'{ctx.author} used {ctx.command} at {ctx.message.created_at}')


log.info('Starting bot')
client.run(DISCORD_TOKEN)
