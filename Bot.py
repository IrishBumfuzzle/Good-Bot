import os
import discord

TOKEN = os.environ['TOKEN']
client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.author.bot == True:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

    if 'bruh' in message.content.lower():
        await message.channel.send('<:bruh:852935532697616407>')

    if 'i think' in message.content.lower():
        await message.channel.send("NO! You can't think because you don't have a brain.")

client.run(TOKEN)