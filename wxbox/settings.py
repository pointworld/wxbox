import os, sys

from decouple import config


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))

SECRET_KEY = 'v4!kq@*%)1hh!oulk+l(tl5htv3@&_qgd-&43rwz8i&hk0g*&q'

DEBUG = True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'message',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'wxbox.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'wxbox.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

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
