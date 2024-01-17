import require
import os, telebot, redis
from redminelib import Redmine
from telebot import types
#from shortuuid import uuid
from load_conf import config as cf

token = os.getenv('TG_TOKEN')
if not token: 
    print('bot token needed...')
    quit()

rm_key = os.getenv('READMINE_KEY')
if not rm_key: 
    print('redmine key needed...')
    quit()

bot = telebot.TeleBot(token)
rm = Redmine(cf.redmine.url, key=rm_key)

r = redis.Redis(host=cf.redis.host, 
                port=cf.redis.port, 
                decode_responses=True)

def lrm(id):
    return Redmine(cf.redmine.url, 
                   username=r.get(f'helper:{id}:login'), 
                   password=r.get(f'helper:{id}:pass'))


def mainPhaseInlineKeyboard(id, markup=None):
    l_rm = lrm(id)
    iam = l_rm.user.get('current')
    if not markup: markup = types.InlineKeyboardMarkup()
    my_count = len(iam.issues)
    tome_count = len(l_rm.issue.filter(author_id=iam.id))
    if my_count > 0:
        markup.add(types.InlineKeyboardButton(text=f'Задачи мне ({my_count})', callback_data="tome_tasks"))
    if tome_count > 0:
        markup.add(types.InlineKeyboardButton(text=f'Мои задачи ({tome_count})', callback_data="my_tasks"))
    return markup


def task_string(task, cd):
    if cd == "tome_tasks":
        author = str(task.author).replace(" -", "")
        return f"[{str(task.created_on)[:10]}] {author}: '{task.subject}' /t{task.id}\n"
    if cd == "my_tasks":
        assigned_to = "не назначена" if not task.assigned_to else "исполнитель: " + str(task.assigned_to).replace(" -", "")
        return f"[{str(task.created_on)[:10]}] '{task.subject}', {assigned_to} /t{task.id}\n"


task_card = lambda task: (
    f'Задача #{task.id} от {str(task.author).replace(" -", "")} {str(task.created_on)[:10]}\n'
    '---------------------------------\n'
    f'Проект:\t\t{task.project}\nСтатус:\t\t{task.status}\nПриоритет:\t{task.priority}\n'
    f'Исполнитель:\t{"не назначена" if not task.assigned_to else str(task.assigned_to).replace(" -", "")}\n'
    '---------------------------------\n'
    f'<b>{task.subject}</b>: {task.description}\n'
)

# bot.forward_message(to_chat_id, from_chat_id, message_id)
# bot.edit_message_text(chat_id=CHAT_WITH_MESSAGE, text=NEW_TEXT, message_id=MESSAGE_TO_EDIT)

check_list = (
    '<b>Уже реализованные и запланированные фичи:</b>\n'
    '---------------------------------\n'
    '✅ Авторизация (пароль, логин redmine)\t-\tDONE\n'
    '✅ Cписок задач (мои задачи, задачи мне)\t-\tDONE\n'
    '✅ Карточка задачи (из списка, по номеру)\t-\tDONE\n'
    '---------------------------------\n'
    '🛠 Создание новой задачи\t\t-\tIN PROGRESS\n'
    '🛠 Дополнение ранее созданной\t\t-\tIN PROGRESS\n'
    '🛠 Вопрос к специалисту\t\t-\tIN PROGRESS\n'
    '---------------------------------\n'
    '📍 Пометить задачу как исполненную\t-\tPLANED\n'
    '📍 назначить задачу себе (или исполнителю)\t-\tPLANED\n'
)
    
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text='Описание функционала', callback_data="Checklist"))
    if not r.get(f'helper:{message.chat.id}:phase'):
        markup.add(types.InlineKeyboardButton(text='Авторизация', callback_data="autorisation"))
    elif r.get(f'helper:{message.chat.id}:phase')=='main':
        markup = mainPhaseInlineKeyboard(message.chat.id, markup)
    bot.reply_to(message, 'Добро пожаловать в сервисную службу технической поддержки компании Ворлдтех. '
                          'Если вы впервые пользуетесь ботом - нужно авторизоваться.', reply_markup=markup)

@bot.message_handler(commands=['t'])
def send_card(message):
    t_num = message.text.replace('/t','')
    l_rm = lrm(message.chat.id)
    task_descr = task_card(l_rm.issue.get(t_num))
    bot.send_message(message.chat.id, task_descr, parse_mode='HTML')

@bot.message_handler(content_types=['text'])
def send_text(message):
    phase = r.get(f'helper:{message.chat.id}:phase')
    
    if phase == 'login':
        
        bot.delete_message(message.chat.id, message.message_id)
        if len(rm.user.filter(name = message.text))>0:
           r.set(f'helper:{message.chat.id}:login',message.text)
           r.set(f'helper:{message.chat.id}:phase','pass') 
           bot.send_message(message.chat.id, 'Введите свой пароль в сервисной службе:')
        else: 
           bot.send_message(message.chat.id, f'Не найден пользователь с таким именем ({message.text}). ' 
                                              'Попробуйте еще раз, или обратитесь к администратору!')
    elif phase == 'pass':
        
        bot.delete_message(message.chat.id, message.message_id)
        user = r.get(f'helper:{message.chat.id}:login')
        pswd = message.text
        l_rm = Redmine(cf.redmine.url, username=user, password=pswd)
        try:
            if l_rm.user.get('current').id:
                r.set(f'helper:{message.chat.id}:pass',message.text)
                r.set(f'helper:{message.chat.id}:phase','main')
                bot.send_message(message.chat.id, 'Система готова к работе.', 
                                 reply_markup=mainPhaseInlineKeyboard(message.chat.id))                   
        except:
            bot.send_message(message.chat.id, 'Пароль не подходит, Попробуйте еще раз, '
                                             f'или обратитесь к администратору! {user=}, {pswd=}')
            
    elif phase == 'main':
        
        if message.text.startswith('/t'):
            bot.delete_message(message.chat.id, message.message_id)
            t_num = message.text.replace('/t','')
            l_rm = lrm(message.chat.id)
            task_descr = task_card(l_rm.issue.get(t_num))
            bot.send_message(message.chat.id, task_descr, parse_mode='HTML')
        else:
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton(text='Новая задача', callback_data="new_task"))
            markup.add(types.InlineKeyboardButton(text='Добавить к последней', callback_data="add_remark"))
            markup.add(types.InlineKeyboardButton(text='Сообщение', callback_data="message"))
            bot.send_message(message.chat.id, 'Как обработать ваше сообщение?', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def start(call):
    message = call.message
    if call.data == "Checklist":
        bot.send_message(message.chat.id, check_list, parse_mode='HTML')
    elif call.data == "autorisation":
        r.set(f'helper:{message.chat.id}:phase','login')
        bot.send_message(message.chat.id, 'Введите свой логин в сервисной службе:')
    elif call.data == "tome_tasks":
        ans = 'Задачи вам:\n'
        l_rm = lrm(message.chat.id)
        iam = l_rm.user.get('current')
        for t in iam.issues:
            ans+=task_string(t,call.data)
        bot.send_message(message.chat.id, ans)
    elif call.data == "my_tasks":
        ans = 'Ваши задачи:\n'
        l_rm = lrm(message.chat.id)
        iam = l_rm.user.get('current')
        for t in l_rm.issue.filter(author_id=iam.id):
            ans+=task_string(t,call.data)
        bot.send_message(message.chat.id, ans)
    elif call.data == "new_task":
        ...
    elif call.data == "add_remark":
        ...
    elif call.data == "message":
        ...
        

bot.infinity_polling()