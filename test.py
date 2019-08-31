"""
通过 requests 模块简单实现微信推送推送
"""

import json, os

import requests
import django
from django.conf import settings


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wxbox.settings')
django.setup()

CONFIG = {
    # app ID
    'app_id': settings.WECHAT_CONFIG['app_id'],
    # app 密钥
    'app_secret': settings.WECHAT_CONFIG['app_secret'],
    # 获取访问 token 的 URL
    'get_token_url': settings.WECHAT_CONFIG['get_cgi_token_url'],
    # 发送普通消息的 URL
    'post_custom_msg_url': settings.WECHAT_CONFIG['post_custom_msg_url'],
    # 发送模版消息的 URL
    'post_template_msg_url': settings.WECHAT_CONFIG['post_template_msg_url'],
    # 消息模版 id
    'template_id': settings.WECHAT_CONFIG['template_id'],
    # 消息接收者 id
    'wx_id': settings.WECHAT_CONFIG['wx_id'],
}


def get_access_token(app_id, app_secret):
    """
    伪造浏览器向 https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential...
    发送 GET 请求，并获取 token
    :param app_id: 应用 ID
    :param app_secret: 应用密钥
    :return: access_token
    """

    res = requests.get(
        url=CONFIG['get_token_url'],
        params={
            "grant_type": "client_credential",
            "appid": app_id,
            "secret": app_secret,
        }
    )

    return res.json()['access_token']

def send_custom_msg_to_user(wx_id, msg, access_token):
    """
    给指定用户发送普通消息
    :param wx_id:
    :param msg:
    :param access_token:
    :return:
    """

    body = {
        'touser': wx_id,
        'msgtype': 'text',
        'text': {
            'content': msg
        }
    }

    req = requests.post(
        url=CONFIG['post_custom_msg_url'],
        params = {
            'access_token': access_token
        },
        # 发送的消息必须是 bytes 类型
        # request，内部发送的数据是字节。默认格式为 Latin-1，它不支持中文！
        # 所以需要使用 json 序列化。如果发送的是字符串，它会使用 Latin-1 转码为 bytes，遇到中文会报错
        # 所以这里，直接强转为 bytes，那么它内部就不会转码了，直接发送！
        data=bytes(json.dumps(body, ensure_ascii=False), encoding='utf-8')
    )

    print(req.text)

def send_template_msg_to_user(wx_id, template_msg, access_token):
    body = {
        'touser': wx_id,
        'template_id': CONFIG['template_id'],
        'data': template_msg,
    }

    req = requests.post(
        url=CONFIG['post_template_msg_url'],
        params = {
            'access_token': access_token
        },
        data=bytes(json.dumps(body, ensure_ascii=False), encoding='utf-8')
    )

    print(req.text)


if __name__ == '__main__':
    # 获取 access_token
    access_token = get_access_token(app_id=CONFIG['app_id'], app_secret=CONFIG['app_secret'])
    print('access_token: ', access_token)

    # 发送普通消息
    msg = 'hello, world.'
    send_custom_msg_to_user(wx_id=CONFIG['wx_id'], msg=msg, access_token=access_token)

    # 发送模版消息
    template_msg = {
        'user': {
            'value': 'Point',
            'color': '#f00',
        }
    }
    send_template_msg_to_user(wx_id=CONFIG['wx_id'], template_msg=template_msg, access_token=access_token)
