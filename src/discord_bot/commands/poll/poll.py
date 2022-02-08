from discord.ext import commands
import discord


class Poll(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def poll(self, ctx, *, args: str = ' ') -> None:
        """
        Normal poll. Does {title} [option] [option] and "Foo Bar"
        :param ctx:
        :param args:
        :return:
        """
        if not self.reg.match(args):
            await ctx.message.add_reaction('👍')
            await ctx.message.add_reaction('👎')
            await ctx.message.add_reaction('🤷‍♀️')
            return

        listArgs = args.split('[')
        name = listArgs.pop(0)[1:]
        name = name[:name.find('}')]

        listArgs = [arg[:arg.find(']')] for arg in listArgs]  # thanks ritz for this line

        if len(listArgs) > 20:
            await ctx.send(f"bad {ctx.author.name}! thats too much polling >:(")
            return
        elif len(listArgs) == 0:
            await ctx.send(f"bad {ctx.author.name}! thats too little polling >:(")
            return
        elif name == '' or '' in listArgs:
            await ctx.send(f"bad {ctx.author.name}! thats too simplistic polling >:(")
            return

        description = ''
        for count in range(len(listArgs)):
            description += f'{self.pollsigns[count]} {listArgs[count]}\n\n'

        embed = discord.Embed(title=name, color=discord.Color.gold(), description=description)
        msg = await ctx.send(embed=embed)

        # add reactions
        for count in range(len(listArgs)):
            await msg.add_reaction(self.pollsigns[count])
