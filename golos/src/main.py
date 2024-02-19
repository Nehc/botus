import require
import time, os, threading, telebot
from collections import deque
from gradio_client import Client
from load_conf import config as cf

q = deque()
print('inits OK...')

#if len(sys.argv)>1:
#    token = sys.argv[1]
#else:
token = os.getenv('TG_TOKEN')
if not token: 
    print('bot token needed...')
    quit()

#print(token)

def extract_arg(arg):
    return arg.split()[1:]

print('def loaded...')

bot = telebot.TeleBot(token)
client = Client(cf.whisper)

print(f'Main cicle is start...')

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "hello...")

@bot.message_handler(commands=['f2me','f2txt','cmd','lf2txt'])
def file_mess_deque(message):
    q.append(message)

@bot.message_handler(content_types=['voice'])
def message_deque(message):
    q.append(message)

#bot.polling(interval=3, timeout=45)
#bot.infinity_polling()
if __name__ == '__main__':
    threading.Thread(target=bot.infinity_polling, name='bot_infinity_polling', daemon=True).start()
    while True:
        if q:
            message = q.popleft()
            lang, tr_lang = None, None
            if message.text =='/f2me' or message.text =='/f2txt' :
                if message.reply_to_message and message.reply_to_message.content_type == 'audio':
                    file_info = bot.get_file(message.reply_to_message.audio.file_id)
                else:
                    bot.reply_to(message,'This command mast be a reply to audio...')
                    continue
                if message.text =='/f2txt':
                    bot.reply_to(message, 'Пакуем результат в файл, ожидайте...')     
                downloaded_file = bot.download_file(file_info.file_path)
                f_name = 'audio.'+file_info.file_path.split('.')[-1]
                with open(f_name, 'wb') as new_file:
                    new_file.write(downloaded_file)
            elif message.text =='/lf2txt' :
                bot.reply_to(message, 'Пакуем результат в файл, ожидайте...')     
                f_name = 'audio.mp3'
            elif message.text and message.text[:4] =='/cmd' :                        
                args = extract_arg(message.text)
                args = dict(a.split('=') for a in args)
                lang = args.get('lang')
                tr_lang = args.get('trto')
                if message.reply_to_message and message.reply_to_message.content_type == 'voice':
                    file_info = bot.get_file(message.reply_to_message.voice.file_id)
                    downloaded_file = bot.download_file(file_info.file_path)
                    f_name = 'audio.ogg'
                    with open(f_name, 'wb') as new_file:
                        new_file.write(downloaded_file)
            else:    
                file_info = bot.get_file(message.voice.file_id)
                downloaded_file = bot.download_file(file_info.file_path)
                f_name = 'audio.ogg'
                with open(f_name, 'wb') as new_file:
                    new_file.write(downloaded_file)

            result = client.predict(f_name, lang, tr_lang, api_name="/get_text")

            if message.text =='/f2txt' or message.text =='/lf2txt':
                with open('result.txt', 'w') as new_file:
                    new_file.write(result)
                with open('result.txt', 'rb') as doc:
                    bot.send_document(message.chat.id, doc) 
            else:
                if len(result) > 4096:
                    msgs = [result[i:i + 4096] for i in range(0, len(result), 4096)]
                    for text in msgs:
                        bot.reply_to(message, text, parse_mode="HTML")    
                else:
                    bot.reply_to(message, result, parse_mode="HTML")
        else:
            time.sleep(1)
