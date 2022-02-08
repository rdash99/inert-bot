from discord.ext import commands
import discord

from . import utilities

import logging
log = logging.getLogger(__name__)


class Ban(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None) -> None:
        """Bans a user from the server with an optional reason"""
        if utilities.is_higher_permission(ctx.author, member) is False:
            # Return some sort of error output
            message: discord.Message = await ctx.reply(
                f"You tried to ban {member.display_name} but they have a higher role than you")
            await message.delete(delay=3)
            return

        # Kicks the user
        await member.ban(reason=reason)

        # Outputting to logs
        # needs an sql refactor :deadeyes:

    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingPermissions):
            message: discord.Message = await ctx.message.reply("You do not have the permission to run this command")
            await message.delete(delay=3)
