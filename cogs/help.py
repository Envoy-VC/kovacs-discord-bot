from cogs.help_embed import HelpEmbed
from discord import components
from discord.ext import commands
import discord
import asyncio
from cogs.help_embed import HelpEmbed
from discord.ext.commands.help import HelpCommand

class Buttons(discord.ui.View):
    def __init__(self,pages):
        super().__init__()
        self.value = 0
        self.pages = pages

    @discord.ui.button(label="<<", style=discord.ButtonStyle.blurple)
    async def first(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.value = 0


    @discord.ui.button(label="<", style=discord.ButtonStyle.blurple)
    async def back(self, button: discord.ui.Button, interaction: discord.Interaction):
        if self.value != 0:
            self.value -= 1

    @discord.ui.button(label=">", style=discord.ButtonStyle.blurple)
    async def next(self, button: discord.ui.Button, interaction: discord.Interaction):
        if self.value != self.pages:
            self.value += 1

    @discord.ui.button(label=">>", style=discord.ButtonStyle.blurple)
    async def last(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.value = self.pages



class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx):
        cog_list = []
        restricted_cogs = ['Activity','Admin','Help','HelpEmbed','Test','Welcome']
        for cog in self.bot.cogs.keys():
            if cog not in restricted_cogs:
                cog_list.append(cog)

        print(cog_list)

        view = Buttons(len(cog_list)-1)

        msg = await ctx.send(embed=HelpEmbed(bot=self.bot).em(view.value),view=view)
        while True:
            await msg.edit(embed=HelpEmbed(bot=self.bot).em(view.value),view=view)


def setup(bot):
    bot.add_cog(Help(bot))