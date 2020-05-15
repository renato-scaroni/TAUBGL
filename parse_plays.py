import json

with open('plays_2019_2.json', 'r') as file:
    data = json.load(file)
    games = {}

    for game in data['games']:
        games[game['id']] = game

    first_played = []
    first_played_names = []
    ids = []
    for play in data['plays']:
        for score in play['playerScores']:
            if score['playerRefId'] == 1 and score['newPlayer']:
                first_played.append(play)
                ids.append(play['gameRefId'])
                first_played_names.append(games[ids[-1]]['name'])

    for name in first_played_names:
        print(name)