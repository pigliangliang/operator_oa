from django.db import models

from django.contrib.auth.models import AbstractUser


# Create your models here.

class Department(models.Model):
    name = models.CharField('部门名称', max_length=32)
    leader = models.CharField('部门领导', max_length=32)

    class Meta:
        verbose_name = '部门'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class MyUser(AbstractUser):

    department = models.ForeignKey(Department, verbose_name='所属部门', on_delete=models.CASCADE, default=True, null=True)

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username