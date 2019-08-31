# Django —— 微信推送消息

参考：https://github.com/hyyc554/wxbox

## 前言

微信公众号的分类

  - 订阅号

  - 服务号

  - 企业号

基于：微信认证服务号 主动推送消息给微信
前提：关注服务号
环境：沙箱环境

沙箱环境地址： https://mp.weixin.qq.com/debug/cgi-bin/sandbox?t=sandbox/login


## 流程（以沙箱环境为例）

### 注册开发者测试账号（微信公众平台）

- 打开该链接 [沙箱环境](https://mp.weixin.qq.com/debug/cgi-bin/sandbox?t=sandbox/login)
  
- 微信扫码并登录

- 注册成功后会得到：

  - appID 和 appsecret
    - 可用于获取 access_token 
  
  - 测试号二维码
    - 用于给用户扫码关注
    - 用户扫码关注后，可以获取到该用户的微信号（openid，非用户真实的微信号）

### 配置相关参数
  
#### 接口信息配置（URL 和 Token）

- 配置
    
  - URL：可以是域名或 IP + 端口
    
  - Token：用于生成签名，微信服务器用来识别网站服务器
  
- 验证服务器地址的有效性

  - 概述

    - 填写的 URL 需要正确响应微信发送的 Token 验证
    
    - 开发者必须自架服务器，当填写的 URL 提交后，微信服务器会发送 GET 请求（携带四个参数）到开发者的服务器，开发者的服务器返回其中 echostr 参数的值则表示验证成功
    
    - 四个参数
    
      - signature：加密的签名
      
      - timestamp：时间戳
      
      - nonce：随机数
      
      - echostr：随机字符串
      
  - 校验流程
  
    - 将 token、timestamp、nonce 三个参数进行字典序排序
    
    - 将三个参数字符串拼接成一个字符串后，进行 sha1 加密
    
    - 将加密后的字符串与 signature 对比，如果相同返回 echostr，表示验证成功
    
  - 使用第三方包校验
  
    - wechatpy(https://github.com/jxtech/wechatpy)

#### 配置模版消息接口

- 用于定制发送给用户的消息模版

- 会为配置的每一个模版自动生成一个 template_id

#### 配置接口权限
  
- 对话服务

- 功能服务

- 网页服务

  - 网页账号    
    
    - 授权回调页面域名  
    
      - 网页授权可以获取用户基本信息
    
      - 用户在网页授权页统一授权给公众号后，微信会将授权数据传给一个回调页面
      
      - 回调页面需在此域名下，以确保安全可靠
  
  - ...

### 引导用户关注公众号（已认证的服务号）

### 引导用户授权微信信息（生成二维码，让用户扫描）

- 该二维码本质上是一个 URL：`https://open.weixin.qq.com/connect/oauth2/authorize?appid={appid}&redirect_uri={redirect_uri}&response_type=code&scope=snsapi_userinfo&state={state}#wechat_redirect`

- 用户通过微信扫码该 URL 后，会提示用户是否允许该公众号访问自己的信息

- 获取用户 openid

- 入库

### 发送消息（模版消息）

- openid

- access_token（2 小时有效期）


## 通过 requests 模块简单实现微信推送消息

```python
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
```

## 通过 Django 实现微信推送消息（核心代码）

### urls.py
```python
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from message import views

urlpatterns = [
    path('admin/', admin.site.urls),
    # 首页
    path('index/', views.IndexView.as_view()),
    # 登录
    path('login/', views.UserLoginView.as_view()),
    # 绑定：用户登录后，引导其关注公众号，并绑定个人微信（用于以后消息推送）
    path('bind/', views.UserBindWeChatView.as_view()),
    # 生成二维码，访问获取用户基本信息
    path('bind_qcode/', views.UserAuthWeChatView.as_view()),
    # 用于协助微信服务器验证网站服务器地址的有效性
    path('wechat_verify/', views.wechat_verify),
    # 用户授权回调
    path('callback/', views.CallbackView.as_view()),
] + static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
```

### models.py

```python
import hashlib

from django.db import models


class UserInfo(models.Model):
    name = models.CharField(max_length=32, unique=True, verbose_name='用户名')
    pwd = models.CharField(max_length=64, verbose_name='密码')
    wx_id = models.CharField(max_length=32, null=True, blank=True, verbose_name='微信 ID')
    uid = models.CharField(max_length=64, unique=True, verbose_name='用户唯一 ID')

    def save(self, *args, **kwargs):
        # 创建用户时，为用户自动生成个人唯一 ID
        if not self.pk:
            m = hashlib.md5()
            m.update(self.name.encode(encoding='utf-8'))
            self.uid = m.hexdigest()
        super().save(*args, **kwargs)
```

### settings.py

```python
from decouple import config

WECHAT_CONFIG = {
    # app ID
    'app_id': config('WX_APP_ID'),
    # app 密钥
    'app_secret': config('WX_APP_SECRET'),
    # 微信 Token：用于生成签名，微信服务器用来验证网站服务器地址
    'token': config('WX_TOKEN'),
    # 消息模版 id
    'template_id': config('WX_TEMPLATE_ID'),
    # 消息接收者 id
    'wx_id': config('WX_ID'),
    # 回调 URL
    'redirect_uri': config('WX_REDIRECT_URI'),
    # 获取访问 cgi token 的 URL
    'get_cgi_token_url': 'https://api.weixin.qq.com/cgi-bin/token',
    # 获取访问 oauth2 token 的 URL
    'get_oauth2_token_url': 'https://api.weixin.qq.com/sns/oauth2/access_token',
    # 发送普通消息的 URL
    'post_custom_msg_url': 'https://api.weixin.qq.com/cgi-bin/message/custom/send',
    # 发送模版消息的 URL
    'post_template_msg_url': 'https://api.weixin.qq.com/cgi-bin/message/template/send',
}
```

```.env
# 微信消息接收者 id
WX_ID=xxx

# 微信 Token：用于生成签名，微信服务器用来验证网站服务器地址
WX_TOKEN=xxx

# 微信消息模版 id
WX_TEMPLATE_ID=xxx

# 微信 app ID
WX_APP_ID=xxx

# 微信 app 密钥
WX_APP_SECRET=xxx

# 微信回调 URL
WX_REDIRECT_URI=xxx
```

### views.py

```python
from django.views import View
from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from message import models
from .utils import get_wx_openid


@csrf_exempt
def wechat_verify(request):
    """
    协助微信后台验证网站服务器地址的有效性
    :param request:
    :return:
    """

    from wechatpy.utils import check_signature
    from wechatpy.exceptions import InvalidSignatureException

    try:
        check_signature(
            token=settings.WECHAT_CONFIG['token'],
            signature=request.GET.get('signature'),
            timestamp=request.GET.get('timestamp'),
            nonce=request.GET.get('nonce'),
        )
        # 返回请求中的回复信息
        return HttpResponse(request.GET.get('echostr', None))
    except InvalidSignatureException as e:
        return HttpResponse(status=403)


class IndexView(View):
    """
    首页
    """
    def get(self, request):
        obj = models.UserInfo.objects.get(id=1)
        return render(request, 'index.html', {'obj': obj})


class UserLoginView(View):
    """
    用户登录
    """

    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        """
        用户登录
        登录成功后重定向到 /bind/ 路由下，引导用户关注微信公众号并授权
        :param request:
        :return:
        """

        # models.UserInfo.objects.create(name='point', pwd=123)

        user = request.POST.get('user')
        pwd = request.POST.get('pwd')

        obj = models.UserInfo.objects.filter(name=user, pwd=pwd).first()
        if obj:
            request.session['user_info'] = {'id': obj.id, 'name': obj.name, 'uid': obj.uid}
            return redirect('/bind/')
        else:
            return render(request, 'login.html')


class UserBindWeChatView(View):
    """
    用户引导用户关注公众号：
    用户登录后，引导其扫码关注公众号，并授权个人微信（用于以后消息推送）
    """

    def get(self, request):
        return render(request, 'bind.html')


class UserAuthWeChatView(View):
    """
    用户微信授权：
    当用户通过微信扫描由 access_url 生成的二维码时，会提示用户是否
    授权公众号访问自己的基本信息
    """

    def get(self, request):
        ret = {'code': 1000}

        try:
            access_url = 'https://open.weixin.qq.com/connect/oauth2/authorize?appid={appid}&redirect_uri={redirect_uri}&response_type=code&scope=snsapi_userinfo&state={state}#wechat_redirect'
            url = access_url.format(
                appid=settings.WECHAT_CONFIG['app_id'],
                redirect_uri=settings.WECHAT_CONFIG['redirect_uri'],
                state=request.session['user_info']['uid']
            )
            ret['data'] = url
        except Exception as e:
            ret['code'] = 1001
            ret['msg'] = str(e)

        return JsonResponse(ret)


class CallbackView(View):
    """
    回调
    """

    def get(self, request):
        """
        用户扫码授权后，微信自动调用该方法
        用于获取授权用户的唯一 ID，入库，以后用于推送消息
        :param request:
        :return:
        """
        code = request.GET.get('code')
        state = request.GET.get('state')

        openid = get_wx_openid(code)

        if openid:
            models.UserInfo.objects.filter(uid=state).update(wx_id=openid)
            response = '<h1>授权成功 %s </h1>' % openid
        else:
            response = '<h1>用户扫码之后，手机上的提示</h1>'

        return HttpResponse(response)

    def post(self, request):
        pass


class TestSendMsgView:
    def send_custom_msg(self):
        """
        发送普通消息
        :return:
        """
        pass

    def send_template_msg(self):
        """
        发送模版消息
        :return:
        """
        pass
```

utils.py
```python
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
```
