# Generated by Django 2.2.2 on 2019-07-02 02:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_id',
            field=models.CharField(max_length=20, unique=True),
        ),
    ]
