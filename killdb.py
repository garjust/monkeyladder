import os

from monkeyladder.development import DATABASES

for name, database in DATABASES.items():
    database_file = database['NAME']
    if not database_file.endswith('monkeyladder.db'):
        print "bad file"
        continue
    if not os.path.exists(database_file):
        print "db dne"
        continue
    print "Killing database: {}".format(database_file)
    os.remove(database_file)