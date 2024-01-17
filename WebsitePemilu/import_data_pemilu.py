import pandas as pd
import os
import django

# Sesuaikan dengan nama projek Django Anda
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "WebsitePemilu.settings")
django.setup()

from Pemilu.models import DataPemilu

def import_data():
    excel_file = '/home/noval/Desktop/Aplikasi Pemenangan Caleg/Belitung_2019.xlsx'
    excel_data = pd.read_excel(excel_file)

    for index, row in excel_data.iterrows():
        
        DataPemilu.objects.create(
            kabupaten=row['Kabupaten'],
            kecamatan=row['Kecamatan'],
            kelurahan=row['Kelurahan'],
            tps=row['TPS'],
            calon_1_2019=row['Calon_1_2019'],
            calon_2_2019=row['Calon_2_2019'],
            calon_3_2019=row['Calon_3_2019'],
            suara_Partai_2019=row['Suara_Partai_2019'],
            calon_1_2024=row['Calon_1_2024'],
            total_suara_2024=row['Total_suara_2024'],
        )
    

if __name__ == "__main__":
    import_data()
