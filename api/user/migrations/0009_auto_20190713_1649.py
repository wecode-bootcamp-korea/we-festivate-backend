# Generated by Django 2.2.2 on 2019-07-13 07:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0008_auto_20190713_1621'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=100, null=True, unique=True),
        ),
    ]
