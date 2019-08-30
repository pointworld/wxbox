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
