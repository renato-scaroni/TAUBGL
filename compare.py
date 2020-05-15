import pandas as pd
from Ludopedia import Ludopedia

file_path = "notas.csv"
df = pd.read_csv(file_path)
games_in_notas=set(df["jogo"].head(108).tolist())
parser = Ludopedia()
parser.fetch_collection('scaroni')
diff = []
for g in parser.collection:
    if not g['title'] in games_in_notas:
        diff.append(g['title'])
print (diff)