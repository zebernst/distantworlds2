# Generated by Django 2.0.2 on 2018-03-21 22:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_auto_20180321_2222'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commander',
            name='application_num',
            field=models.PositiveIntegerField(primary_key=True, serialize=False, verbose_name='App. #'),
        ),
    ]
