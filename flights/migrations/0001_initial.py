# Generated by Django 3.1.2 on 2024-12-13 15:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=64, null=True)),
                ('airport', models.CharField(max_length=64, null=True)),
                ('code', models.CharField(max_length=3, null=True)),
                ('country', models.CharField(max_length=64, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Week',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(unique=True)),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Flight',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('depart_time', models.TimeField(null=True)),
                ('duration', models.DurationField(null=True)),
                ('arrival_time', models.TimeField(null=True)),
                ('plane', models.CharField(max_length=24, null=True)),
                ('airline', models.CharField(max_length=64, null=True)),
                ('economy_fare', models.FloatField(null=True)),
                ('business_fare', models.FloatField(null=True)),
                ('first_fare', models.FloatField(null=True)),
                ('depart_day', models.ManyToManyField(related_name='flights_of_the_day', to='flights.Week')),
                ('destination', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='arrivals', to='flights.place')),
                ('origin', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='departures', to='flights.place')),
            ],
        ),
    ]
