# Generated by Django 2.2.2 on 2019-07-12 00:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0020_auto_20190712_0917'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventreply',
            name='user_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='user.User', to_field='user_id'),
        ),
    ]
