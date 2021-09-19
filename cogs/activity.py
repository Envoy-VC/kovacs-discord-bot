from discord.ext import commands
import discord
import time


class Activity(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        activity = discord.Activity(type=discord.ActivityType.listening, name="!help")
        await self.bot.change_presence(status=discord.Status.idle, activity=activity)

        


def setup(bot):
    bot.add_cog(Activity(bot))