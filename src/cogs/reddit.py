import time
from disnake.ext import commands, tasks
import feedparser
import asyncio
import pickle


class FreeGameFindings(commands.Cog):
    def __init__(self, bot, channel_id) -> None:
        self.bot = bot
        self.channel_id = channel_id
        self.check_for_new_posts.start()

    @tasks.loop(hours=1)
    async def check_for_new_posts(self):
        d = feedparser.parse(
            "https://www.reddit.com/r/FreeGameFindings/search.rss?q=title%3Aepicgames%20OR%20title%3Aepic%20OR%20title%3Asteam&restrict_sr=on&sort=new&t=all"
        )

        try:
            with open("last_time.data", "rb") as f:
                last_time = pickle.load(f)
        except:
            with open("last_time.data", "wb") as f:
                last_time = time.mktime(time.gmtime())
                pickle.dump(last_time, f)

        for i in d.entries[::-1]:
            pub_time = time.mktime(i.published_parsed)
            if pub_time > last_time:
                print(i.link)
                channel = await self.bot.fetch_channel(self.channel_id)
                await channel.send(i.link)
                with open("last_time.data", "wb") as f:
                    pickle.dump(pub_time, f)
