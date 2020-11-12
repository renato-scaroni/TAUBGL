from html.parser import HTMLParser
import requests

class LudopediaCollectionParser(HTMLParser):
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
        # print("open tag", tag)
        self.last_tag.append(tag)
        if tag == "h4":
            self.current_game = {}

    def handle_endtag(self, tag):
        # print("close tag", tag)
        if len(self.last_tag) > 0 and self.last_tag[-1] == tag:
            self.last_tag.pop()
        if tag == "p" and self.current_game is not None:
            self.collection.append(self.current_game)
            self.current_game = None

    def handle_data(self, data):
        if len(self.last_tag) == 0:
            return
        tag = self.last_tag[-1]
        if tag in self.tags_to_ignore:
            return
        data = data.strip()
        # print(tag, data, self.current_game == None)
        if not data == "" and not self.current_game == None:
            if tag == "a":
                self.current_game["title"] = data
                self.current_game["owned"] = True
            if tag == "span" and len(self.collection) > 0:
                self.current_game["rating"] = data
            if tag == "p" and len(self.collection) > 0:
                self.current_game["description"] = data

    @staticmethod
    def fetch_collection_page(user, pg_number=1, tipo='colecao', tipo_jogo=None):
        URL = "https://ludopedia.com.br/colecao"
        PARAMS = {
            'usuario': user,
            'tipo': tipo,
            'pagina': str(pg_number)
        }

        if tipo_jogo is not None:
            PARAMS['tipo_jogo'] = tipo_jogo

        # sending get request and saving the response as response object
        r = requests.get(url = URL, params = PARAMS)

        return r.text

    def fetch_collection(self, user, tipo='colecao', tipo_jogo=None):
        last_collection_size = -1
        page_count = 1
        self.collection = []
        while not len(self.collection) == last_collection_size:
            last_collection_size = len(self.collection)
            self.feed(self.fetch_collection_page(user, page_count, tipo=tipo, tipo_jogo=tipo_jogo))
            page_count += 1