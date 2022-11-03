import os
import re

def search(name, test):
    search = re.search(name, test)
    if search != None:
        return 1
    else:
        return 0

def docker():
    test = os.popen('docker ps').read()
    found = []
    names = ['grafana', 'some-postgres']

    for name in names:
        found.append(search(name, test))

    if sum(found) == 2:
        print('Stopping docker containers')
        os.system('docker stop some-postgres grafana')
    else:
        print('Starting docker containers')
        os.system('docker start some-postgres grafana')

docker()