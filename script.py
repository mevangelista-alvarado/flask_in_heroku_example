import tweepy
import time
from os import environ

CONSUMER_KEY = environ['CONSUMER_KEY']
CONSUMER_SECRET = environ['CONSUMER_SECRET']
ACCESS_KEY = environ['ACCESS_KEY']
ACCESS_SECRET = environ['ACCESS_SECRET']
INFLUENCER = "MujeresUAGro"
calls = 0

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)
print("Credenciales Listas")

influencer = api.get_user(INFLUENCER)
following = api.friends_ids(influencer.id)

print("Amigos de influencer listo")

for account in following:
  account = api.get_user(account)
  api.create_friendship(account.id)
  print("Creando Amistad {}".format(calls))
  calls = calls + 1

  if calls%13 == 0:
      print("Esperando...")
      time.sleep(60 * 15)
      
print("Finish with Influencer {}".format(influencer.id))
    