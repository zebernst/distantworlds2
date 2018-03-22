# Generated by Django 2.0.2 on 2018-03-21 20:22

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20180320_1627'),
    ]

    operations = [
        migrations.RenameField(
            model_name='commander',
            old_name='ship_id',
            new_name='call_sign',
        ),
        migrations.RemoveField(
            model_name='commander',
            name='dw_patch',
        ),
        migrations.RemoveField(
            model_name='commander',
            name='validation',
        ),
        migrations.AddField(
            model_name='commander',
            name='applicant_num',
            field=models.PositiveSmallIntegerField(null=True, verbose_name='Contin. #'),
        ),
        migrations.AlterField(
            model_name='commander',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]