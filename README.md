### Коллекция разных tg-ботов.

- Telegram-бот [Агитко](https://github.com/Nehc/botus/tree/main/agitko-bot):  Бот на основе GPT2 ([#demo](https://t.me/agitko_bot)), обученный на дискуссиях пула [групп AGIRussia](https://t.me/agirussia). Сам код не особо интересен, ибо простенький (но есть dockerfile 😎), но для начинающих может пригодится [colab](https://colab.research.google.com/github/Nehc/botus/blob/main/agitko-bot/GPT-Chatbot.ipynb) с процедурой обучения. Моделька [доступна](https://huggingface.co/Nehc/AGIRussia) на huggigface. <a target="_blank" href="https://colab.research.google.com/github/Nehc/botus/blob/main/agitko-bot/GPT-Chatbot.ipynb">
  <img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/>
</a>

- Telegram-бот [Иоанн Цитатник](https://github.com/Nehc/botus/tree/main/john-preacher): Выдает цитату из библии, подходящую по случаю (косинусная близость). 
Никакой обработки просто поиск поиндексу - только хардкор ([#demo](https://t.me/russian_priest_bot)). 
Под капотом annoy в качестве индекса по Библии (надо заметить книга книг уже разбита на "чанки" и даже проиндексирована 🤔). Индекс можно [скачать](https://huggingface.co/Nehc/rst) отдельно с huggingface.

#### Что бы клонировать только одного бота...

```
git clone -n --depth=1 --filter=tree:0 https://github.com/Nehc/botus.git
cd botus && git sparse-checkout set --no-cone redmine-bot && git checkout
```

Будет скачан репозиторий бота redmine-bot:
```
tree /F /a
```
```
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
