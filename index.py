import os
import json
import http.client

import Parser

from flask import Flask
from flask import render_template, request
from flask.ext.sqlalchemy import SQLAlchemy


#constants
URL_PREFIX = "graph.facebook.com";
APP_ID = "466465463517234";
APP_SECRET = "d12434e88aff924402e529c6c8b493df";

#setup
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['DEBUG'] = True
db  = SQLAlchemy(app)


#database models
class FBuserTable(db.Model):
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

class InviteTable(db.Model):
    __tablename__ = 'invite'

    id = db.Column(db.Integer(), primary_key=True)
    userid = db.Column(db.String())

    def __init__(self, userid):
        self.userid = userid

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
    response = httpGet("/oauth/access_token?grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s"
                       % (APP_ID, APP_SECRET, token)).decode("utf-8")

    if response.startswith('access_token'):
        return str(response)[13:-16]
    else:
        return -1

@app.route('/local')
def local():
    return render_template("local.html")

@app.route('/echo')
def echo1():
    return render_template("echo.html")
    
@app.route('/beta_login')
def beta_login():
    return render_template("beta_login.html")

@app.route('/getMe')
def get_me():
    return render_template("getMe.html")
	
@app.route('/login')
def login():
    return render_template("login.html")
	
@app.route('/appinvite')
def appinvite():
    return render_template("appinvite.html")

@app.route('/testajax')
def testajax():
    return render_template("tester.html")
	
@app.route('/invite/<userid>')
def inviteUser(userid):
    invite = InviteTable.query.filter_by(userid=userid).first()

    if invite:
        return json.dumps({"status": 0, "message": "already invited"})
    else:
        db.session.add(InviteTable(userid))
        db.session.commit()
        return json.dumps({"status": 1})
    
@app.route('/adduser/<userid>/<username>/<token>')
def adduser(userid, username, token):
    try:
        extended_token = getExtendedToken(token)
    
        if extended_token != -1:        
            try:
                db.session.add(FBuserTable(userid, username, extended_token))
                db.session.commit()
                return json.dumps({"status": 1})
            except:
                return json.dumps({"status": 0, "message": "error inserting user token"})
            else:
                return json.dumps({"status": 0, "message": "invalid initial token"});
    except:
        return json.dumps({"status": 0, "message": "error accessing token, perhaps user does not exists or an error happened while acquiring the extended token"})
    
"""
status =>
0 = user not in the system
1 = user registered
2 = user invited
"""

def getUserStatus(userid):
    status = 0
    user = FBuserTable.query.filter_by(userid=userid).first()

    if user:
        status = 1
    else:
        if InviteTable.query.filter_by(userid=userid).first():
            status = 2
    return status

@app.route('/singleuserstatus/<userid>')
def singleuserstatus(userid):
    return json.dumps({"status" : getUserStatus(userid)})

@app.route('/userstatus/<userid_1>/<userid_2>')
def userstatus(userid_1, userid_2):
    return json.dumps({"status_1" : getUserStatus(userid_1), "status_2": getUserStatus(userid_2)})
    
    
@app.route('/user/<userid>')
def getUserInfo(userid):
    user = FBuserTable.query.filter_by(userid=userid).first()

    user['status'] = 1;
    
    if user:
        return json.dumps(user)
    else:
        return json.dumps({"status": 0})

@app.route('/photos')
def getphotos():
    username = request.args.get('username')
    user = FBuserTable.query.filter_by(username=username).first()

    return json.dumps(user)
"""
    response_all = httpGet("/v2.3/%s/photos?access_token=%s" % (user.userid, user.access_token)).decode("utf-8")
    response_uploaded = httpGet("/v2.3/%s/photos?access_token=%s&type=uploaded" % (user.userid, user.access_token)).decode("utf-8")
    
    return json.dumps(Parser.parse(response_all, [""]) + Parser.parse(response_uploaded, [""]))
"""    
@app.route('/parsedphotos')
def getparsedphotos(username):
    username = request.args.get('username')
    tags = request.args.get('tags').split(",")
    
    user = FBuserTable.query.filter_by(username=username).first()
    
    response_all = httpGet("/v2.3/%s/photos?access_token=%s" % (user.userid, user.access_token)).decode("utf-8")
    response_uploaded = httpGet("/v2.3/%s/photos?access_token=%s&type=uploaded" % (user.userid, user.access_token)).decode("utf-8")

    return json.dumps(Parser.parse(response_all, tags) + Parser.parse(response_uploaded, tags))

