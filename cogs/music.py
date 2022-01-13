import disnake
from disnake.ext import commands
from youtubesearchpython import VideosSearch
import yt_dlp
import asyncio



class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.states = {}



    def state_handler(self, guild):
        if guild.id in self.states:
            return self.states[guild.id]
        else:
            self.states[guild.id] = GuildState(guild.id)
            return self.states[guild.id]



    def play_song(self, client, link):
        ydl_opts = {
            'format': 'bestaudio',
            'cookiefile': 'cookies.txt',
            'noplaylist':'True',
            'quiet': 'True',
        }
        FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.sanitize_info(ydl.extract_info(link, download=False))
        URL = info['formats'][3]['url']
        

        def after(error):
            state = self.state_handler(self._guild)
            next_song = state.remove_queue()
            if next_song:
                self.play_song(client, next_song)
            else:
                coro = self._client.disconnect()
                asyncio.run_coroutine_threadsafe(coro, self._client.loop).result()

        client.play(disnake.FFmpegPCMAudio(URL, **FFMPEG_OPTIONS), after=after)


    @commands.group(aliases=["m"])
    async def music(self, ctx):
        '''Plays music!'''
        if ctx.invoked_subcommand is None:
            await ctx.reply("Use a subcommand please!")



    @music.command()
    async def play(self, ctx, *, args):
        '''Add song's name or link after the command for playing through Youtube'''
        if not ctx.author.voice:
            await ctx.reply("Join a voice channel first!")
            return
        if not args:
            await ctx.reply("Please provide name of song!")
            return
        

        self._word = args
        # self._word = re.sub('[^A-Za-z0-9 ]+', '', ' '.join(args))
        music = VideosSearch(self._word, limit=1)
        link = music.result()["result"][0]["link"]


        try:
            self._client = await ctx.author.voice.channel.connect()
            self._guild = ctx.guild
        except disnake.errors.ClientException:
            state = self.state_handler(ctx.guild)
            state.add_queue(link)
            state.starter_message = ctx
            await ctx.reply("Added {0} to queue".format(link))
            return

        self.play_song(self._client, link)
        await ctx.reply("Now playing " + link)



    @music.command()
    async def stop(self, ctx):
        '''Stops the music playback, if any'''
        if ctx.guild.voice_client:
            await self.clearqueue(ctx)
            await ctx.guild.voice_client.disconnect()
            await ctx.reply("Stopped playback")
        else:
            await ctx.reply("I'm not playing any music right now!")



    @music.command(aliases=["cq"])
    async def clearqueue(self, ctx):
        '''Clears the queue'''
        state = self.state_handler(ctx.guild)
        state.queue = []
        await ctx.reply("Cleared queue")



class GuildState():
    def __init__(self, guild_id):
        super().__init__()
        self._guild_id = guild_id
        self.queue = []
        self.starter_message = None
    

    def add_queue(self, song):
        self.queue.append(song)


    def remove_queue(self):
        if self.queue:
            return self.queue.pop(0)
        else:
            return False