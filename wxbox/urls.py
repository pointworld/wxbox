from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from message import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', views.index),
] + static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
