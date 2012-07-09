import os

from monkeyladder.settings.development import DATABASES

def kill():
    for name, database in DATABASES.items():
        database_file = database['NAME']
        if not database_file.endswith('monkeyladder.db'):
            print "Bad File: {}".format(database_file)
            continue
        if not os.path.exists(database_file):
            print "Target database does not exist: {}".format(database_file)
            continue
        print "Killing database: {}".format(database_file)
        os.remove(database_file)
    
if __name__ == '__main__':
    kill()