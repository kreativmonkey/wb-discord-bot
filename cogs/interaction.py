import os
import discord
import requests
import json
import re  # regex

from discord.ext import commands
from dotenv import load_dotenv
from helper.wbdiscourse import WBDiscourse
from helper.extensions import Extensions

BASEURL = 'https://talk.wb-student.org/'

load_dotenv()
APIKEY = os.getenv('API_KEY')
APIUSERNAME = os.getenv('API_USERNAME')


class Interaction(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.wb = WBDiscourse()
        print('Init Interactions')

    # search for a given value in the discourse forum under the BASEURL.
    # to search for posts with tags the searchValue can be like 'tag:sei,bsra'
    # to search for posts from an user the searchValue can be like '@kreativemonkey'
    @commands.command(
        help="Sucht nach einem Wert <searchValue> und gibt maximal <maxResult> Beiträge zurück.\r\n <maxResult>:default(3)",
        brief="Sucht nach einem Wert und gibt die gefundenen Beiträgen zurück."
    )
    async def search(self, ctx, searchValue, maxResult=3):
        requestUrl = self.wb.BaseUrl() + 'search.json'

        HEADERS = {'Api-Key': APIKEY, 'Api-Username': APIUSERNAME}
        # defining a params dict for the parameters to be sent to the API
        PARAMS = {'q': searchValue}
        # sending get request and saving the response as response object
        r = requests.get(url=requestUrl, params=PARAMS, headers=HEADERS)

        # extracting data in json format and get the first 3 found results
        data = r.json()
        chatMessages = self.makeChatResponse(data, maxResult)

        await ctx.send(f'Suchergebnis für "{searchValue}":')
        for message in chatMessages:
            await ctx.send(embed=message)

    def makeChatResponse(self, jsonData, maxMessageCounter):
        result = []
        # foreach posts in the json response ...
        for post in jsonData['posts']:
            # ...check if the result has reached the maxMessageCounter...
            if len(result) != maxMessageCounter:
                # ...get the topicId of the found post to filter for...
                topicId = post['topic_id']
                # ...the topic to get the title of the topic...
                topic = list(filter(lambda x: x['id'] == topicId and (
                    not x['closed'] or not x['archived']), jsonData['topics']))

                if topic:
                    # Creating embedded message for the new added topic
                    embed = discord.Embed(
                        title=topic[0]['title'],
                        description=Extensions.EscapeUrlsInText(post['blurb']),
                        url=self.wb.BaseUrl() + 't/' + str(topicId),
                        # sets the color to the color of the Discourse Categorie
                        color=self.wb.getCategorieColor(
                            topic[0]['category_id'])
                    )

                    embed.set_author(
                        name="@{}".format(post['username']),
                        url='https://talk.wb-student.org/u/{}/summary'.format(
                            post['username']),
                        # Need to be changed to the Userprofileimage if possible
                        icon_url='https://talk.wb-student.org/uploads/default/original/1X/2e6b4f8ea9e4509ec4f99ca73a9906547e80aab0.png'
                    )

                    embed.set_footer(
                        text=self.wb.getCategorieName(topic[0]['category_id'])
                    )

                    result.append(embed)
            else:
                # if result reached the limit => breaking the law
                break

        return result


def setup(client):
    client.add_cog(Interaction(client))


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
