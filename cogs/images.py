from os import name
import random
import aiohttp
from discord.ext import commands
import discord

import praw

from config import *

class Images(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.reddit = None
        if REDDIT_APP_ID and REDDIT_APP_SECRET:
            self.reddit = praw.Reddit(client_id=REDDIT_APP_ID, client_secret=REDDIT_APP_SECRET,
                                      user_agent="KOVACS_DISCORD_BOT:%s:1.0" % REDDIT_APP_ID)



    @commands.command(name="random",description=f"""
    Gives a Random Image from Server Defined Subreddits
    Usage-```{PREFFIX}random (optional subreddit)```
    """)
    async def random(self, ctx, subreddit: str = ""):
        async with ctx.channel.typing():
            if self.reddit:
                # start working
                nsfw_flag = False
                chosen_subreddit = REDDIT_ENABLED_MEME_SUBREDDITS[random.randint(0,len(REDDIT_ENABLED_MEME_SUBREDDITS))]
                if subreddit:
                    # should take default one
                    if subreddit in REDDIT_ENABLED_MEME_SUBREDDITS:
                        chosen_subreddit = subreddit
                    elif subreddit in REDDIT_ENABLED_NSFW_SUBREDDITS:
                        chosen_subreddit = subreddit
                        nsfw_flag = True
                    elif subreddit == 'list':
                        return

                if nsfw_flag:
                    if not ctx.channel.is_nsfw():
                        await ctx.send("This is not allowed here")
                        return

                submissions = self.reddit.subreddit(chosen_subreddit).hot()

                post_to_pick = random.randint(1, 10)
                for i in range(0, post_to_pick):
                    submission = next(x for x in submissions if not x.stickied)
                await ctx.send(submission.url)

            else:
                await ctx.send("This is not working. Contact Administrator.")

    @commands.command(name='rlist',description=f"""
    Gives List of Server Defined Subreddits
    Usage-```{PREFFIX}rlist```
    """)
    async def subreddits_list(self,ctx):
        embed = discord.Embed(
            title = "List of allowed Subreddits",
            description = f"Welcome to random Help Dialog!\n\nCategory - `Images`",
            color =discord.Color.red()
        )
        embed.set_thumbnail(url='https://i.ibb.co/qFXTPN2/logo.png')
        for i in range(len(REDDIT_ENABLED_MEME_SUBREDDITS)-1):
            embed.add_field(name=f'{i+1}',value=f"```{REDDIT_ENABLED_MEME_SUBREDDITS[i]}```",inline=False)

        await ctx.send(embed=embed)

    @commands.command(name="cat",description=f"""
    Gives a Cute Meow
    Usage-```{PREFFIX}cat```
    """)
    async def cat(self, ctx):
        async with ctx.channel.typing():
            async with aiohttp.ClientSession() as cs:
                async with cs.get("http://aws.random.cat/meow") as r:
                    data = await r.json()

                    embed = discord.Embed(title="Meow")
                    embed.set_image(url=data['file'])
                    embed.set_footer(text="http://random.cat/")

                    await ctx.send(embed=embed)

    @commands.command(name="dog",description=f"""
    Random Cute dog pic
    Usage-```{PREFFIX}dog```
    """)
    async def dog(self, ctx):
        async with ctx.channel.typing():
            async with aiohttp.ClientSession() as cs:
                async with cs.get("https://random.dog/woof.json") as r:
                    data = await r.json()

                    embed = discord.Embed(title="Woof")
                    embed.set_image(url=data['url'])
                    embed.set_footer(text="http://random.dog/")

                    await ctx.send(embed=embed)

    @commands.command(name="fox",description=f"""
    Random Image of a fox
    Usage-```{PREFFIX}fox```
    """)
    async def fox(self, ctx):
        async with ctx.channel.typing():
            async with aiohttp.ClientSession() as cs:
                async with cs.get("https://randomfox.ca/floof/") as r:
                    data = await r.json()

                    embed = discord.Embed(title="Floof")
                    embed.set_image(url=data['image'])
                    embed.set_footer(text="https://randomfox.ca/")

                    await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Images(bot))