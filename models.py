from index import db
from sqlalchemy.dialects.postgresql import JSON


class FBuser(db.Model):
    __tablename__ = 'fbuser'

    userid       = db.Column(db.String(), primary_key=True)
    access_token = db.Column(db.String())

    def __init__(self, userid, access_token):
        self.userid = userid
        self.access_token = access_token

    def __repr__(self):
        return '<userid {}>'.format(self.userid)
