# Generated by Django 2.2.2 on 2019-07-04 09:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20190704_1401'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='pw',
            new_name='password',
        ),
    ]
