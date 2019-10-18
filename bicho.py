# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests 
import telepot
URL = "https://www.resultadosdobichotemporeal.com.br/search/label/AVAL%20ONLINE%20ALIAN%C3%87A"
r = requests.get(URL) 

print(r.status_code)

TelegramBot = telepot.Bot('951983791:AAH5fYW1KmTAOMD1bAult-3SQo17NBrLO_Y')

with open("update_id.txt", "r") as f:
    ult_updt = f.read()
    if ult_updt is None or ult_updt == "":
        ult_updt = 0
        updates = TelegramBot.getUpdates()
    else:
        updates = TelegramBot.getUpdates(int(ult_updt)+1)

for upd in updates:
    # chat_id = updt['message']['chat_id']
    chat_id = upd.get("message").get("chat").get("id")
    message = upd.get("message").get("text")
    update_id = upd.get("update_id")
    print update_id
    if message == "/start":
        with open("chat_id.txt","r") as f:
            linhas = f.readlines()
            encontrado = False
            for i in linhas:
                if i.replace("\n","") == str(chat_id):
                    encontrado = True
            
            if not encontrado:
                with open("chat_id.txt","a") as i:
                    i.write(str(chat_id)+"\n")
                    TelegramBot.sendMessage(chat_id, "Bem vindo ao Bot de Alertas!", parse_mode='HTML')
    elif message == "/help":
        TelegramBot.sendMessage(chat_id, "Qualquer duvida enviar um email a <strong>luizchaos@gmail.com!</strong>", parse_mode='HTML')
    
    with open("update_id.txt", "w") as l:
        l.write(str(update_id))

if r.status_code == 200:
    soup = BeautifulSoup(r.content, 'html5lib') 
    posts = soup.find('div', attrs = {'class':'date-posts'})

    for row in posts.findAll('div', attrs = {'class':'post-outer'}):
        artigo = row.find('article')
        titulo = artigo.find('h2')
        link = titulo.find('a')
        nome = link['title']

        bicho_atual = ''        

        with open("ultimo_bicho.txt", "r") as l:
            bicho_atual = l.read()

        if nome.encode('utf-8').strip() != bicho_atual:
            href = link['href']

            with open("ultimo_bicho.txt", "w") as l:
                l.write(nome.encode('utf-8').strip())

            nr = requests.get(href)
            
            if nr.status_code == 200:
                nsoup = BeautifulSoup(nr.content, 'html5lib') 

                corpo = nsoup.find('div', attrs = {'class':'post-body'})

                res = corpo.find('div', attrs = {'itemprop':'description'})

                print(res)
                
                with open("chat_id.txt","r") as s:
                    lin = s.readlines()
                    for i in lin:
                        TelegramBot.sendMessage(int(i), res.text, parse_mode='HTML')

        break
else:
    print('Tente Novamente')