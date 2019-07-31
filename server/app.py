import uuid
import jsonpickle
import pickle
import os
import errno

from flask import Flask, jsonify, request
from flask_cors import CORS

# Biblioteca de Linguagem Natural
import nltk
nltk.download('punkt')
from nltk.tokenize import word_tokenize
from nltk.classify import NaiveBayesClassifier

#Banco de Dados
from pymongo import MongoClient
#clienteMongo = MongoClient('192.168.82.118', 27017,username='root', password='root')
clienteMongo = MongoClient('localhost', 27017)
banco = clienteMongo.igti

import json
from bson import json_util, ObjectId


#twitter
import tweepy
CONSUMER_API_KEY = "PMrkmRMQy3n7yZnBcY4GYihM6"
CONSUMER_API_SECRET = "f3e9oFfDfw3MA8ZmrV6QbeSthUDO8UTdb3TFrOsdkGmWRmmzCx"
ACCESS_TOKEN = "92998645-EphmhVfonqO2YbXtBmRIcgZSpA6aoGt6nNPD8JAI9"
ACCESS_TOKEN_SECRET = "0MbzoFCMq4LrGcya8ro2XMrjBifteujAa3NnVsgepHDG4"

auth = tweepy.AppAuthHandler(CONSUMER_API_KEY, CONSUMER_API_SECRET)
api = tweepy.API(auth)

# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})


def formatar_sentenca(sentenca):
   return {palavra: True for palavra in word_tokenize(sentenca)}

# sanity check route
@app.route('/dashboard', methods=['GET'])
def dashboard():
    response_object = {'status': 'success'}
    if request.method == 'GET':

        tweets_positivos = banco.positivos.find()
        tweets_negativos = banco.negativos.find()
        tweets_novos = banco.novos.find()
        tweets_estatisticas = banco.estatisticas.find()


        response_object['data'] = { 
                                    'tweets_positivos': json_util.dumps(tweets_positivos),
                                    'tweets_negativos': json_util.dumps(tweets_negativos),
                                    'tweets_novos': json_util.dumps(tweets_novos),
                                    'tweets_estatisticas': json_util.dumps(tweets_estatisticas),
                                  }
        

    return jsonify(response_object)


# sanity check route
@app.route('/coleta', methods=['POST'])
def coleta():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        title = post_data.get('title')

        consulta = 'place:1b107df3ccc0aaa1 "' + title + '" '
        numMaxTweets = 10
        tweets_buscados = []
        for tweet in tweepy.Cursor(api.search, q=consulta).items(numMaxTweets):
            # tweets.insert({ 'name': title , 'sentimento':'','avaliacao':'', 'tweet': tweet._json })
            tweets_buscados.append({'title': title, 'sentimento': '', 'avaliacao': '',
                                    'tweet': tweet._json})

        response_object['message'] = 'Retornados ' + str(numMaxTweets) + ' tweets '
        response_object['data'] = tweets_buscados


    return jsonify(response_object)

@app.route('/respostas', methods=['POST'])
def respostas():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        
        tweets = post_data.get('tweets')
        title = post_data.get('title')

        # COLECTIONS MONGODB
        tweets_positivos = banco.positivos
        tweets_negativos = banco.negativos
        #tweets_modelo = banco.modelo
        
        positivos = []
        negativos = []
        for tweet in tweets:
            #print (texto.encode('utf8').lower())
            if tweet['sentimento'] == "N":
                negativos.append(tweet)

            if tweet['sentimento'] == "P":
                positivos.append(tweet)
            
        if len(positivos)>0:
             tweets_positivos.insert_many(positivos)
        if len(negativos)>0:
            tweets_negativos.insert_many(negativos)
        
        response_object['message'] = 'Tweets armazenados no banco de dados'
        response_object['title'] = title
        
     
    return jsonify(response_object)

