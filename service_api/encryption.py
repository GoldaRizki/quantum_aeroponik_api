from qiskit import QuantumCircuit, result
from qiskit.primitives import Sampler
from qiskit_aer import Aer

class Vigenere:

  def dekripsi(self, kunci, cipher_text):
    kunci_index = 0
    panjang_kunci = len(kunci)
    plain_text = ""
    for i in cipher_text:
        nilai_ascii = ord(i)
        nilai_kunci = ord(kunci[kunci_index])
        nilai_karakter = (nilai_ascii - nilai_kunci)%128
        if nilai_karakter < 0 : nilai_karakter += 128 
        plain_text += chr(nilai_karakter)
        kunci_index += 1
        if(kunci_index == panjang_kunci):
            kunci_index = 0

    return plain_text


  def enkripsi(self, kunci, plain_text):
    kunci_index = 0
    panjang_kunci = len(kunci)
    cipher_text = ""
    for i in plain_text:
        nilai_ascii = ord(i)
        nilai_kunci = ord(kunci[kunci_index])
        nilai_karakter = (nilai_ascii + nilai_kunci)%128
        if nilai_karakter < 0 : nilai_karakter += 128 
        cipher_text += chr(nilai_karakter)
        kunci_index += 1
        if(kunci_index == panjang_kunci):
            kunci_index = 0

    return cipher_text


class ProtokolBB84:

    def enkripsi(self, data_input):

        # Convert dulu menjadi binary
        string_biner = ""

        for r in data_input:
            string_biner += format(ord(r), '08b')


        # Dilakukan quantum encryption menggunakan protokol BB84

        simulator = Aer.get_backend('aer_simulator')

        data_hasil = ""

        for q in string_biner:

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
                data_hasil += "0"
            elif pengukuran.get('1') == 100:
                data_hasil += "1"
            else:
                return Response({'error' : 'Data quantum tidak konsisten, kemungkinan disadap'})


        # Convert kembali menjadi string

        string_awal = ""
        for i in range(0, len(data_hasil), 8):
            angka = int(data_hasil[i:i+8], 2)
            string_awal += chr(angka)
        
        return string_awal