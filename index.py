#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import discord, json

with open('.secrets.json', 'r',encoding='utf8') as f:
    data = json.load(f)
    token = data["token"]

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(token)
