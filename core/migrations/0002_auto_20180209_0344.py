# Generated by Django 2.0.2 on 2018-02-09 03:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('system', models.CharField(max_length=128)),
                ('x', models.FloatField(null=True)),
                ('y', models.FloatField(null=True)),
                ('z', models.FloatField(null=True)),
                ('body', models.CharField(blank=True, max_length=64, null=True)),
                ('gravity', models.FloatField(blank=True, null=True)),
                ('site_name', models.CharField(blank=True, max_length=128, null=True)),
                ('lat', models.FloatField(blank=True, null=True)),
                ('lon', models.FloatField(blank=True, null=True)),
                ('edsm_id', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Ship',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model', models.CharField(choices=[('adder', 'Adder'), ('conda', 'Anaconda'), ('aspx', 'Asp Explorer'), ('asps', 'Asp Scout'), ('beluga', 'Beluga Liner'), ('chieftain', 'Chieftain'), ('cobra3', 'Cobra Mk III'), ('cobra4', 'Cobra Mk IV'), ('dbx', 'Diamondback Explorer'), ('dbs', 'Diamondback Scout'), ('dolphin', 'Dolphin'), ('eagle', 'Eagle Mk II'), ('fas', 'Federal Assault Ship'), ('corvette', 'Federal Corvette'), ('dropship', 'Federal Dropship'), ('gunship', 'Federal Gunship'), ('fdl', 'Fer-De-Lance'), ('hauler', 'Hauler'), ('clipper', 'Imperial Clipper'), ('courier', 'Imperial Courier'), ('cutter', 'Imperial Cutter'), ('ieagle', 'Imperial Eagle'), ('keelback', 'Keelback'), ('krait', 'Krait'), ('orca', 'Orca'), ('python', 'Python'), ('sidewinder', 'Sidewinder Mk I'), ('t10', 'Type-10 Defender'), ('t6', 'Type-6 Transporter'), ('t7', 'Type-7 Transporter'), ('t9', 'Type-9 Heavy'), ('viper3', 'Viper Mk III'), ('viper4', 'Viper Mk IV'), ('vulture', 'Vulture')], max_length=16, verbose_name='ship model')),
                ('name', models.CharField(blank=True, max_length=24, null=True, verbose_name='ship name')),
                ('range', models.FloatField(verbose_name='jump range')),
                ('livery', models.CharField(max_length=48, verbose_name='ship livery')),
                ('call_sign', models.CharField(max_length=8, verbose_name='call sign')),
            ],
        ),
        migrations.CreateModel(
            name='Waypoint',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=128)),
                ('arrival_date', models.DateField()),
                ('base_camp', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.Location')),
            ],
        ),
        migrations.AddField(
            model_name='commander',
            name='comms_id',
            field=models.CharField(max_length=15, null=True, verbose_name='comms nickname'),
        ),
        migrations.AddField(
            model_name='commander',
            name='dwe_veteran',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='commander',
            name='platform',
            field=models.CharField(default='PC', max_length=8),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='commander',
            name='primary_role',
            field=models.CharField(default='Photographer', max_length=24),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='commander',
            name='secondary_role',
            field=models.CharField(max_length=24, null=True),
        ),
        migrations.AddField(
            model_name='commander',
            name='timezone',
            field=models.CharField(default='UTC', max_length=8),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='commander',
            name='visited_beagle_point',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='commander',
            name='ship',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.Ship'),
        ),
    ]
