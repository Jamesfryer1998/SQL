import os
import re

def search(name, test):
    return re.search(name, test) is not None

def docker():
    test = os.popen('docker ps').read()
    names = ['grafana', 'some-postgres']
    running = [search(name, test) for name in names]

    if all(running):
        print('Stopping docker containers...')
        os.system('docker stop some-postgres grafana')
        print('Containers stopped.')
    else:
        print('Starting docker containers...')
        os.system('docker start some-postgres grafana')
        print('Containers started.')
        
docker()