import uuid
import jsonpickle
import pickle
from flask import Flask, jsonify, request
from flask_cors import CORS

# Biblioteca de Linguagem Natural
import nltk
nltk.download('punkt')
from nltk.tokenize import word_tokenize
from nltk.classify import NaiveBayesClassifier

#Banco de Dados
from pymongo import MongoClient
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


        response_object['data'] = { 'tweets_positivos': json_util.dumps(tweets_positivos), 'tweets_negativos': json_util.dumps(tweets_negativos) }
        

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
        positivos = []
        negativos = []
        neutros = []
        dados_treinamento = []
        tweets = post_data.get('tweets')
        title = post_data.get('title')

        # COLECTIONS MONGODB
        tweets_positivos = banco.positivos
        tweets_negativos = banco.negativos
        #tweets_modelo = banco.modelo

        for tweet in tweets:
            texto = tweet['tweet']['text']
            #print (texto.encode('utf8').lower())
            if tweet['sentimento'] == "N":
                negativos.append(tweet)
                dados_treinamento.append([formatar_sentenca(texto), "negativo"])

            if tweet['sentimento'] == "P":
                positivos.append(tweet)
                dados_treinamento.append([formatar_sentenca(texto), "positivo"])
            

        if len(positivos)>0:
             tweets_positivos.insert(positivos)
        if len(negativos)>0:
            tweets_negativos.insert(negativos)
        
        response_object['message'] = 'Tweets armazenados no banco de dados'
        response_object['title'] = title
        
     
    return jsonify(response_object)

@app.route('/analisar', methods=['POST'])
def analisar():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        positivos = []
        negativos = []
        neutros = []
        dados_treinamento = []
        qtd = post_data.get('qtd')
        title = post_data.get('title')

        tweets_novos = banco.novos
        tweets_positivos = banco.positivos.find({'title':title})
        tweets_negativos = banco.negativos.find({'title':title})
        #tweets_modelo = banco.modelo dumps(banco.tweets.find({'name':title}))

        #Dados de Treinamento
        for tweet in tweets_negativos:
            texto = tweet['tweet']['text']
            negativos.append(tweet)
            dados_treinamento.append([formatar_sentenca(texto), "negativo"])

        for tweet in tweets_positivos:
            texto = tweet['tweet']['text']
            positivos.append(tweet)
            dados_treinamento.append([formatar_sentenca(texto), "positivo"])

            
        
        
        modelo = NaiveBayesClassifier.train(dados_treinamento)
        with open('cruzeiro.obj', 'wb') as f:
           modelo_serial = pickle.dump(modelo, f)


        #buscando novos
        consulta = 'place:1b107df3ccc0aaa1 "' + title + '" '
        numMaxTweets = int(qtd)
        tweets_buscados = []
        for tweet in tweepy.Cursor(api.search, q=consulta).items(numMaxTweets):
            # tweets.insert({ 'name': title , 'sentimento':'','avaliacao':'', 'tweet': tweet._json })
            tweets_buscados.append({'title': title, 'sentimento': '', 'avaliacao': '',
                                    'tweet': tweet._json})

        

        tweets_novos.insert(tweets_buscados)

        resultado = []
        for tweet in tweets_novos.find({'title':title}):
            sentenca = tweet['tweet']['text']
            sentimento = modelo.classify(formatar_sentenca(sentenca.lower()))
            #texto_resultado = '(' + sentimento + ') ' + sentenca + '\n'
            resultado.append({'title': title, 'sentimento': sentimento, 'avaliacao': '',
                                    'tweet': sentenca})

        # print(resultado)
        response_object['message'] = 'Novo Tweets analisados pelo algoritimo'
        response_object['title'] = title
        response_object['data'] = json_util.dumps(tweets_buscados)
        response_object['resultado'] = json_util.dumps(resultado)


    return jsonify(response_object)


# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')




if __name__ == '__main__':
    app.run()