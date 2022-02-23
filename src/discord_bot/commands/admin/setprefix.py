from discord.ext import commands
# from sql.prefix import SqlClass
from discord_bot.sqlHandler import execute

class SetPrefix(commands.Cog):
    def __init__(self, client):
        self.client = client
        # self.sql = SqlClass()

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setprefix(self, ctx, prefix):
        """
        update prefix for the discord server
        """
        execute("INSERT INTO guilds (prefix) VALUES (%s) WHERE guild_id=%s", prefix, ctx.guild.id)
        await ctx.send(f"Updated prefix to: {prefix}")
