from discord.ext import commands
from time import time
import math


class Ping(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def ping(self, ctx: commands.Context):
        """
        : Works out latency through sending a message
        """
        t1 = time()
        msg = await ctx.send('`pong`')
        t2 = time()
        delay = t2 - t1

        if math.isinf(self.client.latency):
            """
            dpytest bug causes code infinity rounding error
            """
            await msg.edit(
                content=f'`Pong! Latency is 0ms. API Latency is 0ms`')
        else:
            await msg.edit(
                content=f'`Pong! Latency is {round(delay * 1000)}ms. API Latency is {round(self.client.latency * 1000)}ms`')
