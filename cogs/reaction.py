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
                embed = self.createOBKInfoMessage()
                await message.channel.send('**Informationen zur OBK**', embed=embed)

    # checks channels last 25 messages whether the bot already send a messages, starts with <messageStart>, in the last 10 days
    async def messageAlreadySendBefore(self, channel, messageStart):
        async for message in channel.history(limit=25):
            if message.author.bot and message.content.startswith(messageStart) and (datetime.now() - message.created_at).days < 10:
                return False

        return True

    def createOBKInfoMessage(self):
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
            value='Dieses wird vor der Klausur in den News veröffentlicht oder steht [hier](https://www.wb-online-campus.de/infoseiten/public/downloads/Klausurpapier_OBK.pdf) über das WBH-Portal zum Download bereit.',
            inline=False
        )

        embed.add_field(
            name='Klausurpapier (Millimeterpapier)',
            value='[Hier](https://www.wb-online-campus.de/infoseiten/public/downloads/Millimeterpapier_BVTPS_BVTAPS_REAPS.pdf) finden Sie das Klausurpapier für die Prüfungen ''BVTPS'', ''BVTAPS'', ''REAPS''.',
            inline=False
        )

        embed.add_field(
            name='Eidesstattliche Versicherung',
            value='[Hier](https://www.wb-online-campus.de/infoseiten/public/downloads/Eidesstattliche_Versicherung_OBK.pdf) finden Sie das Formular für die eidesstattliche Versicherung im WBH-Portal, welche Sie bei jeder OBK unterschreiben und einreichen müssen.',
            inline=False
        )

        embed.add_field(
            name='Beispiel - ''Vollständige Open Book Klausur'' ',
            value='[Hier](https://www.wb-online-campus.de/infoseiten/public/downloads/BeispielklausurOBK_022021.pdf) finden Sie eine Beispielklausur, wie die PDF-Gesamtdatei aufgebaut sein soll, wenn Sie die OBK bei der WBH hochladen.',
            inline=False
        )

        embed.add_field(
            name='Technische Details - OBK'' ',
            value='[Hier](https://www.wb-online-campus.de/infoseiten/public/downloads/Technische_Details_OBK_06042021.pdf) finden Sie technische Details über die OBK am Klausurtag.',
            inline=False
        )

        embed.add_field(
            name='FAQ',
            value='[Hier](https://www.wb-online-campus.de/infoseiten/public/downloads/FAQ_Open-Book-Klausuren_19_03_2021.pdf) finden Sie alle Fragen & Antworten zu den OBK''s im WBH-Portal.',
            inline=False
        )

        embed.set_footer(text='Information')
        return embed


def setup(client):
    client.add_cog(Reaction(client))
