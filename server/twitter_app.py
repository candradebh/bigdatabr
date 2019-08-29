import socket
import sys
import requests
import requests_oauthlib
import json

# Replace the values below with yours
CONSUMER_KEY = "PMrkmRMQy3n7yZnBcY4GYihM6"
CONSUMER_SECRET = "f3e9oFfDfw3MA8ZmrV6QbeSthUDO8UTdb3TFrOsdkGmWRmmzCx"
ACCESS_TOKEN = "92998645-EphmhVfonqO2YbXtBmRIcgZSpA6aoGt6nNPD8JAI9"
ACCESS_SECRET = "0MbzoFCMq4LrGcya8ro2XMrjBifteujAa3NnVsgepHDG4"


my_auth = requests_oauthlib.OAuth1(CONSUMER_KEY, CONSUMER_SECRET,ACCESS_TOKEN, ACCESS_SECRET)


def send_tweets_to_spark(http_resp, tcp_connection):
    for line in http_resp.iter_lines():
        try:
            full_tweet = json.loads(line)
            tweet_text = full_tweet['text'] + '\n'
            print("Tweet Text: " + tweet_text)
            print ("------------------------------------------")
            tcp_connection.send(tweet_text.encode())
        except:
            e = sys.exc_info()[0]
            print("1 Error: %s" % e)


def get_tweets():
    url = 'https://stream.twitter.com/1.1/statuses/filter.json'
    #query_data = [('language', 'en'), ('locations', '-130,-20,100,50'),('track','#')]
    query_data = [('language', 'en'),('locations', '-130,-20,100,50'),('track','#')]
    query_url = url + '?' + '&'.join([str(t[0]) + '=' + str(t[1]) for t in query_data])
    response = requests.get(query_url, auth=my_auth, stream=True)
    print(query_url, response)
    return response



TCP_IP = "localhost"
TCP_PORT = 9009
conn = None
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)
print("Aguardando conexão TCP com: " +  str(TCP_IP) + ":"+ str(TCP_PORT))
print("Execute o arquivo spark_app.py ...")
conn, addr = s.accept()
print(conn)
print("Connected... Starting getting tweets.")
resp = get_tweets()
send_tweets_to_spark(resp,conn)



