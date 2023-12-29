# Generated by Django 3.2.18 on 2023-12-14 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Pemilu', '0003_rename_daftarpemilih_datapemilih'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datakoordinator',
            name='alamat',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='datakoordinator',
            name='kabupaten',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='datakoordinator',
            name='kecamatan',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='datakoordinator',
            name='kelurahan',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='datakoordinator',
            name='tempat_lahir',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='datakoordinator',
            name='wilayah_kerja',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='datawarga',
            name='alamat',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='datawarga',
            name='ektp',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='datawarga',
            name='kabupaten',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='datawarga',
            name='kecamatan',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='datawarga',
            name='kelurahan',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='datawarga',
            name='tempat_lahir',
            field=models.CharField(max_length=255),
        ),
    ]