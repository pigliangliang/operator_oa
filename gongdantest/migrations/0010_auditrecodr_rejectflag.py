# Generated by Django 2.1.4 on 2019-01-17 09:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gongdantest', '0009_usercase_ctime'),
    ]

    operations = [
        migrations.AddField(
            model_name='auditrecodr',
            name='rejectflag',
            field=models.IntegerField(default=0, verbose_name='是否驳回'),
        ),
    ]
