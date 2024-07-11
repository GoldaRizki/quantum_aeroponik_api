#from django.shortcuts import render
# rasah nggowo kuwi, aku meh nggawe rest API tok

from rest_framework.decorators import api_view
from rest_framework.response import Response

from rest_framework.decorators import parser_classes
from service_api.textParser import PlainTextParser


from service_api.models import Pengukuran
from service_api.models import Konfigurasi

import json
from datetime import datetime

from qiskit import QuantumCircuit, result
from qiskit.primitives import Sampler
from qiskit_aer import Aer


# Create your views here.


# Menyimpan data dari sensor ke dalam database 
@api_view(['POST'])
@parser_classes([PlainTextParser])
def baca_sensor(request):

    # Data dari request masih berupa plain text
    body_request = request.data 

    # Convert dulu menjadi binary
    data_mentah = ""

    for r in body_request:
        data_mentah += format(ord(r), '08b')



    # Dilakukan quantum encryption menggunakan protokol BB84

    simulator = Aer.get_backend('aer_simulator')

    cipher_text = ""

    for q in data_mentah:

        rangkaian = QuantumCircuit(1, 1)

        if q == '0':
            rangkaian.h(0)
            rangkaian.h(0)

        else:
            rangkaian.x(0)
            rangkaian.h(0)
            rangkaian.h(0)

        rangkaian.measure(0,0)
    

        hasil = simulator.run(rangkaian, shots=100).result()
        #print(hasil.get_counts())

        pengukuran = hasil.get_counts()

        if pengukuran.get('0') == 100:
            cipher_text += "0"
        elif pengukuran.get('1') == 100:
            cipher_text += "1"
        else:
            return Response({'error' : 'Data quantum tidak konsisten, kemungkinan disadap'})



    # Convert kembali menjadi string

    string_awal = ""
    for i in range(0, len(cipher_text), 8):
        angka = int(cipher_text[i:i+8], 2)
        string_awal += chr(angka)


    # Dekripsi dari classical encryption method (Vigenere)
    kunci = "wota konservatif"
    kunci_index = 0
    panjang_kunci = len(kunci)
    plain_text = ""
    for i in string_awal:
        nilai_ascii = ord(i)
        nilai_kunci = ord(kunci[kunci_index])
        nilai_karakter = (nilai_ascii - nilai_kunci)%128
        plain_text += chr(nilai_karakter)
        kunci_index += 1
        if(kunci_index == panjang_kunci):
            kunci_index = 0

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

    return Response(konfigurasi)



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