import os
import discord
from discord.ext import commands
import requests
from dotenv import load_dotenv

BASEURL = 'https://talk.wb-student.org/'

load_dotenv()
APIKEY = os.getenv('API_KEY')
APIUSERNAME = os.getenv('API_USERNAME')


class Reaction(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Events
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        # Reagiere auf das kürzel HZP um Informationen für die Hochschulzugangsprüfung an zu zeigen.
        # ToDo: Nur alle x Tage oder alle x Meldungen darauf reagieren...
        if 'hzp' in message.content.lower():
            await message.channel.send('**Wichtige Informationen** zur **HZP** findest du auch auf unserem Discourse unter: https://talk.wb-student.org/tag/hzp')

    # search for a given value in the discourse forum under the BASEURL.
    # to search for posts with tags the searchValue can be like 'tag:sei,bsra'
    # to search for posts from an user the searchValue can be like '@kreativemonkey'
    @commands.command()
    async def search(self, ctx, searchValue):
        requestUrl = BASEURL + 'search'
        HEADERS = {'Api-Key': APIKEY, 'Api-Username': APIUSERNAME}

        # defining a params dict for the parameters to be sent to the API
        PARAMS = {'q': searchValue}
        # sending get request and saving the response as response object
        r = requests.get(url=requestUrl, params=PARAMS, headers=HEADERS)
        print(r.content)

        # extracting data in json format
        # data = r.json()
        # await ctx.send(data)

        await ctx.send(r.content)


def setup(client):
    client.add_cog(Reaction(client))
