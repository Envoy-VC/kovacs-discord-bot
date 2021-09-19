import discord
import discord
from discord.ext import commands

class HelpEmbed(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def em(self,page_number):
        cog_list = []
        restricted_cogs = ['Activity','Admin','Help','HelpEmbed','Test','Welcome']
        for cog in self.bot.cogs.keys():
            if cog not in restricted_cogs:
                cog_list.append(cog)
        
        embed = discord.Embed(
                title=f"Kovacs Help Module",
                description=f"Category - `{cog_list[page_number]}`",
                color=discord.Colour.blurple()
            )
        for command in self.bot.get_cog(cog_list[page_number]).walk_commands():
            if "error" in command.name:
                continue
            embed.add_field(name=f"**{command.name}**",value=f"{command.description}",inline=False)

        return embed

def setup(bot):
    bot.add_cog(HelpEmbed(bot))