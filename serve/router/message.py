import json
from datetime import datetime
from flask import Blueprint, request
from sqlalchemy import or_

from model.user import UserContent, UserInfo, UnreadDialogue
from utils.paser.request import parser_post
from model.user import DialogueInfo, DialogueContent, db

message = Blueprint('message', __name__)


@message.route('/get_dialogue/user', methods=['POST'])
def get_dialogue_user():
    """
    获取用户所有的对话列表
    :param: user_id
    :return: data
    """
    req = parser_post(request)
    if req['user_id']:
        # 数据库查询 production_id=user_id 或者 consumption_id=user_id
        data = DialogueInfo.query.filter(
            or_(DialogueInfo.production_id == req['user_id'], DialogueInfo.consumption_id == req['user_id'])).all()
        res = {'status': True,
               'data': [i.to_json() for i in data]
               }
    else:
        res = {'status': False}
    return res


@message.route('/get_dialogue/content', methods=['POST'])
def get_dialogue_content():
    """
    获取指定内容所有的对话列表
    :param: content_id
    :return: data
    """
    req = parser_post(request)
    if req['content_id']:
        # 数据库查询
        data = DialogueInfo.query.filter_by(content_id=req['content_id']).all()

        res = {'status': True,
               'data': [i.to_json() for i in data]
               }
    else:
        res = {'status': False}
    return res


@message.route('/dialogue', methods=['POST'])
def dialogue():
    """
    获取对话详情
    :param:
    :return: data
    """
    req = parser_post(request)
    if req['dialogue_id']:
        # 获取两个用户的昵称
        ram_dialogue_info = DialogueInfo.query.filter_by(dialogue_id=req['dialogue_id']).first()
        production_nickname = UserInfo.query.filter_by(id=ram_dialogue_info.production_id).first().nick_name
        consumption_nickname = UserInfo.query.filter_by(id=ram_dialogue_info.consumption_id).first().nick_name

        data = DialogueContent.query.get(req['dialogue_id'])
        res = {
            'status': True,
            'data': {
                'production_id': ram_dialogue_info.production_id,
                'production_nickname': production_nickname,
                'consumption_id': ram_dialogue_info.consumption_id,
                'consumption_nickname': consumption_nickname,
                'content': data.content,
            }
        }
    else:
        res = {'status': False}
    return res


@message.route('/dialogue/add', methods=['POST'])
def dialogue_add():
    """
    发送对话
    :param: production_id, consumption_id, content_id, content
    :return: data
    """
    req = parser_post(request)
    if req['production_id'] and req['consumption_id'] and req['content_id'] and req['content']:
        # 判断两个数据库里面是否存在这条内容，如果存在，则更新，如果不存在，则添加
        data = DialogueInfo.query.filter_by(production_id=req['production_id'], consumption_id=req['consumption_id'],
                                            content_id=req['content_id']).first()
        if data:
            DialogueContent.query.filter_by(id=data.dialogue_id).update({'content': req['content']})
            db.session.commit()
            res = {'status': True, 'data': {'once': False}}
        else:
            content_info = UserContent.query.filter_by(content_id=req['content_id']).first()
            ram_dialog_content = DialogueInfo(production_id=req['production_id'], consumption_id=req['consumption_id'],
                                              content_id=req['content_id'], content_info=content_info.content,
                                              content_create_time=content_info.create_time)
            db.session.add(
                ram_dialog_content
            )
            db.session.flush()
            db.session.add(
                DialogueContent(id=ram_dialog_content.dialogue_id, content=req['content'])
            )
            db.session.commit()
            res = {'status': True, 'data': {'once': True, 'dialogue_id': ram_dialog_content.dialogue_id}}
    else:
        res = {'status': False}
    return res


@message.route('/dialogue/user/unread_count', methods=['POST'])
def dialogue_user_unread_count():
    """
    获取用户未读消息数量
    :param:
    :return: data
    """
    req = parser_post(request)
    if req['user_id']:
        # 获取用户每条消息的number_unread累加计算除总数
        unread = UnreadDialogue.query.filter_by(unread_user_id=req['user_id']).all()
        number_unread = 0
        for i in unread:
            number_unread += i.number_unread
        res = {'status': True, 'data': {'number_unread': number_unread}}
    else:
        res = {'status': False}
    return res


@message.route('/dialogue/user/unread_list', methods=['POST'])
def dialogue_user_unread_list():
    """
    获取用户未读消息列表
    :param: user_id
    :return: data
    """
    req = parser_post(request)
    if req['user_id']:
        # 获取未读消息列表
        unread_list = UnreadDialogue.query.filter_by(unread_user_id=req['user_id']).all()
        res = {'status': True, 'data': {'unread_list': [unread.to_json() for unread in unread_list]}}
    else:
        res = {'status': False}
    return res


@message.route('/dialogue/user/read', methods=['POST'])
def dialogue_user_read():
    """
    设置用户消息为已读
    :param: user_id, dialogue_id
    :return: data
    """
    req = parser_post(request)
    if req['user_id'] and req['dialogue_id']:
        # 设置用户消息为已读
        UnreadDialogue.query.filter_by(unread_user_id=req['user_id'], dialogue_id=req['dialogue_id']).delete()
        # 更新消息打开时间
        DialogueInfo.query.filter_by(dialogue_id=req['dialogue_id']).update({'open_time': datetime.now()})
        db.session.commit()
        res = {'status': True}
    else:
        res = {'status': False}
    return res


@message.route('/dialogue/user/unread_add', methods=['POST'])
def dialogue_user_unread_add():
    """
    更新用户未读消息个数
    :param: user_id, dialogue_id
    :return: data
    """
    req = parser_post(request)
    if req['user_id'] and req['dialogue_id']:
        # 添加用户未读消息
        # 如果存在则更新，如果不存在则添加
        data = UnreadDialogue.query.filter_by(unread_user_id=req['user_id'],
                                              dialogue_id=req['dialogue_id']).first()
        if data:
            UnreadDialogue.query.filter_by(unread_user_id=req['user_id'], dialogue_id=req['dialogue_id']).update(
                {'number_unread': 1 + data.number_unread})
            db.session.commit()
        else:
            ram_unread_dialogue = UnreadDialogue(unread_user_id=req['user_id'], dialogue_id=req['dialogue_id'],
                                                 number_unread=1)
            db.session.add(
                ram_unread_dialogue
            )
            db.session.commit()
        res = {'status': True}
    else:
        res = {'status': False}
    return res
