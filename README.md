<a href="https://t.me/postamt_robot">
<p align="center" width="100%">
    <img width="25%" src="https://github.com/realkarych/postamt/assets/62261985/b7545d92-6f06-4410-9873-8b52267216d0">
</p>
</a>

*<p align=center>POSTAMT [on russian — Почтамт] is a Telegram ChatBot that replaces mobile and desktop Email clients in 99% of daily task cases</p>*

<hr>

## 👋 Say hello to POSTAMT

- **Web3 url:** https://postamt_robot.t.me
- **Classic url:** https://t.me/postamt_robot
- **In Telegram:** @postamt_robot

## 🚀 Features

- **Email Management:** Perform various actions on your emails, such as reading, replying, sending, attaching files, and more.

- **Power of Threads:** Your emails are filtered by email addresses in a single Telegram supergroup. Telegram Threads technology allows us to organize the user experience similarly to native email clients (like Gmail, Outlook, etc.).

- **Multi-Account Support:** Connect and manage multiple email accounts within a single interface.

- **Security:** POSTAMT never requests two-factor authentication and does not have access to the danger zone of your Email account. It does not delete emails, manage passwords and personal data. Connection is made via auto-generated IMAP/SMTP access keys. Your emails are not saved or cached anywhere after having read (even on the Telegram servers)

## ❞ Why named POSTAMT?

This project is named in honor of the St. Petersburg Main Post Office [Главпочтамт / Glavpochtamt], a monument of Russian history and culture.

"Postamt" is a German word that translates to "post office" in English. It refers to a facility or building where postal services are provided. Post offices are responsible for handling mail and packages, selling postage stamps, offering various postal services, and providing a range of other services related to mail delivery and communication. Postamt plays a crucial role in the postal system, facilitating the sending and receiving of mail and packages within a region or country.

Our POSTAMT semantically resembles a post office.

## 📊 Roadmap [to the first beta]

- [x] **Scope:** Define project scope and objectives
- [x] **Architecture:** Set up basic project structure
- [x] **Docker:** Set up docker to simplify development & delivery
- [x] **Cryptography:** Set up cryptography infrastructure to encrypt and decrypt secret data
- [x] **Core service:** Implement IMAP-service
- [x] **Migrations:** Setup migrations (alembic)
- [x] **Database:** Implement data schemas and repositories
- [ ] **Telegram "UI" stage 1:** Implement base functionality with registration, adding Email account, group setup
- [ ] **Message broker (Kafka):** Setup Kafka as a single interface to send emails, answers messages
- [ ] **Telegram "UI" stage 2:** Implement Telegram WebViews to check emails
- [ ] **GPT Model:** Integrate GPT API as a emails' summary executor. Candidates: OpenAI, LLaMa
- [ ] **Flood controller:** Set up anti-spam system (on middlewares layer)
- [ ] **Core service:** Implement SMTP-service
- [ ] **Telegram "UI" stage 3:** Implement UI to send emails
- [ ] **Channel subscription:** To use bot, user need to be subscribed to https://t.me/postamt_channel (create filter)
- [ ] **Grafana:** Add [Grafana](https://grafana.com/) dashboard to check statistics

## 🖥️ Installation

We acknowledge your desire for full control over your data. Therefore, all source codes for the project are open, allowing you to host the project locally on your own.

To launch project locally:

- Check our Docs: <a href="./DOCS.md">DOCS.md</a>
- Follow the Guideline: <a href="./INSTALLATION.md">INSTALLATION.md</a>

## 🙏 Contributing

We welcome contributions from developers and non-developers alike! If you're a developer, you can make a direct impact by contributing code. Clone the repository, make your changes, and submit a pull request.

Not a developer? No problem! You can still contribute by creating issues, reporting bugs, or suggesting new ideas for project improvement (do this via GitHub Issues). Your insights and feedback are invaluable to our collective success and helps us to create the best non-native Email client.

Thank you for your contribution and support to the project!
