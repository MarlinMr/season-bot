import discord
import logging
import json
from discord.ext import commands
import random
import datetime
import time


FORMAT = '%(asctime)s %(message)s'
logging.basicConfig(format=FORMAT,filename='./jul/jul.log', encoding='utf-8', level=logging.INFO)

random_gave = 0

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
        random_gave = int(random.random()*len(data["gaver"])-1)
        gave = data["gaver"][random_gave]
        embed = discord.Embed(title="Gavesekken", color=0xff0000, description=f"Det er {len(data['gaver'])} gaver i sekken.")
        embed.add_field(name='Gaver du ser', value=gave, inline=True)
        delta = 1672077600 - time.time()
        embed.set_footer(text=f"Nissen reiser videre om {int((delta/60)/60)} timer")
        await ctx.send(embed=embed)
        data["random_gave"] = random_gave
        with open('./jul/gaveliste.json', 'w') as f:
            json.dump(data, f)
        #await ctx.send(f"Sniktittere havner på slemmelista. Det er {len(data['gaver'])} gaver i sekken, {len(data['slemme'])} på slemmelista.")

    @commands.command()
    async def gammeltitt(self, ctx):
        """Sniktitt i den gamle sekken"""
        logging.info(f"From `{ctx.message.author}` `{ctx.message.content}` in `{ctx.message.channel}`")
        with open("./jul/liste.json", 'r', encoding='utf-8') as f:
            data = json.load(f)
        gave = data["gave"][int(random.random()*len(data["gave"])-1)]
        await ctx.send(f"Du ser {gave}. Det er {len(data['gave'])} gaver i sekken.")

    @commands.command()
    async def gigave(self, ctx, gave):
        """Legger en gave fra deg i sekken"""
        logging.info(f"From `{ctx.message.author}` `{ctx.message.content}` in `{ctx.message.channel}`")
        with open("./jul/gaveliste.json", 'r', encoding='utf-8') as f:
            data = json.load(f)
        if ((str(ctx.message.author.id) not in data["snille"]) and str(ctx.message.author.id) not in data["slemme"]):
            if (random.random() > 0.1):
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
            user_gifts_list3 = data.get('user_gifts_list3', {})
            snille = data['snille']
            slemme = data['slemme']

        if str(ctx.message.author.id) in snille:
#            if str(ctx.message.author.id) in user_gifts:
#                await ctx.send(f'Du har allereie mottatt gåva: {user_gifts[str(ctx.message.author.id)]}')
            if str(ctx.message.author.id) in user_gifts_list3:
                if len(user_gifts_list3[str(ctx.message.author.id)]) > 9:
                    message = f'Du har allereie fått {len(user_gifts_list3[str(ctx.message.author.id)])} gåvar.'
                    embed = discord.Embed(title="Gavesekken", color=0xff0000)
                    embed.add_field(name='Dine Gaver', value=message, inline=True)
                    await ctx.send(embed=embed)
                    return

            if data["random_gave"] < len(gifts):
                gift = data["gaver"][data["random_gave"]]
                data["random_number"] = int(random.random()*len(data["gaver"])-1)
            else:
                gift = random.choice(gifts)
            gifts.remove(gift)
            if str(ctx.message.author.id) in user_gifts_list3:
                user_gifts_list3[str(ctx.message.author.id)].append(gift)
            else:
                user_gifts_list3[str(ctx.message.author.id)] = [gift]
            with open('./jul/gaveliste.json', 'w') as f:
                data['gaver'] = gifts
                data['user_gifts_list3'] = user_gifts_list3
                json.dump(data, f)

            await ctx.send(f'Gåva di er: {gift}')
        elif str(ctx.message.author.id) in slemme:
            if str(ctx.message.author.id) in user_gifts_list3:
                if len(user_gifts_list3[str(ctx.message.author.id)]) > 4:
                    message = f'Du har allereie fått 5 gåvar. Slemme barn får ikkje fler.'
                    embed = discord.Embed(title="Gavesekken", color=0xff0000)
                    embed.add_field(name='Dine Gaver', value=message, inline=True)
                    await ctx.send(embed=embed)
                    return

            if data["random_gave"] < len(gifts):
                gift = data["gaver"][data["random_gave"]]
                data["random_number"] = int(random.random()*len(data["gaver"])-1)
            else:
                gift = random.choice(gifts)
            gifts.remove(gift)
            if str(ctx.message.author.id) in user_gifts_list3:
                user_gifts_list3[str(ctx.message.author.id)].append(gift)
            else:
                user_gifts_list3[str(ctx.message.author.id)] = [gift]
            with open('./jul/gaveliste.json', 'w') as f:
                data['gaver'] = gifts
                data['user_gifts_list3'] = user_gifts_list3
                json.dump(data, f)

            await ctx.send(f'Gåva di er: {gift}')

