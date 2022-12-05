#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import discord, json, os, asyncio
from discord.ext import commands

with open('.secrets.json', 'r',encoding='utf8') as f:
    data = json.load(f)
    token = data["token"]

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='€', case_insensitive=True, intents=intents)

async def load():
    for guild in bot.guilds:
        print(f'Logged in as: {bot.user.name} in {guild.name}. Version: {discord.__version__}')
    print("Loading cogs...")
    for file in os.listdir('./cogs'):
        if file.endswith("jul.py"):
            await bot.load_extension(f"cogs.{file[:-3]}")

async def main():
    print("Starting bot...")
    await load()
    await bot.start(token, reconnect=True)

asyncio.run(main())
