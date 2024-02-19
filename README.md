### Коллекция разных tg-ботов.
<p align="center">
  <img src="https://github.com/Nehc/botus/assets/8426195/2c1fdad5-954f-431e-922a-c3c345f8c532" alt="AGItco demo" width="200">
</p>

- Telegram-бот [Агитко](https://github.com/Nehc/botus/tree/main/agitko-bot):  Бот на основе GPT2 ([#demo](https://t.me/agitko_bot)), обученный на дискуссиях пула [групп AGIRussia](https://t.me/agirussia). Сам код не особо интересен, ибо простенький (но есть dockerfile 😎), но для начинающих может пригодится [colab](https://colab.research.google.com/github/Nehc/botus/blob/main/agitko-bot/GPT-Chatbot.ipynb) с процедурой обучения. Моделька [доступна](https://huggingface.co/Nehc/AGIRussia) на huggigface. <a target="_blank" href="https://colab.research.google.com/github/Nehc/botus/blob/main/agitko-bot/GPT-Chatbot.ipynb">
  <img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/>
</a>
<p align="center">
  <img src="https://github.com/Nehc/botus/assets/8426195/36e14de3-9b62-4923-99b2-52d09d3c78be" alt="AGItco demo" width="400">
</p>

- Telegram-бот [Иоанн Цитатник](https://github.com/Nehc/botus/tree/main/john-preacher): Выдает цитату из библии, подходящую по случаю (косинусная близость). 
Никакой обработки просто поиск поиндексу - только хардкор ([#demo](https://t.me/russian_priest_bot)). 
Под капотом annoy в качестве индекса по Библии (надо заметить книга книг уже разбита на "чанки" и даже проиндексирована 🤔). Индекс можно [скачать](https://huggingface.co/Nehc/rst) отдельно с huggingface. Колаб с индексированием - в комплекте: <a target="_blank" href="https://colab.research.google.com/github/Nehc/botus/blob/main/john-preacher/annoy_rst.ipynb">
  <img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/>
</a>
<p align="center">
  <img src="https://github.com/Nehc/botus/assets/8426195/c4bdb4f2-071f-48bc-8f67-bc77c96ea048" alt="AGItco demo" width="400">
</p>

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
