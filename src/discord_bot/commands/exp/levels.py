import logging
from discord.ext import commands
import discord
log = logging.getLogger(__name__)


class Levels(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.command()
    async def levels(self, ctx: commands.Context):
        """
        :return: embed with levels
        """
        embed = discord.Embed(color=discord.Color.gold())
        embed.set_image(url="https://cdn.arstechnica.net/wp-content/uploads/2022/03/38097_017.jpg")
        
        await ctx.send(embed=embed)
