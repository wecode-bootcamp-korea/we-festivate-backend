# Generated by Django 2.2.2 on 2019-07-12 13:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_auto_20190704_1811'),
        ('event', '0022_auto_20190712_1844'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='EventCommemts',
            new_name='EventCommemt',
        ),
        migrations.AlterModelTable(
            name='eventcommemt',
            table='event_commemt',
        ),
    ]
