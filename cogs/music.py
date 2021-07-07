import discord
from discord.ext import commands
from youtubesearchpython import VideosSearch
import youtube_dl
import asyncio
import os


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot



    def after(self, error):
        coro = self._client.disconnect()
        fut = asyncio.run_coroutine_threadsafe(coro, self._client.loop).result()



    @commands.group()
    async def music(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.reply("Use a subcommand please!")



    @music.command()
    async def play(self, ctx, *args):
        if not ctx.author.voice:
            await ctx.reply("Join a voice channel first!")
            return
        if not args:
            await ctx.reply("Please provide name of song!")
            return

        
        self._word = ' '.join(args)
        music = VideosSearch(self._word, limit=1)
        link = music.result()["result"][0]["link"]
        bitrate = ctx.author.voice.channel.bitrate


        ydl_opts = {
            'format': 'bestaudio', 
            'noplaylist':'True',
            'quiet': 'True',
        }
        FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(link, download=False)
        URL = info['formats'][0]['url']
        

        self._client = await ctx.author.voice.channel.connect()
        
        
        await ctx.send(link)
        self._client.play(discord.FFmpegPCMAudio(URL, **FFMPEG_OPTIONS), after=self.after)

    

    @music.command()
    async def stop(self, ctx):
        if ctx.guild.voice_client:
            await ctx.guild.voice_client.disconnect()
        else:
            await ctx.reply("I'm not playing any music right now!")



class GuildState():
    def __init__(self, guild_id):
        super().__init__()
        self._guild_id = guild_id
    
    def play(self, requester_id):
        self._requester = requester_id

    def stop(self, messager_id):
        return messager_id == self._requester