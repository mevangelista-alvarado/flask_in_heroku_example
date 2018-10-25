#-*- encoding: utf-8 -*-
''' Write a Api Class who use Tweepy! '''
#Python Libraries
import tweepy
import os
#Others
from secrets import KEYS 

def wait_time():
    '''This method wait a 15 minutes'''
    print("Wait 15 minutes")
    time.sleep(60 * 15)

def catch_variable(key_name): 
    '''Assign a value to variable with name key_name'''
    try:
        variable = os.environ[key_name]
    except:
        variable = KEYS.get(key_name, "")
    return variable


def test():
    ''' Testing app '''
    print "Hi test!"
    _api = ApiTwitter()

class ApiTwitter(object):

    def __init__(self, *args, **kwargs):
        self.app_key = catch_variable("consumer_key")
        self.app_secret = catch_variable("consumer_secret")
        self.token_key = catch_variable("access_token")
        self.token_secret = catch_variable("access_secret")
        if self.app_key == "" or  self.app_secret == "" or self.token_key == "" or self.token_secret == "":
            print("Check your secrets file!")

        #Start session from Twitter API
        self.authentication = tweepy.OAuthHandler(self.app_key, self.app_secret)
        self.authentication.set_access_token(self.token_key, self.token_secret)
        self.twitter = tweepy.API(self.authentication)

        self.verify_credentials()

    def verify_credentials(self):
        '''Verify if your credentials is correct'''
        try:
            self.twitter.verify_credentials()
            print("Credentials Verifed")
        except Exception as e:
            print("[API Authentication] Line 36 Error: {}".format(e))

    def get_user(self, user):
        '''Get all user's information'''
        try:
            twitter_user = self.twitter.get_user(user)
        except Exception as e:
            print("[API GET USER] Line 43 Error: {}".format(e))
        return twitter_user

    def get_friends(self, user):
        '''Get all friends to a user'''
        try:
            user_friends = self.twitter.friends_ids(user)
        except Exception as e:
            print("[API FRIENDS IDS] Line 51 Error: {}".format(e))
        #Return a list type variable
        return user_friends

    def create_friend(self, friend):
        '''Create a frienship with a given friend'''
        try:
            self.twitter.create_friendship(friend)
            print("Friendship create with {}".format(friend))
        except Exception as e:
            print("[CREATE FRIENDSHIP] Line 61 Error: {}".format(e))

    def timeline(self, user, tweets):
        '''Get a numbers of tweets of user'''
        try:
            timeline= tweepy.Cursor(self.twitter.user_timeline, user)
        except Exception as e:
            print("[TWEEPY CURSOR] Line 68 Error {}".format(e))

        return timeline.items(tweets)

    def fav_tweet(self, tweet_id):
        '''Gime like to a tweet'''
        try:
            self.twitter.create_favorite(tweet_id)
            return True
        except Exception as e:
            print("[CREATE FAVORITE] Line 78 Error {}".format(e))
            return False

    def follow_this_user(self, owner_account, account):
        '''Determines if the owner user follows a user'''
        try:
            #import code; code.interact(local=locals())
            owner_account = self.twitter.get_user(owner_account)
            account = self.twitter.get_user(account)
        except Exception as e:
            print("[GET USER] Line 88 Error {}".format(e))

        if account.following:
            print("Account followed previously")
            return False
        else:
            if owner_account.id == account.id:
                print("The ID {} is the owner account".format(account.id))
                return False
            else:
                return True

    def get_followers(self, owner_user):
        '''Get followings of owner account '''
        try:
            account = self.twitter.get_user(owner_user)
        except Exception as e:
            print("[GET USER] Line 105 Error {}".format(e))
        try:
            followers = account.followers_ids()
        except Exception as e:
            print("[FOLLOWERS IDS] Line 109 Error: {}".format(e))
        #Return a list type variable
        return followers

    def destroy_friend(self, friend):
        '''Destroy frienship with a given friend'''
        try:
            self.twitter.destroy_friendship(friend)
            print("Destroy Friendship with {}".format(friend))
        except Exception as e:
            print("[DESTROY FRIENDSHIP] Line 119 Error: {}".format(e))

    def search_by_keyword(self, keyword, limit_tweets=200):
        '''
            This method searches a quantity of tweets that contain a keyword and 
            returns a dictionary of users id who published a tweet with 
            this keyword and tweet id
        '''
        users = {}
        for tweet in tweepy.Cursor(self.twitter.search, q=keyword).items(limit_tweets):
            #This is to kwon if he tweet is a retweet
            if tweet.retweet_count == 0 and tweet.lang == 'es':
                users[tweet.id_str] = tweet.user.screen_name

        return users

    def response_tweet(self, dic_user, copy='Hi this a test!'):
        '''
            This method response a tweet for english language 
        '''
        tweets = dic_user.keys()
        for tweet_id in tweets:
            #import code; code.interact(local=locals())
            screen_name = dic_user[tweet_id]
            message = "@" + screen_name + " " + copy
            self.twitter.update_status(message, tweet_id)

        print("[RESPONSE TWEET] Finished")






