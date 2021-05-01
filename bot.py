import os


import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

@client.event
async def on_ready():
	print('Wir sind eingeloggt als User {}'.format(client.user.name))
	
	
@client.event
async def on_message(message):
	if message.author.bot:
		return
		
    # Reagiere auf das kürzel HZP um Informationen für die Hochschulzugangsprüfung an zu zeigen.
    # ToDo: Nur alle x Tage oder alle x Meldungen darauf reagieren...
	if 'hzp' in message.content.lower():
		await message.channel.send('**Wichtige Informationen** zur **HZP** findest du auch auf unserem Discourse unter: https://talk.wb-student.org/tag/hzp')

client.run(TOKEN)
