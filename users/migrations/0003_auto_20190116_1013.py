# Generated by Django 2.1.4 on 2019-01-16 02:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20190115_2217'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='name',
            field=models.CharField(default=53466, max_length=32, verbose_name='用户名'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='myuser',
            name='password',
            field=models.CharField(max_length=32, verbose_name='密码'),
        ),
    ]
