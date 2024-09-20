from django.db import models

# Create your models here.
class Pengukuran(models.Model):
    suhu_dalam = models.FloatField()
    kelembapan_dalam = models.FloatField()
    tangki_air = models.BooleanField()
    waktu_pengukuran = models.DateTimeField(auto_now_add=True)



class Konfigurasi(models.Model):
    nama_konfigurasi = models.CharField(max_length=30)
    nilai = models.FloatField()
