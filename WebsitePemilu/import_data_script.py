# import_data_script.py

import pandas as pd
import os
import django
from datetime import datetime

# Sesuaikan dengan nama projek Django Anda
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "WebsitePemilu.settings")
django.setup()

from Pemilu.models import DataWarga  # Ganti dengan model yang sesuai

def import_data():
<<<<<<< HEAD
    excel_file = '/home/ubuntu/belitung_timur_part2.xlsx'
=======
    excel_file = '/home/noval/Desktop/Aplikasi Pemenangan Caleg/belitung_timur_part1.xlsx'
>>>>>>> b6f5e42878e2557cd4e9066f1c60382f88e6a92d
    excel_data = pd.read_excel(excel_file)

    for index, row in excel_data.iterrows():
        formatted_date = datetime.strptime(row['TANGGAL LAHIR'], '%d-%m-%Y').strftime('%Y-%m-%d')
        
        DataWarga.objects.create(
            kabupaten = row['KABUPATEN'],
            kecamatan = row['KECAMATAN'],
            kelurahan = row['KELURAHAN'],
            nkk       = row['NKK'],
            nik       = row['NIK'],
            nama        = row['NAMA'],
            tempat_lahir = row['TEMPAT LAHIR'],
            tanggal_lahir = formatted_date,
            sts_kawin   = row['STS KAWIN'],
            kelamin     = row['KELAMIN'],
            alamat      = row['ALAMAT'],
            rt          = row['RT'],
            rw          = row['RW'],
            disabilitas = row['DISABILITAS'],
            ektp        = row['EKTP'],
            tps         = row['TPS'],
        )
    

if __name__ == "__main__":
    import_data()
