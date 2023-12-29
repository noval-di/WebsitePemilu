from django import template
from Pemilu.models import DataWarga  # Sesuaikan dengan nama aplikasi dan model Anda

register = template.Library()

@register.filter
def jumlah_kecamatan(kabupaten):
    # Hitung jumlah kecamatan berdasarkan nama kabupaten
    return DataWarga.objects.filter(kabupaten=kabupaten).values('kecamatan').distinct().count()
