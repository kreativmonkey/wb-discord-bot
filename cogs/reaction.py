import os
import discord
import requests
import json
import re  # regex
from datetime import datetime

from discord.ext import commands
from dotenv import load_dotenv


BASEURL = 'https://talk.wb-student.org/'

load_dotenv()
APIKEY = os.getenv('API_KEY')
APIUSERNAME = os.getenv('API_USERNAME')

# TODO: 
# - List of Keywords: Text to support multiple Keywords for one Text and support Multiple Texts

class Reaction(commands.Cog):

    def __init__(self, client):
        self.client = client
        print('Init Reactions')
        self.last_keyword_message = []

    # Events
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        # react on keywords related to 'hzp' to show some informations about.
        hzpKeywords = ('hzp', 'hochschulzugangsprüfung', 'zugangsprüfung')

        if any(keyWord in message.content.lower() for keyWord in hzpKeywords):
            # checks for last 25 messages, whether the bot already send this message in the last 10 days
            if await self.messageAlreadySendBefore(message.channel, '**Wichtige Informationen** zur **HZP**'):
                await message.channel.send('**Wichtige Informationen** zur **HZP** findest du auch auf unserem Discourse unter: https://talk.wb-student.org/tag/hzp')

    # checks channels last 25 messages whether the bot already send a messages, starts with <messageStart>, in the last 10 days
    async def messageAlreadySendBefore(self, channel, messageStart):
        async for message in channel.history(limit=25):
            if message.author.bot and message.content.startswith(messageStart) and (datetime.now() - message.created_at).days < 10:
                return False

        return True

def setup(client):
    client.add_cog(Reaction(client))
