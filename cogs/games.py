from discord.ext import commands
import discord
import random

from rps.model import RPS
from rps.parser import RockPaperScissorParser
from rps.controller import RPSGame


from hangman.controller import HangmanGame

from gaw.controller import GuessAWordGame

from config import *

class Games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="rps",description=f"""
    Play Rock Paper Scissor with the Bot
    Usage-```{PREFFIX}rps (rock|paper|scissor)```
    """)
    async def rps(self, ctx, user_choice: RockPaperScissorParser = RockPaperScissorParser(RPS.ROCK)):
        """
        Play a game of Rock Paper Scissors

        Either choose rock, paper or scissor and beat the bot

        You cannot challenge another user. Its you vs the bot only!
        """
        game_instance = RPSGame()

        user_choice = user_choice.choice

        won, bot_choice = game_instance.run(user_choice)

        if won is None:
            message = "It's a Draw! Both chose: %s" % user_choice
        elif won is True:
            message = "You Win: %s vs %s" % (user_choice, bot_choice)
        elif won is False:
            message = "You Lose: %s vs %s" % (user_choice, bot_choice)

        await ctx.send(message)


    @commands.command(name="hm",description=f"""
    Play Hangman with Bot,DM Only
    Usage-```{PREFFIX}hm (guess)```
    """)
    @commands.dm_only()
    async def hm(self, ctx, guess: str):
        player_id = ctx.author.id
        hangman_instance = HangmanGame()
        game_over, won = hangman_instance.run(player_id, guess)

        if game_over:
            game_over_message = "You did not win"
            if won:
                game_over_message = "Congrats you won!!"

            game_over_message = game_over_message + \
                " The word was %s" % hangman_instance.get_secret_word()

            await hangman_instance.reset(player_id)
            await ctx.send(game_over_message)

        else:
            await ctx.send("Progress: %s" % hangman_instance.get_progress_string())
            await ctx.send("Guess so far: %s" % hangman_instance.get_guess_string())



    @commands.group(description=f"""
    Guess The Word Game
    """)
    async def gaw(self, ctx):
        ctx.gaw_game = GuessAWordGame()

    @gaw.command(name="start",description=f"""
    Start A Lobby for GAW Game
    Play in The Newly Created Temperory Channel
    Usage-```{PREFFIX}gaw start @user1 @user2 ...```
    """)
    async def gaw_start(self, ctx, *members: discord.Member):
        guild = ctx.guild
        author = ctx.author
        players = list()
        for m in members:
            players.append(m)

        channel = await ctx.gaw_game.start_game(guild, author, players)
        if channel is None:
            await ctx.send("You already have a game. Please close it first")
        else:
            game = ctx.gaw_game.fetch_game()
            await ctx.send("Have fun! Please go to the new game room.")
            round = discord.Embed(description="Guess the Word",
                              colour=discord.Colour.dark_purple())
            round.add_field(name="Hint", value=game.category, inline=False)
            round.add_field(name="Length of word", value=len(game.word), inline=False)

            await channel.send(embed=round)

    @gaw.command(name="g",description=f"""
    Guess The Word
    Usage-```{PREFFIX}gaw g (guess)```
    """)
    async def gaw_guess(self, ctx, guess: str):
        channel = ctx.channel
        author = ctx.author
        result, hint = ctx.gaw_game.guess(channel.id, guess)

        if result is None:
            await ctx.send("You are not allowed to play in this channel!")
        elif result is True:
            await ctx.send("%s you won!" % author.name)
            # start new round
            ctx.gaw_game.new_round(channel)
            new_round = ctx.gaw_game.fetch_game()

            next_round = discord.Embed(description="Guess the Word",
                              colour=discord.Colour.dark_purple())
            next_round.add_field(name="Hint", value=new_round.category, inline=False)
            next_round.add_field(name="Length of word", value=len(new_round.word), inline=False)

            await channel.send(embed=next_round)
        elif result is False and hint != "":
            await ctx.send("%s very close!" % author.name)

    @gaw.command(name="end",description=f"""
    End GAW Game
    Usage-```{PREFFIX}gaw end```
    """)
    async def gaw_end(self, ctx):
        guild = ctx.guild
        channel = ctx.channel
        await ctx.gaw_game.destroy(guild, channel.id)
def setup(bot):
    bot.add_cog(Games(bot))