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

    def reset_game_buffer(self):
        # g['rating'] = collection.rating[game.bgid].userrating
        # g['name'] = game.name
        # g['owned'] = bool(int(collection.status[game.name].own))
        self.game_buffer = {}

    def handle_starttag(self, tag, attrs):
        self.last_tag.append(tag)
        print ("open tag", tag)

    def handle_endtag(self, tag):
        print ("close tag", tag)
        if len(self.last_tag) > 0 and self.last_tag[-1] == tag:
            self.last_tag.pop()

    def handle_data(self, data):
        if len(self.last_tag) == 0:
            return
        tag = self.last_tag[-1]
        if tag in self.tags_to_ignore:
            return
        if not data.strip() == "":
            print("Encountered {} - {}".format(tag, data))

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
        self.feed(self.fetch_collection_page(user))

parser = Ludopedia()
parser.fetch_collection('scaroni')