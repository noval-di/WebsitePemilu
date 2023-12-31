# Generated by Django 3.2.18 on 2023-12-21 07:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Pemilu', '0007_auto_20231217_1145'),
    ]

    operations = [
        migrations.RenameField(
            model_name='datakoordinator',
            old_name='wilayah_kerja',
            new_name='nama_wilayah',
        ),
        migrations.AddField(
            model_name='datakoordinator',
            name='tingkat_kerja',
            field=models.CharField(choices=[('kabupaten', 'Kabupaten'), ('kecamatan', 'Kecamatan'), ('kelurahan', 'Kelurahan'), ('tps', 'TPS'), ('belum_ditentukan', 'Belum Ditentukan')], default='belum_ditentukan', max_length=20),
        ),
    ]
