import os
import discord
from discord.ext import commands
from cogs.music import Music

TOKEN = os.environ['TOKEN']

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="$", intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')


# @bot.command()
# async def hangman(ctx):
#     if ctx.author.dm_channel == None:
#         await ctx.author.create_dm()
#     await ctx.author.dm_channel.send("Please respond with a phrase you would like to use for your hangman game in **{.guild}**. \n\nPlease keep phrases less than 31 characters".format(ctx))
#     await ctx.reply("Sent you a dm! Please respond there with the phrase you would like to setup")

#     def check(m):
#         return m.channel == ctx.author.dm_channel and m.author == ctx.author and len(m.content) < 31
    
#     msg = await bot.wait_for('message', check=check, timeout=60)
#     word = msg.content
#     await ctx.send("Alright, a hangman game has just started, you can start guessing now!\n```     ——\n    |  |\n       |\n       |\n       |\n       |\n       |\n    ———————```")
#     await ctx.send("```Guesses:```")


# @hangman.error
# async def count_error(ctx, error):
#     if isinstance(error, discord.ext.commands.errors.CommandInvokeError):
#         await ctx.send("You took too long! Please look at your DM's as that's where I'm asking for the phrase you want to use")
    

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.author.bot == True:
        return

    if 'bruh' in message.content.lower():
        await message.channel.send('<:bruh:852935532697616407>')

    if 'i think' in message.content.lower():
        await message.channel.send("NO! You can't think because you don't have a brain.")

    await bot.process_commands(message)

bot.add_cog(Music(bot))

bot.run(TOKEN)
