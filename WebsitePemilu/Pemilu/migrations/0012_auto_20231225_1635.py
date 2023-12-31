# Generated by Django 3.2.18 on 2023-12-25 16:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Pemilu', '0011_pengaturanwilayah'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datakoordinator',
            name='alamat',
            field=models.CharField(max_length=255, verbose_name='Alamat'),
        ),
        migrations.AlterField(
            model_name='datakoordinator',
            name='disabilitas',
            field=models.IntegerField(verbose_name='Disabilitas'),
        ),
        migrations.AlterField(
            model_name='datakoordinator',
            name='ektp',
            field=models.CharField(max_length=255, verbose_name='EKTP'),
        ),
        migrations.AlterField(
            model_name='datakoordinator',
            name='foto_ktp',
            field=models.ImageField(upload_to='foto_ktp/', verbose_name='Foto KTP'),
        ),
        migrations.AlterField(
            model_name='datakoordinator',
            name='jumlah_rekrutan',
            field=models.IntegerField(default=0, verbose_name='Jumlah Rekrutan'),
        ),
        migrations.AlterField(
            model_name='datakoordinator',
            name='kabupaten',
            field=models.CharField(max_length=255, verbose_name='Kabupaten'),
        ),
        migrations.AlterField(
            model_name='datakoordinator',
            name='kabupaten_bertugas',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Kabupaten Bertugas'),
        ),
        migrations.AlterField(
            model_name='datakoordinator',
            name='kecamatan',
            field=models.CharField(max_length=255, verbose_name='Kecamatan'),
        ),
        migrations.AlterField(
            model_name='datakoordinator',
            name='kecamatan_bertugas',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Kecamatan Bertugas'),
        ),
        migrations.AlterField(
            model_name='datakoordinator',
            name='kelamin',
            field=models.CharField(max_length=1, verbose_name='Jenis Kelamin'),
        ),
        migrations.AlterField(
            model_name='datakoordinator',
            name='kelurahan',
            field=models.CharField(max_length=255, verbose_name='Kelurahan'),
        ),
        migrations.AlterField(
            model_name='datakoordinator',
            name='kelurahan_bertugas',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Kelurahan Bertugas'),
        ),
        migrations.AlterField(
            model_name='datakoordinator',
            name='nama',
            field=models.CharField(max_length=255, verbose_name='Nama'),
        ),
        migrations.AlterField(
            model_name='datakoordinator',
            name='nik',
            field=models.BigIntegerField(verbose_name='NIK'),
        ),
        migrations.AlterField(
            model_name='datakoordinator',
            name='nkk',
            field=models.BigIntegerField(verbose_name='NKK'),
        ),
        migrations.AlterField(
            model_name='datakoordinator',
            name='no_hp',
            field=models.IntegerField(verbose_name='No HP'),
        ),
        migrations.AlterField(
            model_name='datakoordinator',
            name='rt',
            field=models.IntegerField(verbose_name='RT'),
        ),
        migrations.AlterField(
            model_name='datakoordinator',
            name='rw',
            field=models.IntegerField(verbose_name='RW'),
        ),
        migrations.AlterField(
            model_name='datakoordinator',
            name='sts_kawin',
            field=models.CharField(max_length=20, verbose_name='Status Kawin'),
        ),
        migrations.AlterField(
            model_name='datakoordinator',
            name='tanggal_lahir',
            field=models.DateField(verbose_name='Tanggal Lahir'),
        ),
        migrations.AlterField(
            model_name='datakoordinator',
            name='tempat_lahir',
            field=models.CharField(max_length=255, verbose_name='Tempat Lahir'),
        ),
        migrations.AlterField(
            model_name='datakoordinator',
            name='tingkat_kerja',
            field=models.CharField(choices=[('kabupaten', 'Kabupaten'), ('kecamatan', 'Kecamatan'), ('kelurahan', 'Kelurahan'), ('tps', 'TPS'), ('belum_ditentukan', 'Belum Ditentukan')], default='belum_ditentukan', max_length=20, verbose_name='Tingkat Kerja'),
        ),
        migrations.AlterField(
            model_name='datakoordinator',
            name='tps',
            field=models.IntegerField(verbose_name='TPS'),
        ),
        migrations.AlterField(
            model_name='datakoordinator',
            name='tps_bertugas',
            field=models.IntegerField(blank=True, null=True, verbose_name='TPS Bertugas'),
        ),
        migrations.AlterField(
            model_name='datapemilih',
            name='alamat',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Alamat'),
        ),
        migrations.AlterField(
            model_name='datapemilih',
            name='disabilitas',
            field=models.IntegerField(blank=True, null=True, verbose_name='Disabilitas'),
        ),
        migrations.AlterField(
            model_name='datapemilih',
            name='ektp',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='EKTP'),
        ),
        migrations.AlterField(
            model_name='datapemilih',
            name='foto_ktp',
            field=models.ImageField(upload_to='foto_ktp/', verbose_name='Foto Ktp'),
        ),
        migrations.AlterField(
            model_name='datapemilih',
            name='kabupaten',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Kabupaten'),
        ),
        migrations.AlterField(
            model_name='datapemilih',
            name='kecamatan',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Kecamatan'),
        ),
        migrations.AlterField(
            model_name='datapemilih',
            name='kelamin',
            field=models.CharField(blank=True, max_length=1, null=True, verbose_name='Jenis Kelamin'),
        ),
        migrations.AlterField(
            model_name='datapemilih',
            name='kelurahan',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Kelurahan'),
        ),
        migrations.AlterField(
            model_name='datapemilih',
            name='nama',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Nama'),
        ),
        migrations.AlterField(
            model_name='datapemilih',
            name='nik',
            field=models.BigIntegerField(blank=True, null=True, verbose_name='NIK'),
        ),
        migrations.AlterField(
            model_name='datapemilih',
            name='nkk',
            field=models.BigIntegerField(blank=True, null=True, verbose_name='NKK'),
        ),
        migrations.AlterField(
            model_name='datapemilih',
            name='rt',
            field=models.IntegerField(blank=True, null=True, verbose_name='RT'),
        ),
        migrations.AlterField(
            model_name='datapemilih',
            name='rw',
            field=models.IntegerField(blank=True, null=True, verbose_name='RW'),
        ),
        migrations.AlterField(
            model_name='datapemilih',
            name='sts_kawin',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Status Kawin'),
        ),
        migrations.AlterField(
            model_name='datapemilih',
            name='tanggal_lahir',
            field=models.DateField(blank=True, null=True, verbose_name='Tanggal Lahir'),
        ),
        migrations.AlterField(
            model_name='datapemilih',
            name='tempat_lahir',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Tempat Lahir'),
        ),
        migrations.AlterField(
            model_name='datapemilih',
            name='tps',
            field=models.IntegerField(blank=True, null=True, verbose_name='TPS'),
        ),
        migrations.AlterField(
            model_name='pengaturanwilayah',
            name='kabupaten_bangka',
            field=models.BooleanField(default=False, verbose_name='Kabupaten Bangka'),
        ),
        migrations.AlterField(
            model_name='pengaturanwilayah',
            name='kabupaten_bangka_barat',
            field=models.BooleanField(default=False, verbose_name='Kabupaten Bangka Barat'),
        ),
        migrations.AlterField(
            model_name='pengaturanwilayah',
            name='kabupaten_bangka_selatan',
            field=models.BooleanField(default=False, verbose_name='Kabupaten Bangka Selatan'),
        ),
        migrations.AlterField(
            model_name='pengaturanwilayah',
            name='kabupaten_bangka_tengah',
            field=models.BooleanField(default=False, verbose_name='Kabupaten Bangka Tengah'),
        ),
        migrations.AlterField(
            model_name='pengaturanwilayah',
            name='kabupaten_belitung',
            field=models.BooleanField(default=True, verbose_name='Kabupaten Belitung'),
        ),
        migrations.AlterField(
            model_name='pengaturanwilayah',
            name='kabupaten_belitung_timur',
            field=models.BooleanField(default=True, verbose_name='Kabupaten Belitung Timur'),
        ),
        migrations.AlterField(
            model_name='pengaturanwilayah',
            name='kota_pangkal_pinang',
            field=models.BooleanField(default=False, verbose_name='Kota Pangkal Pinang'),
        ),
    ]
