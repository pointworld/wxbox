import requests
from django.conf import settings


def get_wx_openid(code):
    """
    获取微信用户 openid
    """

    res = requests.get(
        url=settings.WECHAT_CONFIG['get_oauth2_token_url'],
        params={
            'appid': settings.WECHAT_CONFIG['app_id'],
            'secret': settings.WECHAT_CONFIG['app_secret'],
            'code': code,
            'grant_type': 'authorization_code',
        }
    ).json()

    return res.get('openid')
