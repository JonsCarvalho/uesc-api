#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

@app.route('/news/', methods=['GET'])
def respond():
    # Coletar e analisar a primeira pagina
    page = requests.get(
        "http://www.uesc.br/noticias/index.php").content

    # Criar o objeto BeautifulSoup
    soup = BeautifulSoup(page, 'html.parser')

    # Remover links inferiores
    last_links = soup.find(class_='fooRow')
    last_links.decompose()

    # Pegar todo o texto da table tabela_noticias
    news_list = soup.find(id='tabela_noticias')

    # Pegar a data de todas as instancias da classe coluna_data_noticia dentro da classe tabela
    news_date_list = news_list.find_all(class_='coluna_data_noticia')

    # Pegar o conteudo de todas as tags <a> da table tabela_noticias
    news_content_list = news_list.find_all('a')[2:]

    # Pegar a descricao de todas as noticias
    news_description_list = news_list.find_all('tr')[1:]

    news = []
    for index in range(len(news_content_list)):
        instance = {}

        date = news_date_list[index].text
        date = date.replace('\n', '')
        date = date.replace('\t', '')

        title = news_content_list[index].text

        description = news_description_list[index].contents[3].contents[1]
        description = description.replace('\n', '')
        description = description.replace('\t', '')

        link = 'http://www.uesc.br/noticias/index.php' + \
            news_content_list[index].get('href')

        instance['date'] = date
        instance['title'] = title
        instance['description'] = description
        instance['link'] = link
        news.append(instance)

    return jsonify(news)    
    # # Retrieve the name from url parameter
    # name = request.args.get("name", None)

    # # For debugging
    # print(f"got name {name}")

    # response = {}

    # # Check if user sent a name at all
    # if not name:
    #     response["ERROR"] = "no name found, please send a name."
    # # Check if the user entered a number not a name
    # elif str(name).isdigit():
    #     response["ERROR"] = "name can't be numeric."
    # # Now the user entered a valid name
    # else:
    #     response["MESSAGE"] = f"Welcome {name} to our awesome platform!!"

    # # Return the response in json format
    # return jsonify(response)

@app.route('/post/', methods=['POST'])
def post_something():
    param = request.form.get('name')
    print(param)
    # You can add the test cases you made in the previous function, but in our case here you are just testing the POST functionality
    if param:
        return jsonify({
            "Message": f"Welcome {name} to our awesome platform!!",
            # Add this option to distinct the POST request
            "METHOD" : "POST"
        })
    else:
        return jsonify({
            "ERROR": "no name found, please send a name."
        })

# A welcome message to test our server
@app.route('/')
def index():
    return "<h1>Bem vindo! Esta é a API de notícias da UESC</h1>"

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.config['JSON_AS_ASCII'] = False
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)