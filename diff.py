from sys import argv, exit

if len(argv) < 3:
    print("need 2 files")
    exit(-1)

f1 = open(argv[1])
f2 = open(argv[2])

set1 = set()
for l in f1.readlines():
    set1.add(l)

set2 = set()
for l in f2.readlines():
    set2.add(l)

for l in list(set.difference(set1, set2)):
    print(l[:-1])