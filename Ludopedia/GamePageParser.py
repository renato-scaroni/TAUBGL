from html.parser import HTMLParser
import requests
import re

def extract_text_in_braces(s):
    result = re.search(r"\(([A-Za-z0-9_]+)\)", s)
    if result is not None:
        return result.group(1)
    return "0"

class LudopediaGamePageParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.open_tags = []
        self.tags_to_ignore = set([
            "script",
            "style"
        ])
        self.collection = []
        self.file = open("log", 'w')

    def handle_starttag(self, tag, attrs):
        # print("open tag", tag)
        self.open_tags.append(tag)
        # if tag == "h4":
        #     self.current_game = {}

    def handle_endtag(self, tag):
        # print("close tag", tag)
        if len(self.open_tags) > 0 and self.open_tags[-1] == tag:
            self.open_tags.pop()
        # if tag == "p" and self.current_game is not None:
        #     self.collection.append(self.current_game)
        #     self.current_game = None

    def handle_data(self, data):
        if len(self.open_tags) == 0:
            return
        tag = self.open_tags[-1]
        # if tag in self.tags_to_ignore:
        #     return
        # data = data.strip()
        # print(tag, data, self.current_game == None)
        if "Tive" in data:
            self.current_game["had"] = int(extract_text_in_braces(data))
        if "Tenho" in data:
            self.current_game["has"] = int(extract_text_in_braces(data))
        if tag == "span" and "h3" in self.open_tags:
            self.current_game["release_date"] = int(extract_text_in_braces(data))

    def parse_game_page(self, url):
        # sending get request and saving the response as response object
        self.current_game = {}
        r = requests.get(url = url)
        self.feed(r.text)
        return self.current_game

    # def fetch_collection(self, user, tipo='colecao', tipo_jogo=None):
    #     last_collection_size = -1
    #     page_count = 1
    #     self.collection = []
    #     while not len(self.collection) == last_collection_size:
    #         last_collection_size = len(self.collection)
    #         self.feed(self.fetch_collection_page(user, page_count, tipo=tipo, tipo_jogo=tipo_jogo))
    #         page_count += 1