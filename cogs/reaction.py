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
        requestUrl = BASEURL + 'search.json'
        HEADERS = {'Api-Key': APIKEY, 'Api-Username': APIUSERNAME}
        # defining a params dict for the parameters to be sent to the API
        PARAMS = {'q': searchValue}
        # sending get request and saving the response as response object
        r = requests.get(url=requestUrl, params=PARAMS, headers=HEADERS)

        # extracting data in json format
        data = r.json()
        print(data)
        # the data have to shorten because its to long
        await ctx.send(data)

        # await ctx.send(r.content)


def setup(client):
    client.add_cog(Reaction(client))


# response of the search request
# {
#     "posts": [
#         {
#             "id": 125,
#             "name": "Philipp S.",
#             "username": "Phil",
#             "avatar_template": "/letter_avatar_proxy/v4/letter/p/e95f7d/{size}.png",
#             "created_at": "2021-05-01T15:26:59.798Z",
#             "like_count": 1,
#             "blurb": "...vainsel/ Java ist auch eine Insel 978-3-8362-7737-2 #video-playlist-tv-2 Video-Playlist :tv: Youtube-Playlists Titel Sprache Kanal https://youtube.de Test - BestPractice Deutsch https://youtube.de Test #wichtige-coding-prinzipien-3 Wichtige Coding-Prinzipien SOLID - https://de.wikipedia.org/wiki/Prinzip...",
#             "post_number": 1,
#             "topic_id": 51
#         },
#         ...
#     ],
#     "topics": [
#         {
#             "id": 51,
#             "title": "GOP - Grundlagen objektorientierte Programmierung",
#             "fancy_title": "GOP - Grundlagen objektorientierte Programmierung",
#             "slug": "gop-grundlagen-objektorientierte-programmierung",
#             "posts_count": 1,
#             "reply_count": 0,
#             "highest_post_number": 1,
#             "created_at": "2021-05-01T15:26:59.644Z",
#             "last_posted_at": "2021-05-01T15:26:59.798Z",
#             "bumped": true,
#             "bumped_at": "2021-05-02T12:02:50.354Z",
#             "archetype": "regular",
#             "unseen": false,
#             "pinned": false,
#             "unpinned": null,
#             "visible": true,
#             "closed": false,
#             "archived": false,
#             "bookmarked": null,
#             "liked": null,
#             "tags": [
#                 "wissensmanagement",
#                 "gop"
#             ],
#             "category_id": 10,
#             "has_accepted_answer": false
#         },
#         ....
#     ],
#     "users": [],
#     "categories": [],
#     "tags": [],
#     "groups": [],
#     "grouped_search_result": {
#         "more_posts": null,
#         "more_users": null,
#         "more_categories": null,
#         "term": "test",
#         "search_log_id": 49,
#         "more_full_page_results": null,
#         "can_create_topic": true,
#         "error": null,
#         "post_ids": [
#             125,
#             177,
#             12,
#             130,
#             55
#         ],
#         "user_ids": [],
#         "category_ids": [],
#         "tag_ids": [],
#         "group_ids": []
#     }
# }
