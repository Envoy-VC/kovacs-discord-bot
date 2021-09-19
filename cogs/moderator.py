from discord.ext import commands
import discord

from utils import mods_or_owner
from config import *

class Moderator(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="kick",description=f"""
    Kick A User
    Usage-```{PREFFIX}kick @user```
    """)
    @mods_or_owner()
    @commands.guild_only()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member = None, reason: str = "Because you were bad. We kicked you."):
        if member is not None:
            await ctx.guild.kick(member, reason=reason)
        else:
            await ctx.send("Please specify user to kick via mention")

    @commands.command(name="ban",description=f"""
    Ban A User
    Usage-```{PREFFIX}ban @user```
    """)
    @mods_or_owner()
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member = None, reason: str = "Because you are naughty. We banned you."):
        if member is not None:
            await ctx.guild.ban(member, reason=reason)
        else:
            await ctx.send("Please specify user to ban via mention")

    @commands.command(name="unban",description=f"""
    Unban A User
    Usage-```{PREFFIX}unban (username)```
    """)
    @mods_or_owner()
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, member: str = "", reason: str = "You have been unbanned. Time is over. Please behave"):
        if member == "":
            await ctx.send("Please specify username as text")
            return

        bans = await ctx.guild.bans()
        for b in bans:
            if b.user.name == member:
                await ctx.guild.unban(b.user, reason=reason)
                await ctx.send("User was unbanned")
                return
        await ctx.send("User was not found in ban list.")


def setup(bot):
    bot.add_cog(Moderator(bot))