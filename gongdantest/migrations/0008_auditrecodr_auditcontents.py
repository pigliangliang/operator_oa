# Generated by Django 2.1.4 on 2019-01-17 06:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gongdantest', '0007_auditrecodr_current'),
    ]

    operations = [
        migrations.AddField(
            model_name='auditrecodr',
            name='auditcontents',
            field=models.CharField(default='同意申请', max_length=300, verbose_name='审核意见'),
        ),
    ]