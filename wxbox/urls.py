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
