from discord import embeds, user
from discord.colour import Color, Colour
from discord.embeds import E
from discord.ext import commands
from discord.ext.commands import bot
from discord.ext.commands.core import command
from economy import functions
import discord
from discord.ext.commands import cooldown, BucketType
from config import *

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    

    @commands.group(name="piper",description="""
    PiedPiper Coin :coin:
    """)
    async def piper(self,ctx):
        pass

    @piper.command(name="create",description=f"""
    Create A PiedPiper Account
    Usage-```{PREFFIX}piper create```
    """)
    async def create_account(self,ctx):
        user_id = str(ctx.author.id)
        is_account_exists = functions.check_account(user_id)
        print(is_account_exists)

        if is_account_exists:
            await ctx.send(f"<@{user_id}> you already have a account")
        else:
            functions.create_account(user_id)
            await ctx.send(f'Account Successfully Created for <@{user_id}>')

    @piper.command(name="top",description=f"""
    Returns The LeaderBoard
    Usage-```{PREFFIX}piper top```
    """)
    async def leaderboard(self,ctx):
        embed = functions.leaderboard()
        if type(embed) == type('hello'):
            await ctx.send(embed)
        else:
            await ctx.send(embed=embed)

    @piper.command(name='bal',description=f"""
    Gives Current Balance of the User
    Usage-```{PREFFIX}piper bal```
    """)
    async def balance(self,ctx):
        user_id = ctx.author.id
        embed = functions.balance(str(user_id))
        await ctx.send(embed=embed)


    @piper.command(name='beg',description=f"""
    Beg For PiperCoin :coin
    Usage-```{PREFFIX}piper beg```
    """)
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def beg(self,ctx):
        amount_collected = functions.beg_coin(str(ctx.author.id))
        if amount_collected != 0:
            msg = f"Hey <@{ctx.author.id}> you managed to collect {amount_collected} :coin:"
            embed = discord.Embed(
            title="Result",
            description=f"{msg}",
            color=discord.Colour.green()
            )
            await ctx.send(embed=embed)
        else:
            msg = f"Hey <@{ctx.author.id}>,no one is giving u :coin: sed life"
            embed = discord.Embed(
            title="Result",
            description=f"{msg}",
            color=discord.Colour.yellow()
            )
            await ctx.send(embed=embed)

    @beg.error
    async def beg_error(self,ctx :commands.Context,error):
        if isinstance(error,commands.CommandOnCooldown):
            em = discord.Embed(title="Error",description=f"This command is on cooldown,try again after {round(error.retry_after)} seconds.",
            color=discord.Colour.dark_orange())
            await ctx.send(embed=em,delete_after = 5)

    @piper.command(name="invest",description=f"""
    Invest In PiedPiper Stocks
    Usage-```{PREFFIX}piper invest (amount)```
    """)
    @commands.cooldown(1,40,commands.BucketType.user)
    async def invest_piper(self,ctx,amount :int):
        user_id = str(ctx.author.id)
        msg = functions.invest(user_id,amount)
        await ctx.send(embed=msg)

    @invest_piper.error
    async def invest_piper_error(self,ctx :commands.Context,error):
        if isinstance(error,commands.CommandOnCooldown):
            em = discord.Embed(title="Error",description=f"This command is on cooldown,try again after {round(error.retry_after)} seconds.",
            color=discord.Colour.dark_orange())
            await ctx.send(embed=em,delete_after = 5)

    @piper.command(name='buy',description=f"""
    Buy A GPU
    Usage-```{PREFFIX}piper buy (gpu_name)```
    """)
    async def buy(self,ctx,gpu):
        gpu = str(gpu)
        user_id = str(ctx.author.id)
        total = functions.max_gpu(user_id)
        gpu_exists = functions.exists_in_owned_gpu(user_id,gpu)
        if total < 5:
            if not gpu_exists:
                details = functions.get_gpu_details(user_id,gpu)
                if type(details) == type([0,1]):
                    funds = functions.check_bal(user_id,details[1])
                    if type(funds) == type(True):
                        status = functions.buy(user_id,details[1],gpu)
                        if status:
                            em = discord.Embed(
                                title=f"Success",
                                description=f"You Successfully Bought {details[0]} for {details[1]} :coin:",
                                color=discord.Colour.brand_green()
                            )
                            await ctx.send(embed=em)

                    else:
                        await ctx.send(embed=funds)
                else:
                    await ctx.send(embed=details)
                
            else:
                em = discord.Embed(
                title="Already Owned",
                description="You already Own this GPU",
                color=discord.Colour.brand_red()
                )
                await ctx.send(embed=em)

        else:
            em = discord.Embed(
                title="Max Limit Reached",
                description="You can only own `5` GPUs",
                color=discord.Colour.brand_red()
            )
            await ctx.send(embed=em)

    @piper.command(name='glist',description=f"""
    Get List Of All GPUs
    Usage-```{PREFFIX}piper glist```
    """)
    async def gpu_list(self,ctx):
        em = functions.gpu_embed()
        await ctx.send(embed = em)

    @piper.command(name='sell',description=f"""
    Sell an Owned GPU
    Usage-```{PREFFIX}piper sell (gpu_name)```
    """)
    async def sell_gpu(self,ctx,name):
        user_id = str(ctx.author.id)
        user_owns_gpu = functions.owns_gpu(user_id,name)
        if user_owns_gpu:
            details = functions.get_gpu_details(user_id,name)
            done = functions.sell(user_id,details,name)
            if done:
                em = discord.Embed(
                    title="Success",
                    description=f"<@{user_id}>,Successfully sold your `{details[0]}` for {round(details[1]*0.9)} :coin:",
                    color=discord.Colour.brand_green()
                )
                await ctx.send(embed=em)

        else:
            em = discord.Embed(
                title="Status",
                description=f"<@{user_id}>You do not own this GPU",
                color=discord.Colour.brand_red()

            )
            await ctx.send(embed = em)

    @piper.command(name='owned',description=f"""
    Gives a List of your Owned GPUs
    Usage-```{PREFFIX}piper owned```
    """)
    async def owned_gpus(self,ctx):
        user_id = str(ctx.author.id)
        owned_gpu = functions.owned(user_id)
        em = discord.Embed(
            title="Owned GPUs",
            description=f"<@{user_id}>'s Owned GPUs List",
            color=discord.Colour.dark_gold()
        )
        for i in range(len(owned_gpu)):
            details = functions.get_gpu_details(user_id,owned_gpu[i])
            em.add_field(name="\u200b",value=f"```{details[0]}```",inline=False)
        
        await ctx.send(embed=em)


    @piper.command(name='mine',description=f"""
    Starts to mine PiperCoin :coin:
    Usage-```{PREFFIX}piper mine```
    """)
    @commands.cooldown(1,60,commands.BucketType.user)
    async def mine_pipercoin(self,ctx):
        user_id = str(ctx.author.id)
        num = len(functions.owned(user_id))
        total_eff = functions.total_efficiency(user_id)
        list = [total_eff-(num*5),total_eff]
        coin_gained = functions.mine(user_id,list)
        em = discord.Embed(
            title="Mining Result",
            description=f"<@{user_id}>,You managed to Mine `{coin_gained}` :coin:",
            color=discord.Colour.dark_teal()
        )
        await ctx.send(embed=em)

    @mine_pipercoin.error
    async def mine_pipercoin_error(self,ctx :commands.Context,error):
        if isinstance(error,commands.CommandOnCooldown):
            em = discord.Embed(title="Error",description=f"Your rig is cooling,try again after {round(error.retry_after)} seconds.",
            color=discord.Colour.dark_orange())
            await ctx.send(embed=em,delete_after = 5)

    @piper.command(name='daily',description=f"""
    Claim Daily Bonus of {DAILY_BONUS} :coin:
    Usage-```{PREFFIX}piper daily```
    """)
    @commands.cooldown(1, 86400, commands.BucketType.user)
    async def daly_bonus(self,ctx):
        user_id = str(ctx.author.id)
        value = functions.daily(user_id)
        if value:
            em = discord.Embed(
            title="Daily Bonus",
            description=f"<@{user_id}>,You Succesfully Claimed Daily Bonus - `250` :coin:",
            color=discord.Colour.blue()
            )
            await ctx.send(embed=em)

    @daly_bonus.error
    async def daly_bonus_error(self,ctx :commands.Context,error):
        if isinstance(error,commands.CommandOnCooldown):
            em = discord.Embed(title="Error",description=f"You have already claimed Daily Bonus,Claim again after {round(error.retry_after/3600)} Hours.",
            color=discord.Colour.dark_orange())
            await ctx.send(embed=em,delete_after = 5)

    @piper.command(name='help',description = F"""
    Commands For PiperCoin :coin:
    Usage-```{PREFFIX}piper help```
    """)
    async def piper_help(self,ctx):
        em = discord.Embed(
            title="PiedPiper Coin",
            description="Commands for PiperCoin",
            color=discord.Colour.dark_teal()
            )
        em.add_field(name=f"create | creates a PiedPiper Wallet Account",value=f"Usage:```{PREFFIX}piper create```",inline=False)
        em.add_field(name=f"top | Displays LeaderBoard",value=f"Usage:```{PREFFIX}piper top```",inline=False)
        em.add_field(name=f"bal | Shows Your Current Balance",value=f"Usage:```{PREFFIX}piper bal```",inline=False)
        em.add_field(name=f"beg | beg for coins(does not work everytime)",value=f"Usage:```{PREFFIX}piper beg```",inline=False)
        em.add_field(name=f"invest | Invest in PiedPiper Stocks",value="Usage:```{PREFFIX}piper invest {amount}```",inline=False)
        em.add_field(name=f"glist | Shows available GPUs for Mining",value=f"Usage:```{PREFFIX}piper glist```",inline=False)
        em.add_field(name=f"buy | Buy a GPU for Mining",value="Usage:```{PREFFIX}piper buy {gpu name}```",inline=False)
        em.add_field(name=f"sell | Sell a GPU",value="Usage:```{PREFFIX}piper sell {gpu name}```",inline=False)
        em.add_field(name=f"owned | Gives a list of your owned GPUs",value="Usage:```{PREFFIX}piper owned```",inline=False)
        em.add_field(name=f"mine | Mines PiperCoin",value=f"Usage:```{PREFFIX}piper mine```",inline=False)
        em.add_field(name=f"daily | Get daily bonus of {DAILY_BONUS} PiperCoins",value=f"Usage:```{PREFFIX}piper daily```",inline=False)

        await ctx.send(embed=em)



def setup(bot):
    bot.add_cog(Economy(bot))