#            gift = random.choice(gifts)
#            gifts.remove(gift)
#            if str(ctx.message.author.id) in user_gifts_list3:
#                user_gifts_list3[str(ctx.message.author.id)].append(gift)
#            else:
#                user_gifts_list3[str(ctx.message.author.id)] = [gift]
#            with open('./jul/gaveliste.json', 'w') as f:
#                data['gaver'] = gifts
##                data['user_gifts_list3'] = user_gifts_list3
#                json.dump(data, f)
            #user_gifts[ctx.message.author.id] = 'coal'
            #with open('./jul/gaveliste.json', 'w') as f:
                #data['user_gifts'] = user_gifts
                #json.dump(data, f)

            #await ctx.send("Du har vore slem i år og vil motta kol i staden for gåva. Brenn ikkje kol på grunn av klimaendringar.")
        else:
            await ctx.send("Du er ikkje i snille- eller slemme-lista. Gje ein gåve med €gigave for å komme på lista.")

    @commands.command()
    async def minegaver(self,ctx):
        """Viser hvilke gaver du har tatt"""
        with open('./jul/gaveliste.json', 'r') as f:
            data = json.load(f)
        if str(ctx.message.author.id) in data["user_gifts"]:
            if str(ctx.message.author.id) in data["user_gifts_list3"]:
                user_gifts = data['user_gifts'][str(ctx.message.author.id)]
                user_gifts_list3 = data['user_gifts_list3'][str(ctx.message.author.id)]
                if str(ctx.message.author.id) in data["snille"]:
                    left = 10 - len(data['user_gifts_list3'][str(ctx.message.author.id)])
                if str(ctx.message.author.id) in data["slemme"]:
                    left = 5 - len(data['user_gifts_list3'][str(ctx.message.author.id)])
                message = f"{user_gifts}"
                for gift in user_gifts_list3:
                    message = message + f"\n{gift[:75]}"
                embed = discord.Embed(title="Gavesekken", color=0xff0000, description=f"\nDu har {left} gaver igjen.")
                embed.add_field(name='Dine Gaver', value=message, inline=True)
                await ctx.send(embed=embed)
            else:
                user_gifts = data['user_gifts'][str(ctx.message.author.id)]
                message = f"{user_gifts}"
                embed = discord.Embed(title="Gavesekken", color=0xff0000, description="Du har 10 gaver igjen.")
                embed.add_field(name='Dine Gaver', value=message, inline=True)
        elif str(ctx.message.author.id) in data["user_gifts_list3"]:
            user_gifts_list3 = data['user_gifts_list3'][str(ctx.message.author.id)]
            if str(ctx.message.author.id) in data["snille"]:
                left = 10 - len(data['user_gifts_list3'][str(ctx.message.author.id)])
            if str(ctx.message.author.id) in data["slemme"]:
                left = 5 - len(data['user_gifts_list3'][str(ctx.message.author.id)])
            message = ''
            for gift in user_gifts_list3:
                message = message + f"\n{gift[:75]}"
            embed = discord.Embed(title="Gavesekken", color=0xff0000, description=f"\nDu har {left} gaver igjen.")
            embed.add_field(name='Dine Gaver', value=message, inline=True)
            await ctx.send(embed=embed)

    @commands.command()
    async def tos(self,ctx):
        """Printer TOS"""
        logging.info(f"From `{ctx.message.author}` `{ctx.message.content}` in `{ctx.message.channel}`")
        await ctx.send("🎅: HoHo! Ved å legge gave i sekken med €giGave kommandoen, forplikter du å skaffe gaven. Den som får gaven har krav på å få den tilsendt fra deg innen nyttårsaften 2022. Hvis du ikke har råd til gaven du gav, kan du ta opp lån.")


async def setup(bot):
    n = jul(bot)
    await bot.add_cog(n)
