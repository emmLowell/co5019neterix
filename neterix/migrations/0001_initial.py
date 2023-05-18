# Generated by Django 4.2.1 on 2023-05-17 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cve',
            fields=[
                ('cve_id', models.IntegerField(primary_key=True, serialize=False)),
                ('cve', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Ip',
            fields=[
                ('ip_id', models.IntegerField(primary_key=True, serialize=False)),
                ('ip_address', models.CharField(max_length=15)),
                ('alias', models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='Ip_cve',
            fields=[
                ('scan_id', models.IntegerField(primary_key=True, serialize=False)),
                ('ip_id', models.IntegerField(unique=True)),
                ('cve_id', models.IntegerField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Ip_port',
            fields=[
                ('scan_id', models.IntegerField(primary_key=True, serialize=False)),
                ('ip_id', models.IntegerField(unique=True)),
                ('port_id', models.IntegerField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Port',
            fields=[
                ('port_id', models.IntegerField(primary_key=True, serialize=False)),
                ('port_number', models.IntegerField()),
                ('service', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Scan',
            fields=[
                ('scan_id', models.IntegerField(primary_key=True, serialize=False)),
                ('scan_type', models.CharField(max_length=30)),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('os', models.CharField(max_length=10)),
                ('ip_id', models.IntegerField()),
            ],
        ),
    ]
