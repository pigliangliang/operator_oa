# Generated by Django 2.1.4 on 2019-01-16 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gongdantest', '0005_auto_20190116_1713'),
    ]

    operations = [
        migrations.AddField(
            model_name='usercase',
            name='workflowid',
            field=models.IntegerField(default=1, verbose_name='所属工作流'),
        ),
    ]
