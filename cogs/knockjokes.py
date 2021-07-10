import discord
from discord.ext import commands
import asyncio



class jokes(commands.Cog):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        


    @commands.Cog.listener()
    async def on_message(self, message):
        if "knock knock" in message.content.lower():
            await message.channel.send("Who's there?")

            def check(m):
                return m.channel == message.channel and m.author == message.author
            
            try:
                msg = await self.bot.wait_for('message', timeout=60 ,check=check)
                await message.channel.send("{0} who?".format(msg.content))
            except asyncio.exceptions.TimeoutError:
                await message.channel.send("You took too much time to reply, so the person slammed the door in your face")