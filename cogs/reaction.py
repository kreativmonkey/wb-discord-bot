import discord

from discord.ext import commands

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
        

def setup(client):
    client.add_cog(Reaction(client))