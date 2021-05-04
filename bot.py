import os
import sys

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
        
@client.event
async def on_member_join(member):
    # Sending DM to new User with a Welcome message and Informations about the Discord and Discourse server.
    await member.create_dm()
    await member.dm_channel.send(
        f'Hallo {member.name}, wilkommen auf dem WBH-Studenten Discord Server. Als nächstes solltest du dein Studiengang unter #studiengang-zuweisen auswählen. Damit schaltest du die für dich nützlichen Kanäle frei.'
    )
    
@client.event
async def on_error(event, *args, **kwargs):
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise

    
client.run(TOKEN)
