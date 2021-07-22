import discord
from discord.ext import commands, tasks
import datetime
import sqlite3
from time import time



def time_convertor(hours, minutes, seconds):
    hours_convert = hours * 3600
    minutes_convert = minutes * 60
    return seconds + hours_convert + minutes_convert 



class time_related(commands.Cog):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        # self.remind_checker.start()
        self.con = sqlite3.connect(':memory:')
        self.cur = self.con.cursor()
        self.cur.execute("CREATE TABLE reminders (epoch TEXT, author TEXT)")



    # @tasks.loop(seconds=1.0)
    # async def remind_checker(self):
    #     if int(time()) == 



    @commands.group(aliases=["t"])
    async def times(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.reply("Please use a subcommand!")

    # @times.command()
    # def timer(self, ctx, *args):

    #     if len(args) != 3:
    #         ctx.reply("Specify amount of time in `hours minutes seconds`: `h m s`, if the amount of arguments is less than 3, then they will be used from last")
        
    #     time = ''.join(args)
    #     time_list = time.split()



    @times.command()
    async def creation(self, ctx, arg):
        timestamp = (int(arg) >> 22) + 1420070400000
        time = int(timestamp/1000)
        await ctx.reply("The time of creation is <t:{0}> in your timezone".format(time))
        await ctx.send("If there is garbage output, please verify the id is correct")
        


    @times.command()
    async def remind(self, ctx, *args):
        lis = ' '.join(args).split()
        second = time_convertor(int(lis[0]), int(lis[1]), int(lis[2]))
        fut_time = int(time()) + second
        msg = await ctx.send("Set reminder for <t:{0}>".format(fut_time))
        self.cur.execute("INSERT INTO reminders VALUES ('{0}', '{1}')".format(fut_time, msg))
            