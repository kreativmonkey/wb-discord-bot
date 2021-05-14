import os
import hmac
import hashlib
import base64
import json

import aiohttp
from aiohttp import web


import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv

from helper.wbdiscourse import WBDiscourse
from helper.extensions import Extensions as ex

load_dotenv()
GUILD = os.getenv('DISCORD_GUILD')
HOOKTOKEN = os.getenv('WEBHOOK_TOKEN')

app = web.Application()
routes = web.RouteTableDef()

class Webserver(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.web_server.start()
        self.guild = None 
        self.wb = WBDiscourse()

        @commands.Cog.listener()
        async def on_ready(self):
            self.guild = discord.utils.get(client.guilds, name=GUILD)


        @routes.get('/')
        async def welcome(request):
            return web.Response(text="Hello, world")

        @routes.post('/hook')
        async def webhook(request):
            print("Calling Webhook")
            # Authorize the request
            if not self.authorizedRequest(request, await request.read()):
                print('401 Unauthorized')
                return web.Response(text=json.dumps("{ 'status' : 'unauthorized' }"))

            # filter webhook with wrong event-type
            if request.headers.get('X-Discourse-Event-Type') != "topic":
                print("202 Wrong Event-Type")
                return web.Response(text=json.dumps("{ 'status' : 'wrong event type' }"))

            # filter webhook with wrong event
            if request.headers.get('X-Discourse-Event') != "topic_created":
                print("202 Wrong Event")
                return web.Response(text=json.dumps("{ 'status' : 'wrong event' }"))

            # getting request json data
            data = await request.json()

            # search for the channel_id by topic tags
            channelid = self.getDiscordChannelId(data['topic']['tags'])
            if channelid == None:
                return web.Response(text=json.dumps("{ 'status' : 'no content' }"))

            # get the channel from the channel_id to send the message
            channel = self.client.get_channel(channelid)
        
            # sending the message to the cannel
            await channel.send('**Neues Thema auf Discourse**', embed=wb.embed_from_topic_json(data))
            return web.Response(text=json.dumps("{ 'status' : 'success' }"))

        self.webserver_port = os.environ.get('PORT', 5000)
        app.add_routes(routes)

    # Verify the Webhook Signature
    # The X-Discourse-Event-Signature consists of 'sha256=' hmac of raw payload.
    def authorizedRequest(self, request, payload):
        # Is the request from the right Instance
        if request.headers.get('X-Discourse-Instance') != self.wb.BaseUrl():
            return False

        # Check if the X-Discourse-Event-Signature is present
        if not 'X-Discourse-Event-Signature' in request.headers:
            return False

        # Generate the signature from the raw payload with sha256 and hmac
        signature = hmac.new(key=bytes(HOOKTOKEN, 'utf-8'), msg=payload, digestmod=hashlib.sha256).hexdigest()
        
        # Check if the signature is simular to the signature in the header by cutting of 'sha256'
        if signature != request.headers.get('X-Discourse-Event-Signature')[7:]:
            print(f"401 Wrong Signature: {signature}")
            return False

        print('Verified Request!')
        return True

    def getDiscordChannelId(self, search):
        if not search:
            return None

        search.sort(key=len)
        self.guild = discord.utils.get(self.client.guilds, name=GUILD)
        # This code will search for the searchstring in the Channel list
        # If there is a channel that starts with that string it will return the channel name
        # so you can use the channelname to connect the bot to the channel and send Messages.
        for s in search:
            print(f"Searching for: {s}")
            result_channel = next(channel.name for channel in self.guild.channels if channel.name.startswith(s))
            if result_channel != -1:
                print(f"Found {s} in {result_channel}")
                break

        if result_channel == -1:
            return None
        
        # Get the channel to return channelid
        channel = discord.utils.get(self.guild.channels, name=result_channel)
        return channel.id

    @tasks.loop()
    async def web_server(self):
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, host='0.0.0.0', port=self.webserver_port)
        await site.start()

    @web_server.before_loop
    async def web_server_before_loop(self):
        await self.client.wait_until_ready()

def setup(client):
    client.add_cog(Webserver(client))


'''
{
  "topic": {
    "tags": [
      "prüfung",
      "obk"
    ],
    "id": 78,
    "title": "Erfahrung und Ablauf OBK",
    "fancy_title": "Erfahrung und Ablauf OBK",
    "posts_count": 1,
    "created_at": "2021-05-04T07:24:00.522Z",
    "views": 1,
    "reply_count": 0,
    "like_count": 0,
    "last_posted_at": "2021-05-04T07:24:00.637Z",
    "visible": true,
    "closed": false,
    "archived": false,
    "archetype": "regular",
    "slug": "erfahrung-und-ablauf-obk",
    "category_id": 9,
    "word_count": 493,
    "deleted_at": null,
    "user_id": 1,
    "featured_link": null,
    "pinned_globally": false,
    "pinned_at": null,
    "pinned_until": null,
    "unpinned": null,
    "pinned": false,
    "highest_post_number": 1,
    "deleted_by": null,
    "has_deleted": false,
    "bookmarked": false,
    "participant_count": 1,
    "thumbnails": null,
    "created_by": {
      "id": 1,
      "username": "kreativmonkey",
      "name": "Sebastian P.",
      "avatar_template": "/user_avatar/talk.wb-student.org/kreativmonkey/{size}/4_2.png"
    },
    "last_poster": {
      "id": 1,
      "username": "kreativmonkey",
      "name": "Sebastian P.",
      "avatar_template": "/user_avatar/talk.wb-student.org/kreativmonkey/{size}/4_2.png"
    },
    "tags_disable_ads": false
  }
}
'''