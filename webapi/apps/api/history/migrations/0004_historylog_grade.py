# Generated by Django 3.2.9 on 2022-01-13 19:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('history', '0003_auto_20211129_2036'),
    ]

    operations = [
        migrations.AddField(
            model_name='historylog',
            name='grade',
            field=models.CharField(default='9', max_length=1),
        ),
    ]
