import disnake
from disnake.ext import commands
import asyncio
from random import randint
import sqlite3
from foaas import random
import re



class Fun(commands.Cog):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        


    @commands.Cog.listener()
    async def on_message(self, message):
        if "knock knock" in message.content.lower():
            if message.author == self.bot.user:
                return

            if message.author.bot == True:
                return

            await message.channel.send("Who's there?")

            def check(m):
                return m.channel == message.channel and m.author == message.author
            
            try:
                msg = await self.bot.wait_for('message', timeout=60 ,check=check)
                await message.channel.send("{0} who?".format(msg.content))
            except asyncio.exceptions.TimeoutError:
                await message.channel.send("You took too much time to reply, so the person slammed the door in your face")

    @commands.command()
    async def knockknock(self, ctx):
        await ctx.reply("Knock knock!")

        def check2(m):
            return m.channel == ctx.channel and m.author == ctx.author and "there" in m.content.lower()

        try:
            await self.bot.wait_for('message', timeout=60, check=check2)
        except asyncio.exceptions.TimeoutError:
            await ctx.send("You took too much time to reply, so the person slammed the door in your face")


        number = randint(1, 99)
        con = sqlite3.connect("Data.db")
        cur = con.cursor()
        out = cur.execute(f"SELECT STARTER, PUNCHLINE FROM jokes WHERE id = {number}")
        joke = out.fetchone()
        
        
        await ctx.send(joke[0])

        def check(m):
            return m.channel == ctx.channel and m.author == ctx.author and "who" in m.content.lower()

        try:
            await self.bot.wait_for('message', timeout=60, check=check)
            await ctx.send(joke[1])
        except asyncio.exceptions.TimeoutError:
            await ctx.send("You didn't ask me who I am. I'm going, hmmph!")



    @commands.command()
    async def fuck(self, ctx):
        message = ctx.message.content.lower()
        match = re.search('(?<=<@!)\d{18}(?=>)', message)
        if match:
            message = random(from_name=f"<@!{ctx.author.id}>", name=f"<@!{message[match.start():match.end()]}>")
            await ctx.reply(message)
        else:
            message = random(from_name=f"<@!{ctx.author.id}>")
            await ctx.reply(message)