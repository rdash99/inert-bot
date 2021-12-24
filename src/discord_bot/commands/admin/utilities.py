import discord

def is_higher_permission(user: discord.Member, target: discord.Member) -> bool:
    """Checks whether the user is able to use this command on the member"""
    return user.top_role > target.top_role