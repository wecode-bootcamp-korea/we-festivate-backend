# Generated by Django 2.2.2 on 2019-07-13 04:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0029_auto_20190713_1321'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventcomment',
            name='created_at',
            field=models.CharField(max_length=30),
        ),
    ]
