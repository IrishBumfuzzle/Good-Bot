import os
import random
import requests
from lxml import etree
import os
from disnake.ext import commands
from asyncio import exceptions


def fill_form(username, password):
    payload = {"txtUserId": username, "txtPassword": password, "isSubmit": "Yes"}

    with requests.Session() as s:
        s.post("https://dpsfsis.com/Users/index.php", data=payload)

        tree = etree.HTML(
            s.get("https://dpsfsis.com/Admin/SelfDeclarationForm.php").text
        )
        sname = tree.xpath('//*[@id="frmReg"]/div/div[2]/div/p/b/span[1]')[0].text
        sadmission = tree.xpath('//*[@id="frmReg"]/div/div[2]/div/p/b/span[2]')[0].text
        sclass = tree.xpath('//*[@id="frmReg"]/div/div[2]/div/p/b/span[3]')[0].text

        temperature = str(round(random.uniform(96.8, 98.6), 1))
        pulse = str(random.randint(72, 99))
        concentration = str(random.randint(97, 99))
        health_form = {
            "temperature": temperature,
            "pulse": pulse,
            "concentration": concentration,
            "suffering": "NA",
            "is_submit": "Yes",
            "sname": sname,
            "sclass": sclass,
            "sadmission": sadmission,
        }
        s.post("https://dpsfsis.com/Admin/SelfDeclarationForm.php", data=health_form)


@commands.command()
async def fill(ctx):
    """Fills health form for you"""
    if ctx.author.dm_channel == None:
        await ctx.author.create_dm()
    await ctx.reply("Reply to the DM with your username and password")
    await ctx.author.dm_channel.send(
        "Give your username and password in the format 'username':'password' (NO spaces on either side of the colon)"
    )

    def check(m):
        return (
            m.channel == ctx.author.dm_channel
            and m.author == ctx.author
            and len(m.content) < 31
        )

    try:
        msg: str = await ctx.bot.wait_for("message", check=check, timeout=60)
    except exceptions.TimeoutError:
        await ctx.reply(
            "You took too long! Please look at your DM's as that's where I'm asking for the details"
        )
        return

    if ":" not in msg.content:
        await ctx.author.dm_channel.send(
            "Error: missing a colon, please format it in the form 'username':'password'"
        )
    else:
        creds = msg.content.split(":")
        fill_form(creds[0], creds[1])
        await ctx.author.dm_channel.send("Filled, but maybe verify it")
