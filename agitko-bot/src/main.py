import require
import os, sys, threading, time
from collections import deque
import torch, telebot
from transformers import AutoTokenizer, AutoModelWithLMHead
from utils import apply_half, move_to_cuda

if len(sys.argv)>1:
    token = sys.argv[1]
else:
    token = os.getenv('TG_TOKEN')
    if not token: 
        print('bot token needed...')
        quit()

q = deque()

# turn on cuda if GPU is available
use_cuda = torch.cuda.is_available()
use_fp16 = True and use_cuda #True

model_name = "Nehc/AGIRussia"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelWithLMHead.from_pretrained(model_name)
model.eval()

if use_fp16:
    model.half()
if use_cuda:
    model.cuda()

bot = telebot.TeleBot(token)

print(f'Main cicle whith cuda is {use_cuda} start...')

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Бот обучен на корпусе диалогов из рускоязычных групп тематики AGI (Artificial general intelegense), "
                          "можно говорить с ним на тему ИИ, сознания, мышления и смежные темы.")

@bot.message_handler(commands=['clear'])
def clear_content(message):
    src = 'data/' + str(message.chat.id)
    try:    
        with open(src, 'w') as new_file:
            new_file.write('')
        bot.reply_to(message, "Context reset done...")
    except FileNotFoundError:
        pass    

@bot.message_handler(content_types='text')
def message_reply(message):
    q.append(message)

#bot.polling(interval=3, timeout=45)
#bot.infinity_polling()
if __name__ == '__main__':
    threading.Thread(target=bot.infinity_polling, name='bot_infinity_polling', daemon=True).start()
    while True:
        if q:
            message = q.popleft()
            src = 'data/' + str(message.chat.id)
            try:    
                with open(src, 'r') as cont_file:
                    context = cont_file.read()+'\n'
            except FileNotFoundError:
                context = ''    
    
            text = context+f"<IN>{message.text}\n<OUT>"
            inpt = tokenizer.encode(text, return_tensors="pt")    
            inpt = move_to_cuda(inpt) if use_cuda else inpt
            inpt = apply_half(inpt) if use_fp16 else inpt

            # Run eval step for caption
            with torch.no_grad():
                out = model.generate(inpt, max_length=len(inpt[0])+300, 
                                     do_sample=True, top_k=5, top_p=0.95, 
                                     temperature=1, eos_token_id=50260, 
                                     pad_token_id=50261) #repetition_penalty = 5.0,  typical_p=0.85 - not good... :(
                					
            out_tokens = torch.where(out[0]==50259)
            last_repl = out[0][out_tokens[0][-1]+1:-1]
            repl = tokenizer.decode(last_repl)
            bot.reply_to(message, repl)
            in_tokens = torch.where(out[0]==50258)
            if len(in_tokens[0])<=2 or len(out[0])<=200:
                context = out[0]                        
            else: 
                context = out[0][in_tokens[0][-3]:]

            with open(src, 'w') as new_file:
                new_file.write(tokenizer.decode(context))
        else:
            time.sleep(1)
