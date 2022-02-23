from discord.ext import commands
from time import time


class Ping(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def ping(self, ctx: commands.Context):
        """
        : works out latency of
        """
        t1 = time()
        msg = await ctx.send('`pong`')
        t2 = time()
        delay = t2 - t1
        await msg.edit(
            content=f'`Pong! Latency is {round(delay * 1000)}ms. API Latency is {round(self.client.latency * 1000)}ms`')
