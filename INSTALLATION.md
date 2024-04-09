# Installation Guide (*nix)

## DockerHub

Make sure Docker is installed. Then run:
`docker pull karych/postamt`

## Sources

1. Make sure required dependencies are installed: `Docker`, `git`, `make`
2. Clone repository: `git clone https://github.com/realkarych/postamt.git`
3. Create `.env` from template `.env.dist` and provide your creds
4. Create `alembic.ini` from template `alembic.ini.example` and provide db URL
5. Execute `make debug`
6. Congrats!

More information in <a href="./DOCS.md">DOCS.md</a>
