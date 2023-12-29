from django.contrib import admin
from Pemilu.models import DataKoordinator, DataPemilih, DataWarga
# Register your models here.
admin.site.register(DataKoordinator)
admin.site.register(DataPemilih)
admin.site.register(DataWarga)