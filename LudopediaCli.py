import Ludopedia
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("--collection", default=None, type=str)
parser.add_argument("--list_url", default=None, type=str)

args = parser.parse_args()

# exemple "https://www.ludopedia.com.br/lista/19726/jogos-que-descobri-no-primeiro-semestre"
def handle_list(url):
    parser = Ludopedia.ListsParser(url)
    parser.fetch_collection()
    for g in parser.collection:
        print(g)


def handle_collections(collection_name):
    parser = Ludopedia.CollectionParser()
    parser.fetch_collection(collection_name, tipo='colecao', tipo_jogo='base')
    collection = list(map(lambda x: (x['title'],x['rating'] if 'rating' in x else "-", x['description'] if 'description' in x else "-"), parser.collection))
    collection = list(map(lambda x: x['rating'] if 'rating' in x else "-", parser.collection))
    for g in collection:
        print(g)

if args.collection is not None:
    handle_collections(args.collection)
if args.list_url is not None:
    handle_list(args.list_url)