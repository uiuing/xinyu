import random
from datetime import datetime
from flask import Blueprint, request
from sqlalchemy import func, or_

from utils.paser.request import parser_post
from model.user import UserContent, db, DialogueInfo, DialogueContent, UserInfo

content = Blueprint('content', __name__)


@content.route('/add', methods=['POST'])
def add():
    """
    添加内容
    :param: tel content open_permissions
    :return: data
    """
    req = parser_post(request)
    if req['content'] and req['user_id'] and req['open_permissions']:
        # 添加到数据库
        # 获取yyyy-mm-dd hh:mm:ss格式的时间
        db.session.add(
            UserContent(user_id=int(req['user_id']), content=req['content'], open_permissions=req['open_permissions'],
                        create_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        )
        db.session.commit()
        res = {'status': True}
    else:
        res = {'status': False}
    return res


@content.route('/delete', methods=['POST'])
def delete():
    """
    删除内容
    :param: content_id
    :return: data
    """
    req = parser_post(request)
    if req['content_id']:
        # 删除数据库中的内容
        UserContent.query.filter_by(content_id=int(req['content_id'])).delete()
        dialogue = DialogueInfo.query.filter_by(content_id=int(req['content_id'])).all()
        print(dialogue)
        for i in dialogue:
            dialogue_id = i.dialogue_id
            DialogueInfo.query.filter_by(dialogue_id=dialogue_id).delete()
            DialogueContent.query.filter_by(id=dialogue_id).delete()
        db.session.commit()
        res = {'status': True}
    else:
        res = {'status': False}
    return res


@content.route('/get_history', methods=['POST'])
def get_history():
    """
    获取历史记录
    :param: tel
    :return: data
    """
    req = parser_post(request)
    if req['user_id']:
        # data转换为json
        data = UserContent.query.filter_by(user_id=int(req['user_id'])).all()
        # 对data对象根据create_time从大到大小排序
        data = sorted(data, key=lambda x: x.create_time, reverse=True)
        res = {
            'status': True,
            'data': [i.to_json() for i in data]
        }
    else:
        res = {'status': False}
    return res


@content.route('/get_recommend_content', methods=['POST'])
def get_recommend_content():
    """
    获取推荐内容
    :param: tel
    :return: data
    """
    req = parser_post(request)
    if req['user_id']:
        # 获取UserContent表长度
        # 获取不重复且随机的10条推荐内容 并排除当前用户的内容
        # 仅老师可见的内容和学生内容区别开来
        # 判断用户是否是老师
        user = UserInfo.query.filter_by(id=int(req['user_id'])).first()
        print(user.authentication)
        if user.authentication == 'teacher':
            # 根据用户id分组
            data = UserContent.query.filter(UserContent.user_id != int(req['user_id'])).order_by(func.rand()).limit(
                10).all()
        else:
            data = UserContent.query.filter(UserContent.user_id != int(req['user_id']),
                                            UserContent.open_permissions == 'all').order_by(func.rand()).limit(3).all()
        ram_data = [i.to_json() for i in data];
        # 对ram_data对象根据去DialogueInfo表中匹配content_id=i['content_id'],production_id=i['user_id']或者consumption_id相等，如果存在则在ram_data中删除
        for i in ram_data[::-1]:
            dialogue = DialogueInfo.query.filter(DialogueInfo.content_id == i['content_id']).filter(
                or_(DialogueInfo.production_id == req['user_id'], DialogueInfo.consumption_id == req['user_id'])).first()
            if dialogue:
                ram_data.remove(i)
        # print(ram_data)
        # 随机打乱ram_data
        ram_data = random.sample(ram_data, len(ram_data))

        res = {
            'status': True,
            'data': ram_data,
        }
    else:
        res = {'status': False}
    return res
