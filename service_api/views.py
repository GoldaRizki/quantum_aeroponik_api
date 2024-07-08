#from django.shortcuts import render
# rasah nggowo kuwi, aku meh nggawe rest API tok

from rest_framework.decorators import api_view
from rest_framework.response import Response

from rest_framework.decorators import parser_classes
from .textParser import PlainTextParser

import json

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
    cipher_text = ""

    for r in body_request:
        cipher_text += format(ord(r), '08b')



    # Dilakukan quantum encryption menggunakan protokol BB84
    rangkaian = QuantumCircuit(1, 1)
    rangkaian.h(0)
    rangkaian.h(0)
    rangkaian.measure(0,0)

    """ 
    simulator = Sampler()
    hasil = simulator.run(rangkaian, shots=100)
    print(hasil)
    """

    simulator = Aer.get_backend('aer_simulator')
    hasil = simulator.run(rangkaian, shots=100).result()
    #print(hasil.get_counts())

    pengukuran = hasil.get_counts()

    if(pengukuran['0'] == 100 or pengukuran['1'] == 100):
        
        # Convert kembali menjadi string
        string_awal = ""
        for i in range(0, len(cipher_text), 8):
            angka = int(cipher_text[i:i+8], 2)
            string_awal += chr(angka)


        # Dekripsi dari classical encryption method (Beaufort)
        kunci = "wota"
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

        dictionary = json.loads(plain_text)
        print(ascii(plain_text))
        return Response(plain_text)

    
    #return Response(body_request)
    return Response({'error' : 'Data quantum tidak konsisten, kemungkinan disadap'})