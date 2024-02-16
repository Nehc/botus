коллекция разных tg-ботов.

`# Что бы клонировать только одного бота...`

```bash
git clone -n --depth=1 --filter=tree:0 https://github.com/Nehc/botus.git
cd botus && git sparse-checkout set --no-cone redmine-bot && git checkout
```

`# Будет скачан тольrо репозиторий бота redmine-bot:`
```
tree /F /a

\---redmine-bot
    |   .dockerignore
    |   .env.example
    |   .gitignore
    |   docker-compose-all.yml
    |   docker-compose.yml
    |   README.md
    |   requirements.txt
    |
    \---src
            config.yaml
            load_conf.py
            main.py
            require.py
            requirements.txt
```
