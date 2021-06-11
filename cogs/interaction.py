import discord
import json
import re  # regex
import os
from discord.channel import TextChannel
from dotenv import load_dotenv

from discord.ext import commands
from helper.wbdiscourse import WBDiscourse
from helper.extensions import Extensions

# TODO Das abfragen der Environment-Variablen ggf. global umsetzen und darauf zugreifen.
load_dotenv()


class Interaction(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.wb = WBDiscourse()
        print('Init Interactions')

    @commands.has_permissions(administrator=True)
    @commands.command(name='listRoles')
    async def listRoles(self, ctx):
        GUILD = os.getenv('DISCORD_GUILD')
        self.guild = discord.utils.get(self.client.guilds, name=GUILD)
        await ctx.send("\r\n".join([str(r.name + ': ' + str(r.id)) if r.name != '@everyone' else '' for r in self.guild.roles]))

    @commands.has_permissions(administrator=True)
    @commands.command(name='assignRoleToChannels')
    async def assignRoleToChannels(self, ctx, *, roleName):
        print('roleName:' + roleName)
        GUILD = os.getenv('DISCORD_GUILD')
        self.guild = discord.utils.get(self.client.guilds, name=GUILD)
        role = discord.utils.get(self.guild.roles, name=roleName)
        for channel in self.guild.channels:
            print(channel.name)
            if type(channel) is TextChannel:
                # TODO der Channel muss auch noch geprüft werden, ob dieser 'Private' ist, ansonsten wird die Rolle auch einem normalen Channel zugewiesen .. macht vllt nicht so viel Sinn ^^
                # TODO Funktioniert so erstmal... aber bei den Berechtigungen muss nochmal geschaut werden.
                # TODO Des Weiteren müsste auch eine Methode erstellt werden, um die Rolle wieder aus allen Channels zu entfernen. ^^
                overwrite = discord.PermissionOverwrite(
                    read_messages=True, send_messages=True)
                await channel.set_permissions(role, overwrite=overwrite)
                await ctx.send('role assigned to channel: ' + channel.name)

        # await ctx.send('role assigned to channel: ' + ch.name)

    # search for a given value in the discourse forum under the BASEURL.
    # to search for posts with tags the searchValue can be like 'tag:sei,bsra'
    # to search for posts from an user the searchValue can be like '@kreativemonkey'
    @commands.command(
        help="Sucht nach einem Wert <searchValue> und gibt maximal <maxResult> Beiträge zurück.\r\n <maxResult>:default(3)",
        brief="Sucht nach einem Wert und gibt die gefundenen Beiträgen zurück."
    )
    async def search(self, ctx, searchValue, maxResult=3):
        requestUrl = self.wb.BaseUrl() + 'search.json'

        # using the discourse api client to search on the discourse server
        # and receive result as json
        data = self.wb.search(searchValue)

        chatMessages = self.makeChatResponse(data, maxResult)

        if chatMessages:
            await ctx.send(f'Suchergebnis für "{searchValue}":')
            for message in chatMessages:
                await ctx.send(embed=message)
        else:
            await ctx.send(f'Die Suche ergab keinen Treffer.')

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
