from main import Kovacs
from discord import embeds
from discord.ext import commands
import discord
from discord.ext.commands import bot
from config import *


class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self,member: discord.Member):
        channel = self.bot.get_channel(WELCOME_CHANNEL)
        em = discord.Embed(
            title=TITLE,
            description=DESCRIPTION,
            colour=discord.Color.from_rgb(RED,GREEN,BLUE)
        )
        server = self.bot.get_guild(SERVER_ID)
        member_count = server.member_count
        em.add_field(name="Welcome",value=f"""
        Hi <@{member.id}>, Welcome to Kovacs Discord Support Server.You just made our 
        community {member_count} member strong.
        """,inline=False)
        em.add_field(name="For Suggestions ",value="<#885559521592868922>",inline=False)
        em.add_field(name="For Bot Testing",value="<#889027496442478602>",inline=False)
        em.add_field(name="To Report Errors",value="<#885559522310127654>",inline=False)
        em.set_thumbnail(url=member.avatar)
        em.set_image(url=IMAGE_URL)
        em.set_author(name=member.name)
        em.set_footer(text=FOOTER_TEXT)
        await channel.send(embed=em)

        for i in JOIN_ROLES:
            await member.add_roles(member.guild.get_role(i))

        
def setup(bot):
    bot.add_cog(Welcome(bot))