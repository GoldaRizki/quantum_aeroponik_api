# PERHATIAN

### Cara instalasi

1. buat virtual environment dulu, kalo di windows tuliskan perintah lewat CMD kedalam direktori yg diinginkan

    >  py -m venv nama_virtual_environment

2. pindah kedalam folder virtual enviromnet 

    >  cd nama_virtual_enviromment

3. aktivasi virtual enviromnent tadi dengan perintah

    >  Scripts\activate.bat

4. clone project ini kedalam virtual environment yang sudah dibuat (pastikan sudah punya akses ke repo ini)

    >  git clone https://github.com/GoldaRizki/quantum_aeroponik_api.git

5. Kalau sudah silahkan masukkan ke dalam folder repo lewat CMD tadi

    >  cd quantum_aeroponik_api

6. Install library yang dibutuhkan dengan perintah

    >  pip install -r requirements.txt

7. Jalankan migration terlebih dahulu

    >  py manage.py migrate

8. Lakukan seeding untuk mengisi database dengan nilai awal melalui fixture

    >  py manage.py loaddata service_api\fixtures\konfigurasi_awal.json

9. Bila sudah, silahkan deploy project seperti biasa

    >  py manage.py runserver 0.0.0.0:80