from html.parser import HTMLParser
import requests

class Ludopedia(HTMLParser):
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
        if tag == "h4":
            self.current_game = {}

    def handle_endtag(self, tag):
        if len(self.last_tag) > 0 and self.last_tag[-1] == tag:
            self.last_tag.pop()
        if tag == "h4":
            self.collection.append(self.current_game)
            self.current_game = None

    def handle_data(self, data):
        if len(self.last_tag) == 0:
            return
        tag = self.last_tag[-1]
        if tag in self.tags_to_ignore:
            return
        data = data.strip()
        if not data == "" and not self.current_game == None:
            if tag == "a":
                self.current_game["title"] = data
                self.current_game["owned"] = True
            if tag == "span" and len(self.collection) > 0:
                self.current_game["rating"] = data
            if tag == "p" and len(self.collection) > 0:
                self.current_game["description"] = data

    @staticmethod
    def fetch_collection_page(user, pg_number=1):
        # api-endpoint
        URL = "https://ludopedia.com.br/colecao"
        # defining a params dict for the parameters to be sent to the API
        PARAMS = {
            'usuario': user,
            'tipo': 'colecao',
            'tipo_jogo': 'base',
            'pagina': str(pg_number)
        }

        # sending get request and saving the response as response object
        r = requests.get(url = URL, params = PARAMS)

        # extracting data in json format
        return r.text

    def fetch_collection(self, user):
        last_collection_size = -1
        page_count = 1
        while not len(self.collection) == last_collection_size:
            last_collection_size = len(self.collection)
            self.feed(self.fetch_collection_page(user, page_count))
            page_count += 1

parser = Ludopedia()
parser.fetch_collection('scaroni')
for g in parser.collection:
    print(g['title'])