import os
import json
import http.client

import config

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy


#constants
URL_PREFIX = "graph.facebook.com";
APP_ID = "387638781429773";
APP_SECRET = "c3215108a42e5e389c6e18dbd329eb51";

#setup
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db  = SQLAlchemy(app)


#database model
class FBuser(db.Model):
    __tablename__ = 'fbuser'

    userid       = db.Column(db.String(), primary_key=True)
    username     = db.Column(db.String())
    access_token = db.Column(db.String())

    def __init__(self, userid, username, access_token):
        self.userid = userid
        self.username = username
        self.access_token = access_token

    def __repr__(self):
        return '<userid {}>'.format(self.userid)


"""
Http GET reponse
"""
def httpGet(uri):
    conn = http.client.HTTPSConnection(URL_PREFIX)    
    conn.request("GET", uri)
    r1 = conn.getresponse()
    return r1.read()
"""
Gets a long live token
"""
def getExtendedToken(token):
    response = httpGet("/oauth/access_token?grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s" % (APP_ID, APP_SECRET, token))
    return str(response)[15:]


@app.route('/user/<username>')
def getuserid(username):
    response = httpGet("/%s" % username)
    json_parse = json.loads(str(response)[2:-1])

    try:
        id = json_parse['id']    
        return json.dumps({'id' : id, "status" : 1})
    except KeyError:
        return json.dumps({"status" : 0})

@app.route('/addtoken/<username>/<token>')
def addtoken(username, token):
    extended_token = getExtendedToken(token)
    userid = json.loads(getuserid(username))['id']

    try:
        db.session.add(FBuser(userid, username, extended_token))
        db.session.commit()
        return json.dumps({"status": 1})
    except:
        return json.dumps({"status": 0})
    

@app.route('/photos/<username>')
def getphotos(username):
    user = FBuser.query.filter_by(username='aajjbbk').first()
    
    response = httpGet("/v2.3/%s/me?access_token=%s" % (user.userid, user.access_token))
    
    return str(response.decode('utf-8'))

if __name__ == "__main__":
    app.run(debug=True)
