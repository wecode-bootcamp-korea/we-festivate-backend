# Generated by Django 2.2.2 on 2019-07-04 02:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0005_eventpost_building_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventpost',
            name='building_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='event.Building'),
        ),
    ]
