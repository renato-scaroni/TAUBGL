from html.parser import HTMLParser
import requests

class LudopediaPublicListsParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.last_tag = []
        self.tags_to_ignore = set([
            "script",
            "style"
        ])
        self.collection = []
        self.file = open("log", 'w')
        self.current_game = None

    def handle_starttag(self, tag, attrs):
        self.last_tag.append(tag)

    def handle_endtag(self, tag):
        if len(self.last_tag) > 0 and self.last_tag[-1] == tag:
            self.last_tag.pop()

    def handle_data(self, data):
        if len(self.last_tag) == 0:
            return
        tag = self.last_tag[-1]
        if tag in self.tags_to_ignore:
            return
        data = data.strip()
        if(self.last_tag[-1] == "h3"):
            self.collection.append("".join(data.split('-')[-1]).strip())

    @staticmethod
    def fetch_collection_page(url, pg_number=1, tipo='colecao'):
        PARAMS = {
            'pagina': str(pg_number)
        }

        # sending get request and saving the response as response object
        r = requests.get(url = url, params = PARAMS)
        return r.text

    def fetch_collection(self, url):
        last_collection_size = 1
        page_count = 1
        self.collection = []
        self.feed(self.fetch_collection_page(url, page_count))

