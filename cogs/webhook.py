import os
import hmac
import hashlib
import base64

import aiohttp
from aiohttp import web


import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv


load_dotenv()
GUILD = os.getenv('DISCORD_GUILD')
HOOKTOKEN = os.getenv('WEBHOOK_TOKEN')

app = web.Application()
routes = web.RouteTableDef()

class Webserver(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.web_server.start()
        self.guild = discord.utils.get(self.client.guilds, name=GUILD)

        @routes.get('/')
        async def welcome(request):
            return web.Response(text="Hello, world")

        @routes.post('/hook')
        async def webhook(request):
            print("Calling Webhook")
            if request.headers.get('X-Discourse-Instance') != "https://talk.wb-student.org":
                print("401 Wrong URL")
                return 401

            if request.headers.get('X-Discourse-Event-Type') != "topic":
                print("200 Wrong Event-Type")
                return 200

            if request.headers.get('X-Discourse-Event') != "topic_created":
                print("200 Wrong Event")
                return 200

            data = await request.json()
            
            if not self.checkSignature(request, data):
                return 401

            title = data['topic']['title']

            # Es sollten nur tags mit einer länge >3 und <5 genutzt werden
            # also muss das hier noch optimiert werden.
            tags = sorted(data['topic']['tags'], key=len)

            # Hier muss über tags iteriert werden. Ich denke es sollte erstmal passen
            # wenn man nur auf den ersten Channel reagiert der existiert,
            # also vermutlich mit nem lambda ausdruck oder so umsetzen....
            channelname = next(self.getDiscordChannelName(tag) for tag in tags if self.getDiscordChannelName(tag) is not None)
            channel = self.client.get_channel(channelname)

            # Embed muss dann noch erstellt werden. Aktuell haben wir den Titel, es könnte
            # auch noch ein paar andere Infos genutzt werden, die stehen aktuell unten als
            # Kommentar ;-)
            await channel.send(embed=embed)
            return 200

        self.webserver_port = os.environ.get('PORT', 5000)
        app.add_routes(routes)

    def checkSignature(self, request, data):
        # Authorize the webhook request 
        # Hier müssen wir nochmal schauen wie Discourse den Webhook authorisierung
        # umgesetzt hat. Den Token kann man zumindest dort angeben....
        if not 'X-Discourse-Event-Signature' in request.headers:
            print("401 No Signature")
            return false

        if self.get_signature(data) != request.headers.get('X-Discourse-Event-Signature'):
            print("401 Wrong Signature")
            return false

    def get_signature(self, payload):
        key = bytes(HOOKTOKEN, 'utf-8')
        return hmac.new(key=key, msg=payload, digestmod=hashlib.sha256).hexdigest()

    def getDiscordChannelName(self, searchstring):

        # This code will search for the searchstring in the Channel list
        # If there is a channel that starts with that string it will return the channel name
        # so you can use the channelname to connect the bot to the channel and send Messages.
        result_channel = next(channel.name for channel in self.guild.channels if channel.name.startswith(searchstring))
        return result_channel


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