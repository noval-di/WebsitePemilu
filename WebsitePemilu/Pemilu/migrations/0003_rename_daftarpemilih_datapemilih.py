# Generated by Django 3.2.18 on 2023-12-14 06:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Pemilu', '0002_rename_koordinator_datakoordinator'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='DaftarPemilih',
            new_name='DataPemilih',
        ),
    ]
