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

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

    if 'bruh' in message.content.lower():
        await message.channel.send('<:bruh:852935532697616407>')

    # exec_maker('bruh', message.content.lower(), await message.channel.send('<:bruh:852935532697616407>'))

# def exec_maker(check_for, in_what, statement):
#     exec(f"if {check_for} in {in_what}: {statement}")

client.run(TOKEN)