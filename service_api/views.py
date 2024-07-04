#from django.shortcuts import render
# rasah nggowo kuwi, aku meh nggawe rest API tok

from rest_framework.decorators import api_view
from rest_framework.response import Response

from rest_framework.decorators import parser_classes
from .textParser import PlainTextParser

import json

from qiskit import QuantumCircuit
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
    rangkaian = QuantumCircuit(1)
    rangkaian.h(0)
    rangkaian.h(0)

    """ 
    simulator = Sampler()
    hasil = simulator.run(rangkaian, shots=100)
    print(hasil)
    """

    simulator = Aer.get_backend('aer_simulator')
    hasil = simulator.run(rangkaian, shots=100).result()
    print(hasil.sample_counts)


    # Convert kembali menjadi string
    string_awal = ""
    for i in range(0, len(cipher_text), 8):
        angka = int(cipher_text[i:i+8], 2)
        string_awal += chr(angka)
    #dictionary = json.loads(body_request)

    # Dekripsi dari classical encryption method 

    
    # Dimasukkan kedalam database lewat model dulu

    

    return Response(string_awal)