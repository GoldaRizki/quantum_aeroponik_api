#from django.shortcuts import render
# rasah nggowo kuwi, aku meh nggawe rest API tok

from rest_framework.decorators import api_view
from rest_framework.response import Response

from rest_framework.decorators import parser_classes
from service_api.textParser import PlainTextParser
from service_api.encryption import Vigenere
from service_api.encryption import ProtokolBB84


from service_api.models import Pengukuran
from service_api.models import Konfigurasi

import json
from datetime import datetime


# Create your views here.

vigenere = Vigenere()
protokol_bb84 = ProtokolBB84()

# Menyimpan data dari sensor ke dalam database 
@api_view(['POST'])
@parser_classes([PlainTextParser])
def baca_sensor(request):

    # Data dari request masih berupa plain text
    body_request = request.data 

    # Dilakukan quantum encryption menggunakan protokol BB84
    classical_cipher = protokol_bb84.enkripsi(body_request)


    # Dekripsi dari classical encryption method (Vigenere)
    kunci = "wota konservatif"

    plain_text = vigenere.dekripsi(kunci, classical_cipher)

    # Dimasukkan kedalam database lewat model dulu
    data = json.loads(plain_text)


    pengukuran = Pengukuran(
        suhu_dalam = data['suhu_dalam'],
        kelembapan_dalam = data['humidity_dalam'],
        suhu_luar = data['suhu_luar'],
        kelembapan_luar = data['humidity_luar'],
        tangki_air = data['tangki_air']
    )

    pengukuran.save()


    return Response()
    


@api_view(['GET'])
def baca_konfigurasi(request):
    
    konfigurasi = Konfigurasi.objects.all().values()

    data = {
        "max_humidity" : konfigurasi[0]["nilai"],
        "min_humidity" : konfigurasi[1]["nilai"],
        "max_suhu" : konfigurasi[2]["nilai"],
        "min_suhu" : konfigurasi[3]["nilai"]
    }
    

    return Response(data)



@api_view(['POST'])
def set_konfigurasi(request):
    
    body_request = request.data

    konfigurasi = Konfigurasi.objects

    #setting konfigurasi

    max_humidity = konfigurasi.get(nama_konfigurasi = "max_humidity")
    max_humidity.nilai = body_request['max_humidity']
    max_humidity.save()
    
    min_humidity = konfigurasi.get(nama_konfigurasi = "min_humidity")
    min_humidity.nilai = body_request['min_humidity']
    min_humidity.save()
    
    max_suhu = konfigurasi.get(nama_konfigurasi = "max_suhu")
    max_suhu.nilai = body_request['max_suhu']
    max_suhu.save()
    
    min_suhu = konfigurasi.get(nama_konfigurasi = "min_suhu")
    min_suhu.nilai = body_request['min_suhu']
    min_suhu.save()

    
    return Response(konfigurasi.all().values())



@api_view(['GET'])
def data_terakhir(request):
    
    pengukuran = Pengukuran.objects.order_by('waktu_pengukuran').last()

    data = {
        "suhu_dalam": pengukuran.suhu_dalam,
        "suhu_luar": pengukuran.suhu_luar,
        "kelembapan_dalam": pengukuran.kelembapan_dalam,
        "kelembapan_luar": pengukuran.kelembapan_luar,
        "tangki_air": pengukuran.tangki_air,
        "waktu_pengukuran": pengukuran.waktu_pengukuran
    }

    return Response(data)

@api_view(['GET'])
def data_sehari(request):
    
    hari_ini = datetime.today()

    pengukuran = Pengukuran.objects.filter(waktu_pengukuran__day = hari_ini.day, waktu_pengukuran__month = hari_ini.month, waktu_pengukuran__year = hari_ini.year)

    
    return Response(pengukuran.values("suhu_dalam", "suhu_luar", "kelembapan_luar", "kelembapan_dalam", "tangki_air", "waktu_pengukuran"))