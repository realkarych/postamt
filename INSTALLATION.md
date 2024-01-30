# Installation Guide (*nix)

1. Make sure that git, Python, Postgres, Docker, Poetry are installed on your machine.
2. Clone repository: `git clone https://github.com/realkarych/postamt.git`
3. Run `poetry install && poetry update` to install project dependencies.
4. Create `app.ini` configuration file and put your credentials. We provided template `app.ini.example` for you.
5. Setup database:
    - PSQL: `CREATE DATABASE postamt;`
    - Initialize alembic migrations: `alembic init --template async migrations`
    - Open alembic.ini -> `sqlalchemy.url = postgresql+asyncpg://user:pass@localhost/postamt`
    - `alembic revision --autogenerate -m "init"`
    - `alembic upgrade head`
6. Configure RabbitMQ [Will be able later]
7. Run Docker container [Will be able later]