@app.route('/novostweets', methods=['POST'])
def analisar():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        positivos = []
        negativos = []
        dados_treinamento = []
        qtd = post_data.get('qtd')
        title = post_data.get('title')

        #pesquisa os negativos e positivos para criar um modelo
        tweets_positivos = banco.positivos.find({'title':title})
        #tweets_positivos = banco.positivos.find()
        tweets_negativos = banco.negativos.find({'title':title})
        #tweets_negativos = banco.negativos.find()
        #tweets_modelo = banco.modelo dumps(banco.tweets.find({'name':title}))
        print(title)
        print(tweets_negativos)
        tam_modelo = 0
        #Dados de Treinamento
        for tweet in tweets_negativos:
            tam_modelo+=1
            texto = tweet['tweet']['text']
            negativos.append(tweet)
            dados_treinamento.append([formatar_sentenca(texto), "negativo"])

        for tweet in tweets_positivos:
            tam_modelo+=1
            texto = tweet['tweet']['text']
            positivos.append(tweet)
            dados_treinamento.append([formatar_sentenca(texto), "positivo"])

        # cria o arquivo modelo 
        modelo = NaiveBayesClassifier.train(dados_treinamento)

        #filename = './modelos/'+title+'.obj'
        filename = './modelos/modelo.obj'
        if not os.path.exists(os.path.dirname(filename)):
            try:
                os.makedirs(os.path.dirname(filename))
            except OSError as exc: # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
        

        with open(filename, 'wb') as f:
           modelo_serial = pickle.dump(modelo, f)


        #buscando novos
        consulta = 'place:1b107df3ccc0aaa1 "' + title + '" '
        #numMaxTweets = int(qtd)
        numMaxTweets = 10


        num_positivos = 0
        media_positivos = 0
        num_negativos = 0
        media_negativos = 0

        resultado = []
        for tweet in tweepy.Cursor(api.search, q=consulta).items(numMaxTweets):
            # print(f"{tweet.user.name} said: {tweet.text}")
            sentenca = tweet.text
            sentimento = modelo.classify(formatar_sentenca(sentenca.lower()))
            if sentimento == 'positivo':
                num_positivos+=1
                sent = 'P'
            else:
                num_negativos+=1
                sent = 'N'
            
            resultado.append({'title': title, 'sentimento': sent, 'avaliacao': '',
                                    'tweet': sentenca})
        if num_positivos > 0 :
            media_positivos = (num_negativos + num_positivos) / num_positivos
        if num_negativos > 0 : 
            media_negativos = (num_negativos + num_positivos) / num_negativos

        # print(resultado)
        response_object['message'] = 'Novo Tweets analisados pelo algoritimo'
        response_object['title'] = title
        response_object['resultado'] = json_util.dumps(resultado)
        response_object['numeros'] = {  'num_positivos':num_positivos,
                                        'num_negativos':num_negativos, 
                                        'media_positivos':media_positivos, 
                                        'media_negativos':media_negativos,
                                        'tam_modelo':tam_modelo }


    return jsonify(response_object)


@app.route('/avaliacao', methods=['POST'])
def avaliacao():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        tweets_novos = banco.novos
        tweets_positivos = banco.positivos
        tweets_negativos = banco.negativos
        negativos = []
        positivos = []
        stats = []
        tweets = post_data.get('tweets')

        for tweet in tweets:
           if tweet['sentimento'] == tweet['avaliacao'] and tweet['avaliacao']=='N' :     
               negativos.append(tweet)
          
           if tweet['sentimento'] == tweet['avaliacao'] and tweet['avaliacao']=='P' :     
               positivos.append(tweet)

        if len(positivos)>0:
             tweets_positivos.insert_many(positivos)
        if len(negativos)>0:
            tweets_negativos.insert_many(negativos)
        
        tweets_novos.insert_many(tweets)

        avaliacao = post_data.get('avaliacao')
        estatisticas = banco.estatisticas
        stats.append(avaliacao)
        estatisticas.insert_many(stats)

    return jsonify(response_object)     

# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')



if __name__ == '__main__':
    app.run()