# SQL Grafana Project

## GIT commit

- git commit -a 
- 'i'
- 'message'
- Esc, :wq
- git push

# TODO
- Find daily/monlty percentage change (maybe do this on python, or in SQL grafana queries)
- Add NFT price data
- NFT rank calculator
- Have docker containers stored on a external volume (once deleted wont lose data)
- 

# Startup
## Docker
- docker start some-postgres grafana (order dependant)
- docker inspect james_network (checks if containers are connetced to network)
- docker stop some-postgres grafana

## Grafana
- http://127.0.0.1:3000/
or
- http://localhost:3000/

## Flask
- Start flask_server.py (run in separate terminal)
- Allows for downloading new cryptos

### SQL Useful Queries
- Gives all table names in the database 
SELECT table_name AS list<br>
FROM information_schema.tables<br>
WHERE table_schema='public'<br>