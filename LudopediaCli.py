import Ludopedia
import argparse
from tabulate import tabulate



# exemple "https://www.ludopedia.com.br/lista/19726/jogos-que-descobri-no-primeiro-semestre"
def handle_list(url):
    parser = Ludopedia.ListsParser(url)
    parser.fetch_collection()
    for g in parser.collection:
        print(g)

def get_collection_line(x):
    line = []
    if not args.no_title:
        line.append(x['title'])
    if args.rating:
        line.append(x['rating'] if 'rating' in x else "-")
    if args.description:
        line.append(x['description'] if 'description' in x else "-")

    return line

def handle_collections(collection_name):
    parser = Ludopedia.CollectionParser()
    parser.fetch_collection(collection_name, tipo='colecao', tipo_jogo='base')

    collection = list(map(get_collection_line, parser.collection))

    headers = []
    if not args.no_title:
        headers.append("title")
    if args.rating:
        headers.append("rating")
    if args.description:
        headers.append("description")

    print(tabulate(collection, headers=headers))

parser = argparse.ArgumentParser()

parser.add_argument("--collection", default=None, type=str)
parser.add_argument("--no_title", action='store_true')
parser.add_argument("-r", "--rating", action='store_true')
parser.add_argument("-d","--description", action='store_true')


parser.add_argument("--list_url", default=None, type=str)

args = parser.parse_args()
if args.collection is not None:
    handle_collections(args.collection)
if args.list_url is not None:
    handle_list(args.list_url)
