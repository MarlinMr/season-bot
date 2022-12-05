import discord
import logging
import json
from discord.ext import commands
from random import random


FORMAT = '%(asctime)s %(message)s'
logging.basicConfig(format=FORMAT,filename='./jul/jul.log', encoding='utf-8', level=logging.INFO)

class jul(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def gigave(self, ctx):
        """Legger en gave fra deg i sekken"""
        await ctx.send("🎅: HoHo! Nissemor og Nissefar har pussa opp postmottaket sitt, men er ikke helt ferdig enda. Du kan derimot delta i denne betatesten!")
        logging.info(f"From `{ctx.message.author}` `{ctx.message.content}` in `{ctx.message.channel}`")
        with open("./jul/gaveliste.json", 'r', encoding='utf-8') as f:
            data = json.load(f)
        if ((str(ctx.message.author.id) not in data["snille"]) and str(ctx.message.author.id) not in data["slemme"]):
            if (random() > 0.1):
                data["snille"].append(str(ctx.message.author.id))
            else:
                data["slemme"].append(str(ctx.message.author.id))
            with open("./jul/gaveliste.json", 'w', encoding='utf-8') as f:
                json.dump(data,f)
                await ctx.message.add_reaction("📜")
        if (ctx.message.content[8:] in data["gaver"]):
            await ctx.message.add_reaction("♻️")
        else:
            gift = str(ctx.message.content[8:]) + " fra <@" + str(ctx.message.author.id) + ">"
            data["gaver"].append(gift)
            with open("./jul/gaveliste.json", 'w', encoding='utf-8') as f:
                json.dump(data,f)
                await ctx.message.add_reaction("🎁")

    @commands.command()
    async def tagave(self, ctx):
        """Gir gave til de snille barna"""
        await ctx.send("🎅: HoHo! Ingen gaver før julaften!")

async def setup(bot):
    n = jul(bot)
    await bot.add_cog(n)
