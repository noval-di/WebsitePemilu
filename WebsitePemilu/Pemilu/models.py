from django.db import models
from django.core.exceptions import ValidationError
# Create your models here.

# Tabel sebagai baseline data warga
class DataWarga(models.Model):
    # Informasi wilayah
    kabupaten = models.CharField(max_length=255)
    kecamatan = models.CharField(max_length=255)
    kelurahan = models.CharField(max_length=255)

    # Detail warga
    nkk = models.BigIntegerField()
    nik = models.BigIntegerField()
    nama = models.CharField(max_length=255)
    tempat_lahir = models.CharField(max_length=255)
    tanggal_lahir = models.DateField()
    sts_kawin = models.CharField(max_length=20)
    kelamin = models.CharField(max_length=1)
    alamat = models.CharField(max_length=255)
    rt = models.IntegerField()
    rw = models.IntegerField()
    disabilitas = models.IntegerField()
    ektp = models.CharField(max_length=255)
    tps = models.IntegerField()

    def __str__(self):
        return self.nama

# Tabel Koordinator
class DataKoordinator(models.Model):
    # Informasi wilayah kerja koordinator
    kabupaten = models.CharField('Kabupaten',max_length=255)
    kecamatan = models.CharField('Kecamatan',max_length=255)
    kelurahan = models.CharField('Kelurahan',max_length=255)

    # Detail koordinator
    nkk = models.BigIntegerField('NKK')
    nik = models.BigIntegerField('NIK')
    nama = models.CharField('Nama',max_length=255)
    tempat_lahir = models.CharField('Tempat Lahir',max_length=255)
    tanggal_lahir = models.DateField('Tanggal Lahir')
    sts_kawin = models.CharField('Status Kawin',max_length=20)
    kelamin = models.CharField('Jenis Kelamin',max_length=1)
    alamat = models.CharField('Alamat',max_length=255)
    rt = models.IntegerField('RT')
    rw = models.IntegerField('RW')
    disabilitas = models.IntegerField('Disabilitas')
    ektp = models.CharField('EKTP',max_length=255)
    tps = models.IntegerField('TPS')
    
    # Informasi tambahan koordinator
    tingkat_kerja_choices = [
        ('kabupaten', 'Kabupaten'),
        ('kecamatan', 'Kecamatan'),
        ('kelurahan', 'Kelurahan'),
        ('tps', 'TPS'),
        ('belum_ditentukan', 'Belum Ditentukan'),
    ]
    tingkat_kerja = models.CharField('Tingkat Kerja', max_length=20, choices=tingkat_kerja_choices, default='belum_ditentukan')

    kabupaten_bertugas = models.CharField('Kabupaten Bertugas',max_length=255, blank=True, null=True)
    kecamatan_bertugas = models.CharField('Kecamatan Bertugas',max_length=255, blank=True, null=True)
    kelurahan_bertugas = models.CharField('Kelurahan Bertugas',max_length=255, blank=True, null=True)
    tps_bertugas = models.IntegerField('TPS Bertugas',blank=True, null=True)

    
    foto_ktp = models.ImageField('Foto KTP', upload_to='foto_ktp/')
    jumlah_rekrutan = models.IntegerField('Jumlah Rekrutan',default=0)
    no_hp = models.IntegerField('No HP')

    def clean(self):
        if self.tingkat_kerja == 'kabupaten':
            if self.kecamatan_bertugas or self.kelurahan_bertugas or self.tps_bertugas:
                raise ValidationError("Koordinator tingkat kabupaten hanya boleh memiliki kabupaten_bertugas yang diisi.")
        elif self.tingkat_kerja == 'kecamatan':
            if not self.kabupaten_bertugas or not self.kecamatan_bertugas:
                raise ValidationError("Koordinator tingkat kecamatan harus memiliki kabupaten_bertugas dan kecamatan_bertugas yang diisi.")
            if self.kelurahan_bertugas or self.tps_bertugas:
                raise ValidationError("Koordinator tingkat kecamatan tidak boleh memiliki kelurahan_bertugas atau tps_bertugas.")
        elif self.tingkat_kerja == 'kelurahan':
            if not all([self.kabupaten_bertugas, self.kecamatan_bertugas, self.kelurahan_bertugas]):
                raise ValidationError("Koordinator tingkat kelurahan harus memiliki semua field wilayah bertugas yang diisi.")
            if self.tps_bertugas:
                raise ValidationError("Koordinator tingkat kelurahan tidak boleh memiliki tps_bertugas.")
        elif self.tingkat_kerja == 'tps':
            if not all([self.kabupaten_bertugas, self.kecamatan_bertugas, self.kelurahan_bertugas, self.tps_bertugas]):
                raise ValidationError("Koordinator tingkat TPS harus memiliki semua field wilayah bertugas dan tps_bertugas yang diisi.")
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.nama} - ID: {self.id}"

# Tabel Daftar Pemilih
class DataPemilih(models.Model):
     # Informasi wilayah  pemilih
    kabupaten = models.CharField('Kabupaten',max_length=255, blank=True, null=True)
    kecamatan = models.CharField('Kecamatan',max_length=255, blank=True, null=True)
    kelurahan = models.CharField('Kelurahan',max_length=255, blank=True, null=True)

    # Detail pemilih
    nkk = models.BigIntegerField('NKK',blank=True, null=True)
    nik = models.BigIntegerField('NIK',blank=True, null=True)
    nama = models.CharField('Nama',max_length=255, blank=True, null=True)
    tempat_lahir = models.CharField('Tempat Lahir',max_length=255, blank=True, null=True)
    tanggal_lahir = models.DateField('Tanggal Lahir',blank=True, null=True)
    sts_kawin = models.CharField('Status Kawin',max_length=20, blank=True, null=True)
    kelamin = models.CharField('Jenis Kelamin',max_length=1, blank=True, null=True)
    alamat = models.CharField('Alamat',max_length=255, blank=True, null=True)
    rt = models.IntegerField('RT',blank=True, null=True)
    rw = models.IntegerField('RW', blank=True, null=True)
    disabilitas = models.IntegerField('Disabilitas',blank=True, null=True)
    ektp = models.CharField('EKTP',max_length=255, blank=True, null=True)
    tps = models.IntegerField('TPS',blank=True, null=True)

    # Informasi tambahan pemilih
    foto_ktp = models.ImageField('Foto Ktp',upload_to='foto_ktp/')
    koordinator = models.ForeignKey(DataKoordinator, on_delete=models.CASCADE)

    def __str__(self):
        return self.nama  # Atau gunakan informasi lain yang sesuai

from django.db import models

class PengaturanWilayah(models.Model):
    kabupaten_bangka = models.BooleanField('Kabupaten Bangka',default=False)
    kabupaten_bangka_selatan = models.BooleanField('Kabupaten Bangka Selatan',default=False)
    kabupaten_bangka_tengah = models.BooleanField('Kabupaten Bangka Tengah',default=False)
    kabupaten_bangka_barat = models.BooleanField('Kabupaten Bangka Barat',default=False)
    kota_pangkal_pinang = models.BooleanField('Kota Pangkal Pinang',default=False)
    kabupaten_belitung = models.BooleanField('Kabupaten Belitung',default=True)
    kabupaten_belitung_timur = models.BooleanField('Kabupaten Belitung Timur',default=True)
    

    # Tambahkan wilayah lain jika perlu
