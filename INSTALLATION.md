# Installation Guide (*nix)

## DockerHub

Make sure Docker is installed. Then run:
`docker pull karych/postamt`

## Sources

1. Make sure required dependencies are installed: `Docker`, `git`, `make`
2. Clone repository: `git clone https://github.com/realkarych/postamt.git`

## Setting up
4. Create `.env` from template `.env.dist` and provide your creds
5. Create `alembic.ini` from template `alembic.ini.example` and provide db URL
6. You need to initialize web-tunnel for webapps. On dev, you can use ngrok
7. Execute `make debug`
8. Congrats!

More information in <a href="./DOCS.md">DOCS.md</a>
