import require
import os, sys, random, threading, time
import pandas, telebot, torch
from torch import Tensor
from collections import deque
from transformers import AutoTokenizer, AutoModel
from annoy import AnnoyIndex 
import torch.nn.functional as F

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

#print(f'Start with cuda is {use_cuda} and fp16 (half) is {use_fp16}.')

#model_name = "sberbank-ai/sbert_large_mt_nlu_ru"
model_name = "intfloat/multilingual-e5-large"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)
model.eval()

if use_cuda:
    model.cuda()
if use_fp16:
    model.half()

if not os.path.exists('rst/rst.indx'):
    from git import Repo
    Repo.clone_from('https://huggingface.co/Nehc/rst',to_path='rst')  
      
rst_ind = AnnoyIndex(1024, metric='angular')
rst_ind.load('rst/rst.indx')
rst_df = pandas.read_csv('rst/rst_db.csv')

bot = telebot.TeleBot(token)

print(f'Main cicle whith cuda is {use_cuda} start...')

#Mean Pooling - Take attention mask into account for correct averaging
def mean_pooling(model_output, attention_mask):
    token_embeddings = model_output[0] #First element of model_output contains all token embeddings
    input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    sum_embeddings = torch.sum(token_embeddings * input_mask_expanded, 1)
    sum_mask = torch.clamp(input_mask_expanded.sum(1), min=1e-9)
    return sum_embeddings / sum_mask

def average_pool(last_hidden_states: Tensor,
                 attention_mask: Tensor) -> Tensor:
    last_hidden = last_hidden_states.masked_fill(~attention_mask[..., None].bool(), 0.0)
    return last_hidden.sum(dim=1) / attention_mask.sum(dim=1)[..., None]

def citate(sentence, count=5):
    indices = rst_ind.get_nns_by_vector(sentence, count)
    ind = random.choice(indices)
    str_ = rst_df.loc[ind].Text
    print(f"{str_} [{rst_df.loc[ind]['Book']}{rst_df.loc[ind]['Chapter']}:{rst_df.loc[ind]['Verse']}]")
    f_ind = ind 
    words = rst_df.loc[f_ind].Text.split()
    if words[0][0]=='(' and words[0][-1]==')':
        str_ = str_.replace(words[0]+' ','')
    while (not words[0].istitle()
            and not (words[1].istitle() and words[0][0]=='(' and words[0][-1]==')')):
        f_ind-=1
        str_ = rst_df.loc[f_ind].Text+' '+str_
        words = rst_df.loc[f_ind].Text.split()             
        if words[0][0]=='(' and words[0][-1]==')':
            str_ = str_.replace(words[0]+' ','')
    l_ind = ind
    while rst_df.loc[l_ind].Text.find('.')<0:
        l_ind+=1
        str_ +=' '+rst_df.loc[l_ind].Text
        words = rst_df.loc[l_ind].Text.split()             
        if words[0][0]=='(' and words[0][-1]==')':
            str_ = str_.replace(words[0]+' ','')

    book = rst_df.loc[f_ind]['Book']
    chap = rst_df.loc[f_ind]['Chapter']
    if f_ind==l_ind:
        vers = rst_df.loc[f_ind]['Verse']
    else:
        vers = (str(rst_df.loc[f_ind]['Verse'])+
                '-'+str(rst_df.loc[l_ind]['Verse']))
    return str_+f" [{book}{chap}:{vers}]"

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Данный бот подбирает соответствующую случаю цитату из библии. "
              "Вы прост опишите ему (коротко) вашу жизненную ситацию, и получаете подходящий ответ.")

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
            txt = message.text
            if txt[-1]=='?':
                txt = 'query: ' + txt[:-1]
            else:    
                txt = 'passage: ' + txt[:-1]
            inpt = [txt]
            inpt = tokenizer(inpt, return_tensors='pt')
            if use_cuda:
                inpt = inpt.to(torch.cuda.current_device())
            # Run eval step for caption
            with torch.no_grad():
                out = model(**inpt)		
            #sentence_embeddings = mean_pooling(out, inpt['attention_mask'])
            embeddings = average_pool(out.last_hidden_state, inpt['attention_mask'])
            embeddings = F.normalize(embeddings, p=2, dim=1)	
            repl = citate(embeddings[0])
            bot.reply_to(message, repl)
        else:
            time.sleep(1)
