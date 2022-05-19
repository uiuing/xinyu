import base64
import random
import time

from flask import Blueprint, request
from model.user import SignCheck, UserInfo, db
from utils.paser.request import parser_post
from urllib.parse import quote, unquote
from tencentcloud.common import credential
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
# 导入对应产品模块的client models。
from tencentcloud.sms.v20210111 import sms_client, models

# 导入可选配置类
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile

sign = Blueprint('sign', __name__)


def sdk_send_sms(tel, code):
    """
    腾讯云发送短信
    :param tel:
    :param code:
    """
    # 使用腾讯SDK发送验证码
    try:
        cred = credential.Credential("AKIDc2OUfbqgp7JxS4qx3va6pgR4Siz4hA3H", "IhLqIYgmna8R4Sfm12qrkct0qiNvdifu")

        # 非必要步骤:
        # 实例化一个客户端配置对象，可以指定超时时间等配置
        clientProfile = ClientProfile()
        clientProfile.signMethod = "TC3-HMAC-SHA256"  # 指定签名算法
        clientProfile.language = "en-US"

        client = sms_client.SmsClient(cred, "ap-guangzhou", clientProfile)
        req = models.SendSmsRequest()

        req.SmsSdkAppId = "1400664121"
        req.SignName = "学习日志个人网"
        req.TemplateId = "1395969"
        req.TemplateParamSet = [str(code)]
        req.PhoneNumberSet = ["+86" + tel]

        client.SendSms(req)

    except TencentCloudSDKException as err:
        print(err)


@sign.route('/sendCode', methods=['POST'])
def send_code():
    """
    发送验证码
    :param: phoneNumber:PhoneNumber
    :return: data
    """
    req = parser_post(request)
    # 发送验证码并存储到数据库
    if req['phoneNumber']:
        # 生成随机的6位数
        code = str(int(random.random() * 1000000))
        # 判断code长度，如果小于6位则补充0
        if len(str(code)) < 6:
            code = str(code) + '0' * (6 - len(str(code)))

        tel = str(req['phoneNumber'])

        # 判断count的值是不是>=4，>=4则不发送验证码
        count = SignCheck.query.filter(SignCheck.tel == tel).first()
        if count:
            if count.count >= 4:
                if count.start_time:
                    # 获取当前时间，判断是否过了一天
                    now = time.time()
                    if now - count.start_time >= 86400:
                        # 过了一天，重置count的值
                        count.count = 1
                        count.code = code
                        db.session.commit()
                        sdk_send_sms(tel, code)
                        res = {'status': True}
                    else:
                        res = {'status': False}
                else:
                    count.start_time = time.time()
                    db.session.commit()
                    res = {'status': False}
            else:
                count.code = code
                count.count += 1
                db.session.commit()
                sdk_send_sms(tel, code)
                res = {'status': True}
        else:
            # 如果电话号码不存在则插入新的验证码
            count = SignCheck(tel=tel, code=code, count=1)
            db.session.add(count)
            db.session.commit()
            sdk_send_sms(tel, code)
            res = {'status': True}
        # 响应对象
    else:
        res = {'status': False}
    return res


@sign.route('/verifyCode', methods=['POST'])
def verify_code():
    """
    校验验证码
    :param: phoneNumber&code
    :return: data
    """
    req = parser_post(request)
    if req['phoneNumber'] and req['code']:
        tel = req['phoneNumber']
        # 从数据库获取验证码
        code = SignCheck.query.get(tel).code
        # 判断验证码是否正确，如果正确则添加用户信息，否则返回错误信息
        if req['code'] == code:
            # 从数据库获取用户id
            user_obj = UserInfo.query.filter(UserInfo.tel == tel).first()
            # 存在则返回用户id，不存在则新增用户
            if user_obj:
                res = {'status': True,
                       'data': {"check_judgment": True, "user_id": user_obj.id, "nick_name": user_obj.nick_name}}
            else:
                # 将电话号码关键信息变成*符号
                nick_name = tel[0:3] + '****' + tel[7:]
                # 将nick_name 进行urlencoded编码 -> 进行base64编码
                nick_name = base64.b64encode(quote(nick_name, safe="~!@#$&*()=:/,;?+'").encode("utf-8")).decode("utf-8")
                # 插入新的用户信息
                db.session.add(
                    UserInfo(id=None, nick_name=nick_name, tel=tel, password='', authentication='students')
                )
                db.session.commit()
                # 获取新的用户id
                user_id = UserInfo.query.get(UserInfo.tel == tel).first().id
                res = {'status': True, 'data': {"check_judgment": True, "user_id": user_id, "nick_name": nick_name}}
        else:
            res = {'status': False, 'data': {"check_judgment": False}}
    else:
        res = {'status': False}
    return res


@sign.route('/getNickName', methods=['POST'])
def get_nick_name():
    """
    获取用户昵称
    :param: user_id
    :return: data
    """
    req = parser_post(request)
    if req['user_id']:
        user_id = req['user_id']
        # 获取用户昵称
        nick_name = UserInfo.query.filter(UserInfo.id == user_id).first().nick_name
        res = {'status': True, 'data': {"nick_name": nick_name}}
    else:
        res = {'status': False}
    return res


@sign.route('/modifyNickname', methods=['POST'])
def modify_nick_name():
    """
    修改昵称
    :param: user_id&nick_name
    :return: data
    """
    req = parser_post(request)
    if req['user_id'] and req['nick_name']:
        # 查找用户昵称是否存在
        nick_name = UserInfo.query.filter(UserInfo.nick_name == req['nick_name']).first()
        if nick_name:
            res = {'status': False}
        else:
            # 修改昵称
            UserInfo.query.filter(UserInfo.id == int(req['user_id'])).update({'nick_name': req['nick_name']})
            db.session.commit()
            res = {'status': True}
    else:
        res = {'status': False}
    return res


@sign.route('/getAuthentication', methods=['POST'])
def get_authentication():
    """
    获取用户认证状态
    :param: user_id
    :return: data
    """
    req = parser_post(request)
    if req['nick_name']:
        nick_name = req['nick_name']
        print(nick_name)
        # 获取用户认证状态
        authentication = UserInfo.query.filter(UserInfo.nick_name == nick_name).first().authentication
        db.session.commit()
        res = {'status': True, 'data': {"authentication": authentication}}
    else:
        res = {'status': False}
    return res
