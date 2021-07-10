import os
import discord
from discord.ext import commands
from cogs import hangman, knockjokes, music

TOKEN = os.environ['TOKEN']

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="$", intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

    

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

    if 'sus' in message.content.lower():
        await message.add_reaction("<:sus:862227814471565322>")

    await bot.process_commands(message)

bot.add_cog(music.Music(bot))
bot.add_cog(hangman.Hangman(bot))
bot.add_cog(knockjokes.jokes(bot))

bot.run(TOKEN)
