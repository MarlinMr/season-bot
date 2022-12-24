import discord
import logging
import json
from discord.ext import commands
from random import random
import random
import datetime
import time


FORMAT = '%(asctime)s %(message)s'
logging.basicConfig(format=FORMAT,filename='./jul/jul.log', encoding='utf-8', level=logging.INFO)

class jul(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def juleinfo(self, ctx):
        """Informasjon fra Nissen"""
        logging.info(f"From `{ctx.message.author}` `{ctx.message.content}` in `{ctx.message.channel}`")
        await ctx.send("🎅: HoHo! Her kan du legge gaver i sekken med `€gigave`. Gjør du det, havner du også på lista over snille og slemme.")

    @commands.command()
    async def titt(self, ctx):
        """Sniktitt i sekken til nissen"""
        logging.info(f"From `{ctx.message.author}` `{ctx.message.content}` in `{ctx.message.channel}`")
        with open("./jul/gaveliste.json", 'r', encoding='utf-8') as f:
            data = json.load(f)
#        gave = data["gaver"][int(random()*len(data["gaver"])-1)]
#        await ctx.send(f"Du ser {gave}. Det er {len(data['gaver'])} gaver i sekken.")
        await ctx.send(f"Sniktittere havner på slemmelista. Det er {len(data['gaver'])} gaver i sekken, {len(data['slemme'])} på slemmelista.")

    @commands.command()
    async def gammeltitt(self, ctx):
        """Sniktitt i den gamle sekken"""
        logging.info(f"From `{ctx.message.author}` `{ctx.message.content}` in `{ctx.message.channel}`")
        with open("./jul/liste.json", 'r', encoding='utf-8') as f:
            data = json.load(f)
        gave = data["gave"][int(random()*len(data["gave"])-1)]
        await ctx.send(f"Du ser {gave}. Det er {len(data['gave'])} gaver i sekken.")

    @commands.command()
    async def gigave(self, ctx, gave):
        """Legger en gave fra deg i sekken"""
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
        gift = str(ctx.message.content[8:]) + " fra <@" + str(ctx.message.author.id) + ">"
        if (gift in data["gaver"]):
            await ctx.message.add_reaction("♻️")
        else:
            data["gaver"].append(gift)
            with open("./jul/gaveliste.json", 'w', encoding='utf-8') as f:
                json.dump(data,f)
                await ctx.message.add_reaction("🎁")

    @commands.command()
    async def tagave(self, ctx):
        """Gir gave til de snille barna"""
        logging.info(f"From `{ctx.message.author}` `{ctx.message.content}` in `{ctx.message.channel}`")
        #current_time = datetime.datetime.now(datetime.timezone.utc).astimezone(datetime.timezone(datetime.timedelta(hours=2)))

        #if current_time < datetime.datetime(year=current_time.year, month=12, day=24, hour=20, minute=0):

        if time.time() < 1671904800:
            await ctx.send("Det er ikkje tid for å motta gåver enno. Prøv igjen den 24. desember klokka 2000.")
            return

        with open('./jul/gaveliste.json', 'r') as f:
            data = json.load(f)
            gifts = data['gaver']
            user_gifts = data.get('user_gifts', {})
            snille = data['snille']
            slemme = data['slemme']

        if str(ctx.message.author.id) in snille:
            if str(ctx.message.author.id) in user_gifts:
                await ctx.send(f'Du har allereie mottatt gåva: {user_gifts[str(ctx.message.author.id)]}')
                return

            gift = random.choice(gifts)
            gifts.remove(gift)
            user_gifts[ctx.message.author.id] = gift
            with open('./jul/gaveliste.json', 'w') as f:
                data['gaver'] = gifts
                data['user_gifts'] = user_gifts
                json.dump(data, f)

            await ctx.send(f'Gåva di er: {gift}')
        elif str(ctx.message.author.id) in slemme:
            user_gifts[ctx.message.author.id] = 'coal'
            with open('./jul/gaveliste.json', 'w') as f:
                data['user_gifts'] = user_gifts
                json.dump(data, f)

            await ctx.send("Du har vore slem i år og vil motta kol i staden for gåva. Brenn ikkje kol på grunn av klimaendringar.")
        else:
            await ctx.send("Du er ikkje i snille- eller slemme-lista. Gje ein gåve med €gigave for å komme på lista.")

    @commands.command()
    async def tos(self,ctx):
        """Printer TOS"""
        logging.info(f"From `{ctx.message.author}` `{ctx.message.content}` in `{ctx.message.channel}`")
        await ctx.send("🎅: HoHo! Ved å legge gave i sekken med €giGave kommandoen, forplikter du å skaffe gaven. Den som får gaven har krav på å få den tilsendt fra deg innen nyttårsaften 2022. Hvis du ikke har råd til gaven du gav, kan du ta opp lån.")

async def setup(bot):
    n = jul(bot)
    await bot.add_cog(n)
