# Installation
1. Install frontend:
    - `cd frontend`
    - `yarn install`
2. Generate the secrets directory:
    - `./secrets`
3. Generate the secrets files:
    - `./secrets/google_search_token` with a single line of content `efgh` for example
    - `./secrets/postgres_password` with a single line of content `1234` for example
    - `./secrets/postgres_user` with a single line of content `abcd` for example
4. Docker compose up
    - `docker-compose up`
5. Visit `http://localhost:3000/gallery`

# Testing
1. Unsure... need to figure out again and write down the directions


# The Stack
## Databases
1. Postgres (host: postgres, port: 5432)
2. MongoDB (host: mongo, port 27017)

## DB Admins
1. PGAdmin (port: 5431)
2. Mongo-Express (port: 27016)

## Frontend
1. NextJS

## Backend
1. Currently Python
