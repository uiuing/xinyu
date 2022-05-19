import base64
from urllib.parse import quote

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
    content_id = db.Column(db.BigInteger, nullable=False)
    content_info = db.Column(db.Text, nullable=False)
    content_create_time = db.Column(db.DateTime, nullable=False)
    open_time = db.Column(db.DateTime, nullable=False)

    def to_json(self):
        # 获取用户昵称
        consumption_nick_name = UserInfo.query.filter_by(id=self.consumption_id).first().nick_name
        production_nick_name = UserInfo.query.filter_by(id=self.production_id).first().nick_name
        return {
            'dialogue_id': self.dialogue_id,
            'production_id': self.production_id,
            'consumption_id': self.consumption_id,
            'content_id': self.content_id,
            'content_info': self.content_info,
            "consumption_nick_name": consumption_nick_name,
            "production_nick_name": production_nick_name,
            'create_time': self.content_create_time.strftime('%Y-%m-%d %H:%M:%S'),
        }


class UnreadDialogue(db.Model):
    __tablename__ = 'unread_dialogue'
    dialogue_id = db.Column(db.BigInteger, primary_key=True)
    number_unread = db.Column(db.Integer)
    unread_user_id = db.Column(db.BigInteger)

    def to_json(self):
        return {
            'dialogue_id': self.dialogue_id,
            'number_unread': self.number_unread,
            'unread_user_id': self.unread_user_id
        }


class SignCheck(db.Model):
    __tablename__ = 'sign_check'

    tel = db.Column(db.String(11), primary_key=True, unique=True, index=True)
    code = db.Column(db.String(6), nullable=False)
    count = db.Column(db.Integer, default=0)
    start_time = db.Column(db.DateTime, nullable=False)


class UserContent(db.Model):
    __tablename__ = 'user_content'
    content_id = db.Column(db.BIGINT, primary_key=True, nullable=False, unique=True, index=True, autoincrement=True)
    user_id = db.Column(db.BIGINT, nullable=False)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, nullable=False)
    open_permissions = db.Column(db.String(20), nullable=False)

    def to_json(self):
        # 获取用户昵称
        nick_name = UserInfo.query.filter_by(id=self.user_id).first().nick_name
        return {
            'content_id': self.content_id,
            'user_id': self.user_id,
            'content': self.content,
            'create_time': self.create_time.strftime('%Y-%m-%d %H:%M:%S'),
            'nick_name': nick_name,
            'open_permissions': self.open_permissions
        }


class UserInfo(db.Model):
    __tablename__ = 'user_info'

    id = db.Column(db.BIGINT, primary_key=True, autoincrement=True, nullable=False, unique=True, index=True)
    nick_name = db.Column(db.String(20), primary_key=True, nullable=False)
    tel = db.Column(db.String(11), primary_key=True, nullable=False)
    password = db.Column(db.String(255, 'utf8_general_ci'))
    introduction = db.Column(db.String(255, 'utf8_general_ci'), server_default=db.FetchedValue())
    authentication = db.Column(db.Enum('students', 'teacher'), nullable=False, server_default=db.FetchedValue())
