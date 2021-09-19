from discord.ext import commands
import discord
from utils import notify_user
from config import *

class Basic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ping",description=f"""
    Returns The Latency Of the Bot
    Usage-```{PREFFIX}ping```
    """)
    async def ping(self, ctx):
        await ctx.send(f"Pong! I replied in {round(self.bot.latency * 1000)}ms")

    @commands.command(description=f"""
    Get The Server's Invite Link
    Usage-```{PREFFIX}invite```
    """)
    async def invite(self, ctx):
        link = await ctx.channel.create_invite(max_age=86400)
        await ctx.send(link)
        
    @commands.command(description=f"""
    Pokes a User in DM
    Usage-```{PREFFIX}poke @user```
    """)
    async def poke(self, ctx, member: discord.Member = None):

        if member is not None:
            message = f"<@{ctx.author.id}> poked you!!!!"
            await notify_user(member, message)
        else:
            await ctx.send("Please use @mention to poke someone.")

def setup(bot):
    bot.add_cog(Basic(bot))