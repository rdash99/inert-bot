import logging

import discord
from discord.ext import commands
import urbandictionary as ud

log = logging.getLogger(__name__)


class UrbanDictionary(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["ud"])
    async def urbandictionary(self, ctx, word: str = None):
        """
        Looks up a definition in urban dictionary
        """
        if word is None:
            await ctx.reply("You did not specifiy a word.")
            return

        definition = ud.define(word)[0]

        urban_embed = discord.Embed(title=f"Urban Dictionary: {word.title()}",
                                    description="An urban description")

        urban_embed.add_field(name="Description", value=definition.definition, inline=False)

        if definition.example is not None:
            urban_embed.add_field(name="Example", value=definition.example, inline=False)

        await ctx.reply(embed=urban_embed)
