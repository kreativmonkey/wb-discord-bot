import os


import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()

@client.event
async def on_ready():
    guild = discord.utils.get(client.guilds, name=GUILD)
    
    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )    
    
    channels = '\n - '.join([channel.name for channel in guild.channels])
    print(f'Guild Channels:\n - {channels}')
	
	
@client.event
async def on_message(message):
	if message.author.bot:
		return
		
    # Reagiere auf das kürzel HZP um Informationen für die Hochschulzugangsprüfung an zu zeigen.
    # ToDo: Nur alle x Tage oder alle x Meldungen darauf reagieren...
	if 'hzp' in message.content.lower():
		await message.channel.send('**Wichtige Informationen** zur **HZP** findest du auch auf unserem Discourse unter: https://talk.wb-student.org/tag/hzp')
    
client.run(TOKEN)
