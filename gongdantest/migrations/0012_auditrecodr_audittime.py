# Generated by Django 2.1.4 on 2019-01-18 01:32

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gongdantest', '0011_usercase_rejectflag'),
    ]

    operations = [
        migrations.AddField(
            model_name='auditrecodr',
            name='audittime',
            field=models.DateTimeField(default=datetime.datetime.now, verbose_name='审批时间'),
        ),
    ]
