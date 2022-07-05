import urllib.parse
class DAPI:
    def __init__(self):
        self.version = 10
        self.base_url = "https://discord.com/api/"

    def url_for(self, rest):
        urllib.parse.urljoin(f"{self.base_url}v{self.version}", rest)
