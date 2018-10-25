import os
from datetime import datetime
from flask import Flask, request, jsonify
#from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from utils import ApiTwitter, wait_time

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'crud.sqlite')
#db = SQLAlchemy(app)
ma = Marshmallow(app)

#Create a model
#class User(db.Model):
#    id = db.Column(db.Integer, primary_key=True)
#    twitter_user = db.Column(db.String(80), unique=True)
#    email = db.Column(db.String(120), unique=True)
#
#    def __init__(self, twitter_user, email):
#        self.twitter_user = twitter_user
#        self.email = email


@app.route('/')
def homepage():
    the_time = datetime.now().strftime("%A, %d %b %Y %l:%M %p")

    return """
    <h1>Hello heroku</h1>
    <p>It is currently {time}.</p>

    <img src="http://loremflickr.com/320/240/dog">
     """.format(time=the_time)

#### Endpoints #####
class UserSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('twitter_user', 'email', 'keyword')

user_schema = UserSchema()
users_schema = UserSchema(many=True)

# endpoint to create new user
@app.route("/api/influencer", methods=["POST"])
def add_user():
    twitter_user = request.json['twitter_user']
    email = request.json['email']
    
    _api = ApiTwitter()
    influencer = _api.get_user(twitter_user)
    friends_influencer = _api.get_friends(influencer.id)
    calls = 0

    for account in friends_influencer:
        account = _api.get_user(account)
        if _api.follow_this_user("AlvMevangelista", account.id):
            _api.create_friend(account.id)
            calls = calls + 1
            for tweet in _api.timeline(account.id, 1):
                if _api.fav_tweet(tweet.id):
                    print("Fav Tweet ready")
                else:
                    print("Already fav Tweet before")
        else:
            continue

        if calls%13 == 0:
            wait_time()

    return jsonify(twitter_user)

@app.route("/api/test", methods=["POST"])
def reply_tweet():
    keyword = request.json['keyword']
    _api = ApiTwitter()

    dic_user = _api.search_by_keyword(keyword, limit_tweets=5)
    _api.response_tweet(dic_user, copy='Hi this a test [I am Bot]!')

    return jsonify('Ready')

if __name__ == '__main__':
    app.run(debug=True)