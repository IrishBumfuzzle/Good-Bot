import discord
from discord.ext import commands
import re
from asyncio import exceptions



class Hangman(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.states = {}
        


    @commands.group(aliases=["h"])
    async def hangman(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.reply("Please use a subcommand!")



    @hangman.command()
    async def create(self, ctx):
        if ctx.author.dm_channel == None:
            await ctx.author.create_dm()
        await ctx.author.dm_channel.send("Please respond with a phrase you would like to use for your hangman game in **{.guild}**. \n\nPlease keep phrases less than 31 characters".format(ctx))
        await ctx.reply("Sent you a dm! Please respond there with the phrase you would like to setup")

        def check(m):
            return m.channel == ctx.author.dm_channel and m.author == ctx.author and len(m.content) < 31
        try:
            msg = await self.bot.wait_for('message', check=check, timeout=60)
        except exceptions.TimeoutError:
            await ctx.send("You took too long! Please look at your DM's as that's where I'm asking for the phrase you want to use")
            return

        word = msg.content.replace(" ", "  ")
        self.states[ctx.guild.id] = GuildState(word)
        await ctx.send("Alright, a hangman game has just started, you can start guessing now!\n```     ——\n    |  |\n       |\n       |\n       |\n       |\n       |\n    ———————```")
        await ctx.send("```Guesses:\nWord: {0}```".format(re.sub('\S', '_ ', word)))



    def output(self, number_of_wrong_guesses):
        cases = {
            0: "```     ——\n    |  |\n       |\n       |\n       |\n       |\n       |\n    ———————```",
            1: "```     ——\n    |  |\n    o  |\n       |\n       |\n       |\n       |\n    ———————```",
            2: "```     ——\n    |  |\n    o  |\n   /   |\n       |\n       |\n       |\n    ———————```",
            3: "```     ——\n    |  |\n    o  |\n   /|  |\n       |\n       |\n       |\n    ———————```",
            4: "```     ——\n    |  |\n    o  |\n   /|\ |\n       |\n       |\n       |\n    ———————```",
            5: "```     ——\n    |  |\n    o  |\n   /|\ |\n    |  |\n       |\n       |\n    ———————```",
            6: "```     ——\n    |  |\n    o  |\n   /|\ |\n    |  |\n   /   |\n       |\n    ———————```",
            7: "```     ——\n    |  |\n    o  |\n   /|\ |\n    |  |\n   / \ |\n       |\n    ———————```"
        }
        return cases.get(number_of_wrong_guesses)



    def correct_output(self, guild_id, letter):
        state = self.states[guild_id]
        word = state.word
        guesses = state.guesses
        replace = re.sub('[^{0} ]'.format(''.join(str(e) for e in guesses)), '_ ', word)
        return replace



    @hangman.command()
    async def guess(self, ctx, args):
        if len(args) != 1:
            await ctx.reply("Only 1 letter please.")
        elif ctx.guild.id in self.states:
            state = self.states[ctx.guild.id]
            word = state.word
            guess_word = ''.join(args)
            if guess_word in state.word:
                state.guesses.append(guess_word)
                await ctx.reply("That's correct!")
                await ctx.send(self.output(state.wrong))
                if state.revealed == len(word) - word.count(' '):
                    await ctx.send("You guesses the phrase! The phrase was {0}".format(state.word))
                else: 
                    await ctx.send("```Guesses: {0}\nWord: {1}```".format(state.wrong_guess(), self.correct_output(ctx.guild.id, guess_word)))
                    state.revealed += 1
            else:
                state.guesses.append(guess_word)
                await ctx.reply("That's wrong.")
                state.wrong += 1
                await ctx.send(self.output(state.wrong))
                if state.wrong == 7:
                    await ctx.send("You lost the game. The phrase was {0}".format(state.word))
                else:
                    await ctx.send("```Guesses: {0}\nWord: {1}```".format(state.wrong_guess(), self.correct_output(ctx.guild.id, guess_word)))
        else:
            ctx.reply("No hangman game is going on!")



class GuildState():
    def __init__(self, word):
        self.word = word
        self.guesses = []
        self.revealed = 0
        self.wrong = 0


    def wrong_guess(self):
        return ', '.join(e for e in self.guesses)