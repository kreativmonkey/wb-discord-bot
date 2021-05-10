import discord

from discord.ext import commands


class Reaction(commands.Cog):

    def __init__(self, client):
        self.client = client
        print('Init Reactions')
        self.last_keyword_message = []

    # Events
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        # TODO: add more keywords
        # react on keywords related to 'hzp' to show some informations about.
        hzpKeywords = ('hzp', 'hochschulzugangsprüfung', 'zugangsprüfung')
        obkKeywords = ('obk', 'open book klausur',
                       'open-book-klausur', 'obk\'s', 'obks')

        if any(keyWord in message.content.lower() for keyWord in hzpKeywords):
            # checks for last 25 messages, whether the bot already send this message in the last 10 days
            if await self.messageAlreadySendBefore(message.channel, '**Wichtige Informationen** zur **HZP**'):
                await message.channel.send('**Wichtige Informationen** zur **HZP** findest du auch auf unserem Discourse unter: https://talk.wb-student.org/tag/hzp')

        if any(keyWord in message.content.lower() for keyWord in obkKeywords):
            if await self.messageAlreadySendBefore(message.channel, '**Informationen zur OBK**'):
                # Creating embedded message for the new added topic
                embed = discord.Embed(
                    title='Open Book Klausuren',
                    description='- Die Klausuren gehen **90 bis 120 Minuten**\n'
                    '- Für den Verwaltungsaufwand werden **30 Minuten** gewährt\n'
                    '- Gesamtzeit für Klausur: **Klausurzeit + Verwaltungsaufwand**\n'
                    '- Der **Download** wird zum **Start der Klausur** freigeschaltet.\n'
                    '- Es dürfen **keine OBK\'s auf Discord** gepostet werden\n'
                    '\n'
                    'Bitte nehmt an Klausurtagen Rücksicht auf andere und besucht den Onlinecampus nur wenn notwendig',
                    color=discord.Colour.gold(),
                )

                embed.set_author(
                    name="Helferlein",
                    url='',
                    icon_url=''
                )

                embed.add_field(
                    name='Weitere Informationen:',
                    value='- Auf [Discourse](https://talk.wb-student.org/tag/obk) \n- In den [Hochschulnews](https://www.wb-online-campus.de/Neuigkeiten/Free/hochschul-news/index.html)',
                    inline=False
                )

                embed.add_field(
                    name='Klausurpapier',
                    value='Dieses wird vor der Klausur in den News veröffentlicht.',
                    inline=False
                )

                embed.set_footer(text='Information')
                await message.channel.send('**Informationen zur OBK**', embed=embed)

    # checks channels last 25 messages whether the bot already send a messages, starts with <messageStart>, in the last 10 days
    async def messageAlreadySendBefore(self, channel, messageStart):
        async for message in channel.history(limit=25):
            if message.author.bot and message.content.startswith(messageStart) and (datetime.now() - message.created_at).days < 10:
                return False

        return True


def setup(client):
    client.add_cog(Reaction(client))
