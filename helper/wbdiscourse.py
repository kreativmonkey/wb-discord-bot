import discord


class WBDiscourse:

    def __init__(self):
        self.categories = {
            3 : "Teamtalk",
            5 : "Modulthemen",
            7 : "Stammtisch",
            9 : "Erfahrungsbericht",
            10 : "Wissenssammlung", 
            11 : "Tipps und Tricks",
            12 : "WBH-Beschwerden",
        }

        self.colors = {
            3 : discord.Colour.dark_orange(),
            5 : discord.Colour.blue(),
            7 : discord.Colour.green(),
            9 : discord.Colour.blurple(),
            10 : discord.Colour.dark_red(),
            11 : discord.Colour.orange(),
            12 : discord.Colour.darker_gray(),   
        }
        self.prot = "https://"
        self.url = "talk.wb-student.org"


    def getCategorieName(self, catID):
        return self.categories[catID]

    def getCategorieColor(self, catID):
        return self.color[catID]

    def BaseUrl(self):
        return self.prot + self.url