import urllib.parse
class BAPI:
    def __init__(self):
        self.base_url = "https://direct.projects.iotaspencer.me:5000/sendto/"
        self.bot_name = None

    def url_for(self, bot_name):
        self.bot_name = bot_name
        if self.bot_name is not None:
            urllib.parse.urljoin(f"{self.base_url}", f"{self.bot_name}")
        else:
            raise ArgumentError("Bot name is not specified")

bapi = BAPI()
def get_bot_url(bot_name):
    bapi.url_for(bot_name)