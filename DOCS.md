## Locales
We use Babel for localization. So here are the most common commands that you have to use:

- **Extract texts:** `pybabel extract --input-dirs=. -o locales/bot.pot`
- **Initialize Babel with default language:** `pybabel init -i locales/bot.pot -d locales -D bot -l en`
- **Add new language:** `pybabel init -i locales/bot.pot -d locales -D bot -l ru`
- **Update locales after changes:** `pybabel update -d locales -D bot -i locales/bot.pot`
- **Compile locales:** `pybabel compile -d locales -D bot`

Our advise: managing locales is a very tedious and inconvenient process, so we use https://poedit.net/ to create translations faster.

## Run, Test & Deployment
We use Docker and docker-compose to organize testing and deploying environments. Project runs in two Docker containers:

1) Bot
2) PostgreSQL

**Launch app in Debug mode (with stacktrace):** `make debug`
**Launch app in Production mode:** `make run`

**Check Makefile:** we provided the more useful commands to console cli. Run `make help` to check them out.

## How to create postgres dump?
For security reasons, we have disabled the ability to connect to the base outside of the server.

To open PSQL, execute: `psql -h localhost -p 5432 -U <username> postamt`. Then you can create dump as usual.
