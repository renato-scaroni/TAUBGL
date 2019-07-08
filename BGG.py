from urllib.error import  URLError
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import ParseError as ETParseError
import urllib.request, urllib.error, urllib.parse
from libBGG.BGGAPI import BGGAPI
import csv
import threading
import time


class BGG(object):
    def _fetch_tree(self, url):
        try:
            tree = ET.parse(urllib.request.urlopen(url))
        except URLError as e:
            print ('error getting URL: %s' % url)
            if hasattr(e, 'reason'):
                print ('We failed to reach a server. Reason: %s' % e.reason)
            elif hasattr(e, 'code'):
                print ('The server couldn\'t fulfill the request. Error code: %d', e.code)
            # raise BGGAPIException(e)
            return None
        except ETParseError as e:
            print('unable to parse BGG response to %s' % url)
            # raise BGGAPIException(e)
            return None

        return tree

    def parseBgInfo(self, root, bgid):
        kwargs = dict()
        kwargs['bgid'] = bgid
        # entries that use attrib['value'].
        value_map = {
            './/yearpublished': 'year',
            './/minplayers': 'minplayers',
            './/maxplayers': 'maxplayers',
            './/playingtime': 'playingtime',
            './/name': 'names',
            ".//link[@type='boardgamefamily']": 'families',
            ".//link[@type='boardgamecategory']": 'categories',
            ".//link[@type='boardgamemechanic']": 'mechanics',
            ".//link[@type='boardgamedesigner']": 'designers',
            ".//link[@type='boardgameartist']": 'artists',
            ".//link[@type='boardgamepublisher']": 'publishers',
            ".//link[@type='boardgamecategory']": 'categories',
            './/averageweight': 'weight'
        }
        for xpath, bg_arg in value_map.items():
            els = root.findall(xpath)
            for el in els:
                if 'value' in el.attrib:
                    if bg_arg in kwargs:
                        # multiple entries, make this arg a list.
                        if type(kwargs[bg_arg]) != list:
                            kwargs[bg_arg] = [kwargs[bg_arg]]
                        kwargs[bg_arg].append(el.attrib['value'])
                    else:
                        kwargs[bg_arg] = el.attrib['value']
                else:
                    print('no "value" found in %s for game %s' % (xpath, name))

        # entries that use text instead of attrib['value']
        value_map = {
            './thumbnail': 'thumbnail',
            './image': 'image',
            './description': 'description'
        }
        for xpath, bg_arg in value_map.items():
            els = root.findall(xpath)
            if els:
                if len(els) > 0:
                    print('Found multiple entries for %s, ignoring all but first' % xpath)
                kwargs[bg_arg] = els[0].text

        return kwargs


    def fetchMultiBoardgameInfo(self, bgids):
        root_url = 'http://www.boardgamegeek.com/xmlapi2/'
        url = '%sthing?id=%s&stats=1' % (root_url, bgids)
        tree = self._fetch_tree(url)
        root = tree.getroot()
        detailedBgInfo = {}
        for child in root:
            if 'type' in child.attrib and child.attrib['type'] == 'boardgame' or child.attrib['type'] == 'boardgameexpansion':
                bgid = child.attrib['id']
                print(bgid)
                detailedBgInfo[bgid] = self.parseBgInfo(child, bgid)

        return detailedBgInfo

    def fetch_collection(self, username):
        api = BGGAPI()
        collection = api.fetch_collection(username, forcefetch=True)

        # properties to be extracted from collection
        cols = [
            #this is retrieved from collection entry 0-7
            'name', 'owned', 'rating', 'bggRank', 'numplays', 'version_nickname', 'bgid', 'thumbnail',
            # this is extended info, string 8-12
            'year', 'image', 'description', 'families',
            # this is extended info int 12-14
            'playingtime', 'minplayers', 'maxplayers',
            # this is extended info, lists 14-19
            'designers', 'mechanics', 'categories', 'publishers'
            # this is extended info, float 19
            'weight'
        ]

        self.d = []
        bgs = [getattr(game, 'bgid', None) for game in collection.games]
        bgids = ','.join(bgs)
        detailedBgInfo = self.fetchMultiBoardgameInfo(bgids)
        for game in collection.games:
            self.loadGameInformation(game, d)

        return d


    def loadGameInformation(self, game, d):
        g = {}
        g['bggRank'] = collection.rating[game.bgid].BGGrank
        g['rating'] = collection.rating[game.bgid].userrating
        g['name'] = game.name
        g['owned'] = bool(int(collection.status[game.name].own))
        g['numplays'] = int(collection.status[game.name].numplays)
        g['version_nickname'] = getattr(game, 'version_nickname', None)
        g['thumbnail'] = getattr(game, 'thumbnail', None)
        g['bgid'] = int(getattr(game, 'bgid', None))
        info = detailedBgInfo[str(g['bgid'])]

        g['weight'] = float(info['weight'])

        for a in cols[8:12]:
            if a in info:
                g[a] = str(info[a])
            else:
                g[a] = " - "

        for a in cols[12:15]:
            if a in info:
                try:
                    g[a] = int(info[a])
                except:
                    g[a] = info[a]
            else:
                g[a] = " - "

        for a in cols[15:19]:
            if a in info:
                if not type(info[a]) is list:
                    g[a] = [info[a]]
                else:
                    g[a] = info[a]
            else:
                g[a] = " - "

        print('%s was created in %s by %s. Categories: %s Mechanics: %s    playingtime: %s weight: %s families: %s'
                % (g['name'], g['year'], g['designers'], g['categories'], g['mechanics'], g['playingtime'], g['weight'], g['families']))

        d.append(g)