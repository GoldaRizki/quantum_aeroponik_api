#from django.shortcuts import render
# rasah nggowo kuwi, aku meh nggawe rest API tok

from rest_framework.decorators import api_view
from rest_framework.response import Response

from rest_framework.decorators import parser_classes
from .textParser import PlainTextParser

import json
import binascii



# Create your views here.

@api_view(['POST'])
@parser_classes([PlainTextParser])
def baca_sensor(request):

    # Data dari request masih berupa plain text
    body_request = request.data 

    # Convert dulu menjadi binary
    cipher_text = binascii.hexlify(body_request.encode())

    #dictionary = json.loads(body_request)



    print(cipher_text)

    return Response(cipher_text)