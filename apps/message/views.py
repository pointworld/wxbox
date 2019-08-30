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
