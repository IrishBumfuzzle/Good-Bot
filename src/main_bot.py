import os
import disnake
from disnake.ext import commands
from cogs import fun, hangman, music, time_related, health_form
import logging

logging.basicConfig()

TOKEN = os.environ["TOKEN"]

intents = disnake.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="$", intents=intents)


@bot.event
async def on_ready():
    print(f"{bot.user} has connected to disnake!")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.author.bot == True:
        return

    if "bruh" in message.content.lower():
        await message.add_reaction("<:bruh:852935532697616407>")

    if "i think" in message.content.lower():
        await message.channel.send(
            "NO! You can't think because you don't have a brain."
        )

    if "sus" in message.content.lower():
        await message.add_reaction("<:sus:862227814471565322>")

    if "no u" in message.content.lower():
        await message.channel.send("no u")

    await bot.process_commands(message)


bot.add_cog(music.Music(bot))
bot.add_cog(hangman.Hangman(bot))
bot.add_cog(fun.Fun(bot))
bot.add_cog(time_related.time_related(bot))
bot.add_command(health_form.fill)

bot.run(TOKEN)
