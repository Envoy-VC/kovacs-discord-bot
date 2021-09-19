from os import name
import random
from discord.ext import commands
from config import *



class Gamble(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="roll",description=f"""
    Gives a Random Number in 1-100
    Usage-```{PREFFIX}roll```
    """)
    async def roll(self, ctx):
        number = random.randrange(1,101)
        await ctx.send(number)

    @commands.command(name="dice",description=f"""
    Rolls a Dice
    Usage-```{PREFFIX}dice```
    """)
    async def dice(self, ctx):
        number = random.randrange(1,7)
        await ctx.send(number)

    @commands.command(name="coin",description=f"""
    Flips A Coin
    Usage-```{PREFFIX}coin```
    """)
    async def coin(self, ctx):
        number = random.randint(0,1)
        await ctx.send("Heads" if number == 1 else "Tails")

def setup(bot):
    bot.add_cog(Gamble(bot))