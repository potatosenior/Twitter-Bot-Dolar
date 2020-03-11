import tweepy 
import requests
import threading
import datetime

consumer_key = ''
consumer_secret = '' 
access_token = '' 
access_token_secret = '' 
auth = tweepy.OAuthHandler(consumer_key, consumer_secret) 
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
path = "./images/" # caminho da imagem
index = 1 # imagem inicial
total = 11 # total de imagens
lastValue = 0 # ultima cotacao

def publicarTweet(imagePath, dollar): # http://docs.tweepy.org/en/latest/api.html#API.media_upload
  data = datetime.datetime.now()
  diaAtual = data.strftime("%A")
  horarioAtual = data.hour - 3# int, -3 pois na VM ta adiantado 3hrs
  horario_str = '%d/%d %dh' % (data.day, data.month, horarioAtual)
  
  if(diaAtual == "Saturday" or diaAtual == "Sunday"): # sabado e domingo bolsa nao abre
    print('--Bolsa fechada (final de semana)' + horario_str)
    return
  if(horarioAtual < 10 or horarioAtual > 17): # horario da bolsa
    print('--Bolsa fechada (horario)' + horario_str)
    return

  global lastValue

  emoji = "➖"
  if(float(dollar) > float(lastValue)):
    emoji = "⬆️"
    if(float(dollar) < float(lastValue)):
      emoji = "⬇️"
  lastValue = float(dollar)

  status = emoji + "  Valor atual do @50cent: R$ %.2f" % (float(dollar) / 2)
  api.update_with_media(imagePath, status)
  print('Tweet publicado em ', horario_str)
  print("-Imagem publicada: ", index)

def valorAtualDollar(): 
  # https://docs.awesomeapi.com.br/api-de-moedas
  # bid -> Compra
  # ask -> Venda
  # high -> Maximo
  # low -> Minimo
  response = requests.get("https://economia.awesomeapi.com.br/all/USD-BRL")
  dollar = response.json()['USD']['bid']
  code = response.status_code
  print("Valor atual do dollar: R$ %.2f (compra)" % (float(dollar)))

  if(code != 200):
    print("Erro na API de dollar! Error code: %d" % (code))
    return ""
  return dollar

def setInterval(func, time):
  e = threading.Event()
  while not e.wait(time):
      func()

def main():
  global index
  
  dollar = valorAtualDollar()
  if(dollar): 
    publicarTweet(path + str(index) + ".jpg", dollar) 
  else: 
    return
  index += 1
  if index == total:
    index = 1

print("Bot iniciado")
main()
setInterval(main, 60 * 60 * 2.5) # Intervalo entre cada post em segundos