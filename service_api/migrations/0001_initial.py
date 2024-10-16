# Generated by Django 5.0.6 on 2024-09-20 21:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Konfigurasi',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama_konfigurasi', models.CharField(max_length=30)),
                ('nilai', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Pengukuran',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('suhu_dalam', models.FloatField()),
                ('kelembapan_dalam', models.FloatField()),
                ('tangki_air', models.BooleanField()),
                ('waktu_pengukuran', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
