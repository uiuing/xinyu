# coding: utf-8
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()



class DialogueContent(db.Model):
    __tablename__ = 'dialogue_content'

    id = db.Column(db.BigInteger, primary_key=True)
    content = db.Column(db.Text)



class DialogueInfo(db.Model):
    __tablename__ = 'dialogue_info'

    dialogue_id = db.Column(db.BigInteger, primary_key=True)
    production_id = db.Column(db.BigInteger, nullable=False)
    consumption_id = db.Column(db.BigInteger, nullable=False)
    consumption_nick_name = db.Column(db.String(255), nullable=False)
    unread_quantity = db.Column(db.BigInteger)
    content_id = db.Column(db.BigInteger, nullable=False)
    content_info = db.Column(db.String(255), nullable=False)



class SignCheck(db.Model):
    __tablename__ = 'sign_check'

    tel = db.Column(db.String(11), primary_key=True, unique=True)
    code = db.Column(db.String(6), nullable=False)



class UserContent(db.Model):
    __tablename__ = 'user_content'

    content_id = db.Column(db.BigInteger, primary_key=True, index=True)
    user_id = db.Column(db.BigInteger, nullable=False)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, nullable=False)

    def to_json(self):
        return {
            'content_id': self.content_id,
            'user_id': self.user_id,
            'content': self.content,
            'create_time': self.create_time
        }


class UserInfo(db.Model):
    __tablename__ = 'user_info'

    id = db.Column(db.BigInteger, primary_key=True, nullable=False, unique=True)
    nick_name = db.Column(db.String(20), primary_key=True, nullable=False, unique=True)
    tel = db.Column(db.String(11), primary_key=True, nullable=False, unique=True)
    password = db.Column(db.String(255, 'utf8_general_ci'))
    introduction = db.Column(db.String(255, 'utf8_general_ci'), nullable=False, server_default=db.FetchedValue())
    authentication = db.Column(db.Enum('学生', '老师', '志愿者'), nullable=False, server_default=db.FetchedValue())
