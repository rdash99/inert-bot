import logging

import discord
from discord.ext import commands
import urbandictionary as ud
import requests

log = logging.getLogger(__name__)


class XKCD(commands.Cog):
    def __init__(self, client):
        self.client = client

    @staticmethod
    async def get_comic_amount():
        return requests.get("https://xkcd.com/614/info.0.json").json()['num']

    @commands.command()
    async def xkcd(self, ctx, comic: int = None):
        """
        Gets a comic from xkcd
        """

        if comic is None:
            comic = await self.get_comic_amount()

        error = 0
        if comic > await self.get_comic_amount():
            comic = await self.get_comic_amount()
            error = 1
        if comic < 1:
            comic = 1
            error = 2

        xkcd_embed: discord.Embed = discord.Embed(title=F"Comic #{comic}")

        if error == 1:
            xkcd_embed.add_field(name="Warning:", value="Value too high, set to most recent comic", inline=True)
        if error == 2:
            xkcd_embed.add_field(name="Warning:", value="Value too low, set to first comic", inline=True)

        image_url = requests.get(f"https://xkcd.com/{comic}/info.0.json").json()['img']
        xkcd_embed.set_image(url=image_url)

        await ctx.reply(embed=xkcd_embed)
