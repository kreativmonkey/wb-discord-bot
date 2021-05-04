import discord
import os

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

class Welcome(commands.Cog):
    
    def __init__(self, client):
        self.client = client

    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        guild = discord.utils.get(self.client.guilds, name=GUILD)
        
        print(
            f'{self.client.user} is connected to the following guild:\n'
            f'{guild.name}(id: {guild.id})'
        )    

        channels = '\n - '.join([channel.name for channel in guild.channels])
        print(f'Guild Channels:\n - {channels}')

        # This code will search for the searchstring in the Channel list
        # If there is a channel that starts with that string it will return the channel name
        # so you can use the channelname to connect the bot to the channel and send Messages.
        search_channel = "aee"
        result_channel = next(channel.name for channel in guild.channels if channel.name.startswith(search_channel))
        print(f'\n\n\n{result_channel}')



    @commands.Cog.listener()
    async def on_member_join(self, member):
        # Sending DM to new User with a Welcome message and Informations about the Discord and Discourse server.
        await member.create_dm()
        await member.dm_channel.send(
            f'Hallo {member.name}, wilkommen auf dem WBH-Studenten Discord Server. Als nächstes solltest du dein Studiengang unter #studiengang-zuweisen auswählen. Damit schaltest du die für dich nützlichen Kanäle frei.'
        )

    # Commands
    @commands.command()
    async def ping(self, ctx):
        await ctx.send('Pong!')



def setup(client):
    client.add_cog(Welcome(client))