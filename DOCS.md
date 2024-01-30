## Locales
We use Babel for localization. So here are the most common commands that you have to use:

- **Extract texts:** `pybabel extract --input-dirs=. -o locales/bot.pot`
- **Initialize Babel with default language:** `pybabel init -i locales/bot.pot -d locales -D bot -l en`
- **Add new language:** `pybabel init -i locales/bot.pot -d locales -D bot -l ru`
- **Update locales after changes:** `pybabel update -d locales -D bot -i locales/bot.pot`
- **Compile locales:** `pybabel compile -d locales -D bot`

Our advise: managing locales is a very tedious and inconvenient process, so we use https://poedit.net/ to create translations faster.
