### Коллекция разных tg-ботов.
<p align="center">
  <img src="https://github.com/Nehc/botus/assets/8426195/2c1fdad5-954f-431e-922a-c3c345f8c532" alt="AGItco demo" width="200">
</p>

- Telegram-бот [Агитко](https://github.com/Nehc/botus/tree/main/agitko):  Бот на основе GPT2 ([#demo](https://t.me/agitko_bot)), обученный на дискуссиях пула [групп AGIRussia](https://t.me/agirussia). Сам код не особо интересен, ибо простенький (но есть dockerfile 😎), но для начинающих может пригодится [colab](https://colab.research.google.com/github/Nehc/botus/blob/main/agitko/GPT-Chatbot.ipynb) с процедурой обучения. Моделька [доступна](https://huggingface.co/Nehc/AGIRussia) на huggigface. <a target="_blank" href="https://colab.research.google.com/github/Nehc/botus/blob/main/agitko/GPT-Chatbot.ipynb">
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

- Telegram-бот **Visus** (кода пока нет - нужно довести до ума... Есть [#demo](https://t.me/visius_bot)). User-пики всех моих ботов (ну кроме AGItko - он самый древний) сделаны этим ботом. Умеет он две функции: 

  - 📝 Image Captioning | VQA - т.е. кидаете картинку, он говорит что на ней и может ответить на простенькие вопросы (см. Картинку) по последней картинке. В качестве бэкенда еще старая [OFA](https://github.com/Nehc/ofa_telegram) (до апгрейда).  Сейчас уже в значительной степени - прошлый век. Лучше взять [BLIP](https://huggingface.co/Salesforce/blip-vqa-base), [BLIP2](https://huggingface.co/Salesforce/blip2-opt-2.7b), а для совсем отчаянных - [Llava](https://huggingface.co/liuhaotian/llava-v1.5-7b) или [idefics-9b](https://huggingface.co/HuggingFaceM4/idefics-9b)!   

  - 🏞 Если написать ему: "Нарисуй дождь на закате дня" - нарисует! Под капотом Stable Diffusion 1.5 (какая-то слегка потюненая, с https://civitai.com/) в обертке от [AUTOMATIC1111](https://github.com/AUTOMATIC1111/stable-diffusion-webui).
<p align="center">
  <img src="https://github.com/Nehc/botus/assets/8426195/3a63dc86-4253-466d-b91e-e5059ccbac88" alt="AGItco demo" width="800">
</p>

- Бот [Golos](https://github.com/Nehc/botus/tree/main/golos) - для расшифровки голосовых ([#demo](https://t.me/golosisto_bot)). Штука простая, но полезная. Работает на [whisper](https://github.com/openai/whisper) от OpenAI. Так же есть [код бэкенда для него](https://github.com/Nehc/whisper_with_diarisation) на gradio (веб-морда+api) и с [диаризацией](https://ru.wikipedia.org/wiki/%D0%94%D0%B8%D0%B0%D1%80%D0%B8%D0%B7%D0%B0%D1%86%D0%B8%D1%8F)! Вполне годный бейзлайн, который можно поразвивать.
<p align="center">
  <img src="https://github.com/Nehc/botus/assets/8426195/95f8ee7b-0ac8-4539-a0c5-42a115f24a06" alt="AGItco demo" width="400">
</p>

- Еще один интересный бот - **GameMaster**, который я делал - для создания текстово/визуальных новел, как в примере на картинке. Работал на движке ChatGPT (и локально Stable Diffusion, как в Visus для создания иллюстраций), сейчас заглушен, т.к. подписки платной у меня пока нет. Получается совместное творчество человека и нейросети: можно самому задать героя и сеттинг, можно попросить сгенерировать бота. После этого бот задает развитие сюжета, а человек определяет действия героя. Получается забавно. Код весь [выложил](https://github.com/Nehc/GameMaster), если кого заинтересует. 🤭 

<p align="center">
  <img src="https://github.com/Nehc/botus/assets/8426195/e749efbb-60be-49df-82a3-76f7d27beb57" alt="AGItco demo" width="400">
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
