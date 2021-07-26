import discord
from discord.ext import commands, tasks
import datetime
from time import time



def time_convertor(hours=0, minutes=0, seconds=0):
    hours_convert = hours * 3600
    minutes_convert = minutes * 60
    return seconds + hours_convert + minutes_convert 



class time_related(commands.Cog):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        self.remind_checker.start()
        self.states = []



    @tasks.loop(seconds=1.0)
    async def remind_checker(self):
        for i in range(len(self.states)):
            if self.states[i].epoch <= int(time()):
                await self.states[i].author.send("Your timer is up")
                self.states.pop(i)



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
        await ctx.reply("The time of creation is <t:{0}> in your timezone\nIf there is garbage output, please verify the id is correct".format(time))
        


    @times.command()
    async def remind(self, ctx, *args):
        """DOES SOMETHING"""
        liste = ' '.join(args)
        lis = liste.split("h")
        hours = lis[0]
        lis1 = lis[1].split("m")
        minutes = lis1[0]
        seconds = lis1[1]
        second = time_convertor(int(hours), int(minutes), int(seconds.replace("s", "")))
        fut_time = int(time()) + second
        msg = await ctx.send("Reminder set for <t:{0}>".format(fut_time))
        if ctx.author.dm_channel == None:
            dm = await ctx.author.create_dm()
        else:
            dm = ctx.author.dm_channel
        state = GuildState(fut_time, dm)
        self.states.append(state)
        


class GuildState():
    def __init__(self, epoch, author):
        super().__init__()
        self.epoch = epoch
        self.author = author
            