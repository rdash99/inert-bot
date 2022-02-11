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
intents.members = True  # Needed to updated database when joining a server
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
    members = [member.id for member in client.users]
    update_users(members)

    guilds = {guild.id:guild for guild in client.guilds}

    db_guilds = select("SELECT guild_id FROM guilds")
    db_guilds = [db_guilds[0] for db_guilds in db_guilds]

    guildQuery = "insert into guilds (`guild_id`, `prefix`) values"
    userGuildQuery = "insert into user_guilds (`user_id`, `guild_id`) values"
    guild_data = []
    userGuild_ids = []
    # Every guild that isn't in the database
    for guild_id, guild in guilds.items() :
        if guild_id not in db_guilds:
            guildQuery += " (%s, %s),"
            guild_data.append(guild_id)
            guild_data.append(DEFAULT_PREFIX)
        
        # Check if all members are in the database
        db_members = select("SELECT user_id FROM user_guilds")
        db_members = [db_members[0] for db_members in db_members]
        async for member in guild.fetch_members(limit=None):
            if member.id not in db_members:
                userGuildQuery += " (%s,%s),"
                userGuild_ids.append(member.id)
                userGuild_ids.append(guild.id)

    # Check whether any data will be added to the server
    if len(guild_data) > 0:
        execute(guildQuery[:-1], *guild_data)
    
    if len(userGuild_ids) > 0:
        execute(userGuildQuery[:-1], *userGuild_ids)

    # Every guild that the bot has been removed from
    [execute("delete from guilds where guild_id=%s", db_g) for db_g in db_guilds if db_g not in guilds.keys()]

    log.info("bot ready")

def update_users(members):
    """
    Queries the sql server and updates all missing users
    """
    db_members = select("SELECT user_id from users")
    db_members = [db_members[0] for db_members in db_members]

    userQuery = "insert into users (`user_id`) values"
    user_ids = []
    for member in members:
        if member not in db_members:
            user_ids.append(member)
            userQuery += " (%s),"
    
    if len(user_ids) > 0:
        execute(userQuery[:-1], *user_ids)  # https://docs.python.org/3/tutorial/controlflow.html#tut-unpacking-arguments

@client.event
async def on_guild_join(guild):
    # sql.add_guild(guild.id, ".")
    execute("insert into guilds (`guild_id`, `prefix`) values (%s,%s)", guild.id, DEFAULT_PREFIX)
    # Added all members in the server to the server
    userGuildQuery = "insert into user_guilds (`user_id`, `guild_id`) values"
    userGuild_ids = []
    members = []
    async for member in guild.fetch_members(limit=None):
        # Add member to list to be checked by the update users function
        members.append(member.id)
        # Add all members to the user guild list
        userGuildQuery += " (%s, %s),"
        userGuild_ids.append(member.id)
        userGuild_ids.append(guild.id)
    
    update_users(members)
    execute(userGuildQuery[:-1], *userGuild_ids)

@client.event
async def on_guild_remove(guild):
    # sql.remove_guild(guild.id)
    execute("delete from guilds where guild_id=%s", guild.id)

@client.event
async def on_member_join(member):
    # sql.add_guild(guild.id, ".")
    execute("insert ignore into users (`user_id`) values (%s)", member.id)
    execute("insert into user_guilds (`user_id`, `guild_id`) values (%s, %s)", member.id, member.guild.id)


@client.before_invoke
async def before_invoke(ctx):
    # logging for when any command is ran
    log.info(f'{ctx.author} used {ctx.command} at {ctx.message.created_at}')


log.info('Starting bot')
client.run(DISCORD_TOKEN)
