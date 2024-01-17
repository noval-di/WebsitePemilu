from django.shortcuts import render

from .forms import PendaftaranPemilihForm
from .models import DataWarga, DataKoordinator, DataPemilih
from django.http import HttpResponse

from .models import PengaturanWilayah
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    pengaturan = PengaturanWilayah.objects.first()
    print("Pengaturan wilayah:", pengaturan.__dict__)

    kabupaten_settings = {
        'Belitung': pengaturan.kabupaten_belitung,
        'Belitung Timur': pengaturan.kabupaten_belitung_timur,
        'Bangka': pengaturan.kabupaten_bangka,
        'Bangka Barat': pengaturan.kabupaten_bangka_barat,
        'Bangka Selatan': pengaturan.kabupaten_bangka_selatan,
        'Bangka Tengah': pengaturan.kabupaten_bangka_tengah,
        'Pangkal Pinang': pengaturan.kota_pangkal_pinang,
    }

    total_pemilih = 0
    total_tps = 0
    total_koordinator = 0
    total_dpt = 0

    for kabupaten, setting in kabupaten_settings.items():
        if setting:
            kelurahan_kabupaten = DataWarga.objects.filter(kabupaten__iexact=kabupaten).values('kelurahan').distinct()
            for kelurahan in kelurahan_kabupaten:
                total_pemilih += DataPemilih.objects.filter(kabupaten__iexact=kabupaten, kelurahan=kelurahan['kelurahan']).count()
                total_tps += DataWarga.objects.filter(kabupaten__iexact=kabupaten, kelurahan=kelurahan['kelurahan']).values('tps').distinct().count()
                total_koordinator += DataKoordinator.objects.filter(kabupaten__iexact=kabupaten, kelurahan=kelurahan['kelurahan']).count()
                total_dpt += DataWarga.objects.filter(kabupaten__iexact=kabupaten, kelurahan=kelurahan['kelurahan']).distinct().count()

    target_per_tps_koordinator = 3  # Target dukungan koordinator per TPS
    target_per_tps_pemilih = 30  # Target pemilih terdaftar per TPS

    if total_tps != 0:
        target_capaian_pemilih = 100 * total_pemilih / (target_per_tps_pemilih * total_tps)
        target_capaian_koordinator = 100 * total_koordinator / (target_per_tps_koordinator * total_tps)
    else:
        target_capaian_pemilih = 0
        target_capaian_koordinator = 0
        
    informasi_kabupaten = {}

    for kabupaten, setting in kabupaten_settings.items():
        if setting:
            informasi_kabupaten[kabupaten] = {
                'id': f'kabupaten_{kabupaten.lower().replace(" ", "_")}',
                'dukungan_koordinator': 0,
                'target_koordinator': 0,
                'persentase_koordinator': 0.0,
                'dukungan_pemilih': 0,
                'target_pemilih': 0,
                'persentase_pemilih': 0.0,
                'kecamatan': {}
            }
            kecamatan_kabupaten = DataWarga.objects.filter(kabupaten__iexact=kabupaten).values('kecamatan').distinct()
            
            for kecamatan in kecamatan_kabupaten:
                informasi_kabupaten[kabupaten]['kecamatan'][kecamatan['kecamatan']] = {
                    'id': f'kecamatan_{kabupaten.lower().replace(" ", "_")}_{kecamatan["kecamatan"].lower().replace(" ", "_")}',
                    'dukungan_koordinator': 0,
                    'target_koordinator': 0,
                    'persentase_koordinator': 0.0,
                    'dukungan_pemilih': 0,
                    'target_pemilih': 0,
                    'persentase_pemilih': 0.0,
                    'kelurahan': {}
                }

                kelurahan_kecamatan = DataWarga.objects.filter(kabupaten__iexact=kabupaten, kecamatan__iexact=kecamatan['kecamatan']).values('kelurahan').distinct()

                for kelurahan in kelurahan_kecamatan:
                    informasi_kabupaten[kabupaten]['kecamatan'][kecamatan['kecamatan']]['kelurahan'][kelurahan['kelurahan']] = {
                        'id': f'kelurahan_{kabupaten.lower().replace(" ", "_")}_{kecamatan["kecamatan"].lower().replace(" ", "_")}_{kelurahan["kelurahan"].lower().replace(" ", "_")}',
                        'dukungan_koordinator': 0,
                        'target_koordinator': 0,
                        'persentase_koordinator': 0.0,
                        'dukungan_pemilih': 0,
                        'target_pemilih': 0,
                        'persentase_pemilih': 0.0,
                        'tps': {}
                    }

                    tps_kelurahan = DataWarga.objects.filter(kabupaten__iexact=kabupaten, kecamatan__iexact=kecamatan['kecamatan'], kelurahan__iexact=kelurahan['kelurahan']).values('tps').distinct()

                    for tps in tps_kelurahan:
                        total_koordinators_tps = DataKoordinator.objects.filter(tingkat_kerja='tps', kabupaten_bertugas__iexact=kabupaten, kecamatan_bertugas__iexact=kecamatan['kecamatan'], kelurahan_bertugas__iexact=kelurahan['kelurahan'], tps_bertugas=tps['tps']).count()
                        total_pemilih_tps = DataPemilih.objects.filter(kabupaten__iexact=kabupaten, kecamatan__iexact=kecamatan['kecamatan'], kelurahan__iexact=kelurahan['kelurahan'], tps=tps['tps']).count()
                        total_target_koordinator_tps = 3
                        total_target_pemilih_tps = 30
                        
                        informasi_kabupaten[kabupaten]['kecamatan'][kecamatan['kecamatan']]['kelurahan'][kelurahan['kelurahan']]['tps'][tps['tps']] = {
                            'id': f'tps_{kabupaten.lower().replace(" ", "_")}_{kecamatan["kecamatan"].lower().replace(" ", "_")}_{kelurahan["kelurahan"].lower().replace(" ", "_")}_{tps["tps"]}',
                            'dukungan_koordinator': total_koordinators_tps,
                            'target_koordinator': total_target_koordinator_tps,
                            'persentase_koordinator': (total_koordinators_tps / total_target_koordinator_tps) * 100 if total_target_koordinator_tps else 0,
                            'dukungan_pemilih': total_pemilih_tps,
                            'target_pemilih': total_target_pemilih_tps,
                            'persentase_pemilih': (total_pemilih_tps / total_target_pemilih_tps) * 100 if total_target_pemilih_tps else 0,
                        }

                    total_koordinator_kelurahan = sum([tps_info['dukungan_koordinator'] for tps_info in informasi_kabupaten[kabupaten]['kecamatan'][kecamatan['kecamatan']]['kelurahan'][kelurahan['kelurahan']]['tps'].values()])
                    total_target_koordinator_kelurahan = sum([tps_info['target_koordinator'] for tps_info in informasi_kabupaten[kabupaten]['kecamatan'][kecamatan['kecamatan']]['kelurahan'][kelurahan['kelurahan']]['tps'].values()])
                    total_pemilih_kelurahan = sum([tps_info['dukungan_pemilih'] for tps_info in informasi_kabupaten[kabupaten]['kecamatan'][kecamatan['kecamatan']]['kelurahan'][kelurahan['kelurahan']]['tps'].values()])
                    total_target_pemilih_kelurahan = sum([tps_info['target_pemilih'] for tps_info in informasi_kabupaten[kabupaten]['kecamatan'][kecamatan['kecamatan']]['kelurahan'][kelurahan['kelurahan']]['tps'].values()])

                    informasi_kabupaten[kabupaten]['kecamatan'][kecamatan['kecamatan']]['kelurahan'][kelurahan['kelurahan']]['dukungan_koordinator'] = total_koordinator_kelurahan
                    informasi_kabupaten[kabupaten]['kecamatan'][kecamatan['kecamatan']]['kelurahan'][kelurahan['kelurahan']]['target_koordinator'] = total_target_koordinator_kelurahan
                    informasi_kabupaten[kabupaten]['kecamatan'][kecamatan['kecamatan']]['kelurahan'][kelurahan['kelurahan']]['persentase_koordinator'] = (total_koordinator_kelurahan / total_target_koordinator_kelurahan) * 100 if total_target_koordinator_kelurahan else 0
                    informasi_kabupaten[kabupaten]['kecamatan'][kecamatan['kecamatan']]['kelurahan'][kelurahan['kelurahan']]['dukungan_pemilih'] = total_pemilih_kelurahan
                    informasi_kabupaten[kabupaten]['kecamatan'][kecamatan['kecamatan']]['kelurahan'][kelurahan['kelurahan']]['target_pemilih'] = total_target_pemilih_kelurahan
                    informasi_kabupaten[kabupaten]['kecamatan'][kecamatan['kecamatan']]['kelurahan'][kelurahan['kelurahan']]['persentase_pemilih'] = (total_pemilih_kelurahan / total_target_pemilih_kelurahan) * 100 if total_target_pemilih_kelurahan else 0

                total_koordinator_kecamatan = sum([kelurahan_info['dukungan_koordinator'] for kelurahan_info in informasi_kabupaten[kabupaten]['kecamatan'][kecamatan['kecamatan']]['kelurahan'].values()])
                total_target_koordinator_kecamatan = sum([kelurahan_info['target_koordinator'] for kelurahan_info in informasi_kabupaten[kabupaten]['kecamatan'][kecamatan['kecamatan']]['kelurahan'].values()])
                total_pemilih_kecamatan = sum([kelurahan_info['dukungan_pemilih'] for kelurahan_info in informasi_kabupaten[kabupaten]['kecamatan'][kecamatan['kecamatan']]['kelurahan'].values()])
                total_target_pemilih_kecamatan = sum([kelurahan_info['target_pemilih'] for kelurahan_info in informasi_kabupaten[kabupaten]['kecamatan'][kecamatan['kecamatan']]['kelurahan'].values()])
                
                informasi_kabupaten[kabupaten]['kecamatan'][kecamatan['kecamatan']]['dukungan_koordinator'] = total_koordinator_kecamatan
                informasi_kabupaten[kabupaten]['kecamatan'][kecamatan['kecamatan']]['target_koordinator'] = total_target_koordinator_kecamatan
                informasi_kabupaten[kabupaten]['kecamatan'][kecamatan['kecamatan']]['persentase_koordinator'] = (total_koordinator_kecamatan / total_target_koordinator_kecamatan) * 100 if total_target_koordinator_kecamatan else 0
                informasi_kabupaten[kabupaten]['kecamatan'][kecamatan['kecamatan']]['dukungan_pemilih'] = total_pemilih_kecamatan
                informasi_kabupaten[kabupaten]['kecamatan'][kecamatan['kecamatan']]['target_pemilih'] = total_target_pemilih_kecamatan
                informasi_kabupaten[kabupaten]['kecamatan'][kecamatan['kecamatan']]['persentase_pemilih'] = (total_pemilih_kecamatan / total_target_pemilih_kecamatan) * 100 if total_target_pemilih_kecamatan else 0

            
            total_koordinator_kabupaten = sum([kecamatan_info['dukungan_koordinator'] for kecamatan_info in informasi_kabupaten[kabupaten]['kecamatan'].values()])
            total_target_koordinator_kabupaten = sum([kecamatan_info['target_koordinator'] for kecamatan_info in informasi_kabupaten[kabupaten]['kecamatan'].values()])
            total_pemilih_kabupaten = sum([kecamatan_info['dukungan_pemilih'] for kecamatan_info in informasi_kabupaten[kabupaten]['kecamatan'].values()])
            total_target_pemilih_kabupaten = sum([kecamatan_info['target_pemilih'] for kecamatan_info in informasi_kabupaten[kabupaten]['kecamatan'].values()])

            informasi_kabupaten[kabupaten]['dukungan_koordinator'] = total_koordinator_kabupaten
            informasi_kabupaten[kabupaten]['target_koordinator'] = total_target_koordinator_kabupaten
            informasi_kabupaten[kabupaten]['persentase_koordinator'] = (total_koordinator_kabupaten / total_target_koordinator_kabupaten) * 100 if total_target_koordinator_kabupaten else 0
            informasi_kabupaten[kabupaten]['dukungan_pemilih'] = total_pemilih_kabupaten
            informasi_kabupaten[kabupaten]['target_pemilih'] = total_target_pemilih_kabupaten
            informasi_kabupaten[kabupaten]['persentase_pemilih'] = (total_pemilih_kabupaten / total_target_pemilih_kabupaten) * 100 if total_target_pemilih_kabupaten else 0
    
    context = {
        'total_pemilih': total_pemilih,
        'total_koordinator': total_koordinator,
        'total_dpt': total_dpt,
        'target_capaian_pemilih': target_capaian_pemilih,
        'target_capaian_koordinator': target_capaian_koordinator,
        'total_tps': total_tps,
        
        'informasi_kabupaten': informasi_kabupaten,
        'target_per_tps_koordinator': target_per_tps_koordinator,
        'target_per_tps_pemilih': target_per_tps_pemilih,
    }
    return render(request, 'Pemilu/dashboard.html', context)

from django.shortcuts import render
from .models import PengaturanWilayah

@login_required
def data_pemilih(request):
    jumlah_data_pemilih = DataPemilih.objects.count()
    data_pemilih = DataPemilih.objects.all()
    
    kabupaten_list = DataPemilih.objects.values_list('kabupaten', flat=True).distinct()
    kecamatan_list = DataPemilih.objects.values_list('kecamatan', flat=True).distinct()
    kelurahan_list = DataPemilih.objects.values_list('kelurahan', flat=True).distinct()
    tps_list = DataPemilih.objects.values_list('tps', flat=True).distinct()

    context = {
        'total_pemilih': jumlah_data_pemilih,
        'data_pemilih': data_pemilih,
        'kabupaten_list': kabupaten_list,
        'kecamatan_list': kecamatan_list,
        'kelurahan_list': kelurahan_list,
        'tps_list': tps_list,
    }
    return render(request, 'Pemilu/data_pemilih.html', context)

from .forms import KoordinatorForm

@login_required
def data_koordinator(request):
    jumlah_data_koordinator = DataKoordinator.objects.count()
    data_koordinator = DataKoordinator.objects.all()
    
    kabupaten_list = DataKoordinator.objects.values_list('kabupaten_bertugas', flat=True).distinct()
    kecamatan_list = DataKoordinator.objects.values_list('kecamatan_bertugas', flat=True).distinct()
    kelurahan_list = DataKoordinator.objects.values_list('kelurahan_bertugas', flat=True).distinct()
    tps_list = DataKoordinator.objects.values_list('tps_bertugas', flat=True).distinct()
    
    context = {
        'total_koordinator': jumlah_data_koordinator,
        'data_koordinator': data_koordinator,
        'kabupaten_list': kabupaten_list,
        'kecamatan_list': kecamatan_list,
        'kelurahan_list': kelurahan_list,
        'tps_list': tps_list,
    }
    return render(request, 'Pemilu/data_koordinator.html',context )

from django.http import JsonResponse

def verifikasi_nik(request):
    if request.method == 'POST':
        nik = request.POST.get('nik')
        nik_terdaftar = DataWarga.objects.filter(nik=nik).exists()
        if nik_terdaftar == True:
            data_warga = DataWarga.objects.filter(nik=nik).first()
            data = {
                'registered': True,
                'data_warga': {
                    
                    'kabupaten': data_warga.kabupaten,
                    'kecamatan': data_warga.kecamatan,
                    'kelurahan': data_warga.kelurahan,
                    'nkk': data_warga.nkk,
                    'nik': data_warga.nik,
                    'nama': data_warga.nama,
                    'tempat_lahir': data_warga.tempat_lahir,
                    'tanggal_lahir': data_warga.tanggal_lahir,
                    'sts_kawin': data_warga.sts_kawin,
                    'kelamin': data_warga.kelamin,
                    'alamat': data_warga.alamat,
                    'rt': data_warga.rt,
                    'rw': data_warga.rw,
                    'disabilitas': data_warga.disabilitas,
                    'ektp': data_warga.ektp,
                    'tps': data_warga.tps,
                }}
            
            return JsonResponse( data )

    return JsonResponse({}, status=400)

from django.shortcuts import render, redirect
from .forms import KoordinatorForm
from django.contrib import messages

@login_required
def tambah_koordinator(request):
    if request.method == 'POST':
        form = KoordinatorForm(request.POST, request.FILES)
        if form.is_valid():
            koordinator = form.save(commit=False)
            koordinator.jumlah_rekrutan = 0  
            koordinator.save()
            return JsonResponse({'success': True, 'message': 'Koordinator berhasil ditambahkan', 'redirect': '/tambah-koordinator/'})
        else:
            error_message = 'Terjadi kesalahan dalam pengisian wilayah tugas koordinator.'
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error pada field '{field}': {error}")
                    if field in ['kabupaten_bertugas', 'kecamatan_bertugas', 'kelurahan_bertugas', 'tps_bertugas']:
                        messages.error(request, error_message)
            return JsonResponse({'success': False, 'message': error_message})
    else:
        form = KoordinatorForm()
    if form.errors:
        for field, error in form.errors.items():
            messages.error(request, f'{field}: {error}')
    
    context = {'form': form}
    return render(request, 'Pemilu/tambah_koordinator.html', context)


from django.shortcuts import get_object_or_404, render

@login_required
def edit_koordinator(request, coordinator_id):
    koordinator = get_object_or_404(DataKoordinator, id=coordinator_id)

    if request.method == 'POST':
        form = KoordinatorForm(request.POST, instance=koordinator)
        if form.is_valid():
            form.save()
            return redirect('data_koordinator') 
    else:
        form = KoordinatorForm(instance=koordinator)

    context = {'form': form}
    return render(request, 'Pemilu/edit_koordinator.html', context)

def delete_koordinator(request, coordinator_id):
    try:
        koordinator = DataKoordinator.objects.get(id=coordinator_id)
        koordinator.delete()
        return JsonResponse({'message': 'Koordinator berhasil dihapus'})
    except DataKoordinator.DoesNotExist:
        return JsonResponse({'error': 'Koordinator tidak ditemukan'}, status=404)

def cek_dpt(request, nik):
    data_warga = DataWarga.objects.filter(nik=nik).exists()  # Mengecek keberadaan NIK dalam data_warga
    return render(request, 'cek_dpt.html', {'terdaftar': data_warga})

@login_required
def daftar_pemilih(request):
    jumlah_data_pemilih = DataPemilih.objects.count()
    
    if request.method == 'POST':
        form = PendaftaranPemilihForm(request.POST)
        if form.is_valid():
            nama_input = form.cleaned_data['nama']
            is_dpt = DataWarga.objects.filter(nama=nama_input).exists()
            if is_dpt:
                DataPemilih.objects.create(nama=nama_input,)  
                return HttpResponse("Pemilih berhasil ditambahkan.")
            else:
                return HttpResponse("NIK tidak terdaftar sebagai DPT.")
    else:
        form = PendaftaranPemilihForm()
        
    context = {
        'total_pemilih': jumlah_data_pemilih,
        'form': form,
    }
    return render(request, 'Pemilu/daftar_pemilih.html', context)



from .forms import PemilihForm

from django.shortcuts import get_object_or_404

@login_required
def tambah_pemilih(request):
    if request.method == 'POST':
        form = PemilihForm(request.POST, request.FILES)
        if form.is_valid():
            pemilih = form.save(commit=False)  
            koordinator_id = pemilih.koordinator.id
            koordinator = DataKoordinator.objects.get(pk=koordinator_id)
            koordinator.jumlah_rekrutan += 1
            koordinator.save()
            pemilih.save()
            return JsonResponse({'success': True, 'message': 'Relawan berhasil ditambahkan', 'redirect': '/tambah-pemilih/'}) 
        else:
            error_message = 'Terjadi kesalahan dalam pengisian form relawan.'
            for field, errors in form.errors.items():
                messages.error(request, error_message)
            return JsonResponse({'success': False, 'message': error_message})
    else:
        form = PemilihForm()
    
    context = {'form': form}
    return render(request, 'Pemilu/tambah_pemilih.html', context)

def delete_pemilih(request, pemilih_id):
    try:
        pemilih = DataPemilih.objects.get(id=pemilih_id)
        pemilih.delete()
        return JsonResponse({'message': 'Pemilih berhasil dihapus'})
    except DataPemilih.DoesNotExist:
        return JsonResponse({'error': 'Pemilih tidak ditemukan'}, status=404)
    
@login_required
def edit_pemilih(request, pemilih_id):
    pemilih = get_object_or_404(DataPemilih, id=pemilih_id)
    if request.method == 'POST':
        form = PemilihForm(request.POST, instance=pemilih)
        if form.is_valid():
            form.save()
            return redirect('data_pemilih') 
    else:
        form = PemilihForm(instance=pemilih)

    context = {'form': form}
    return render(request, 'Pemilu/edit_pemilih.html', context)

from django.shortcuts import render
from .models import DataPemilih

@login_required
def filter_data_pemilih(request):
    kabupaten = request.GET.get('kabupaten')
    kecamatan = request.GET.get('kecamatan')
    kelurahan = request.GET.get('kelurahan')
    tps = request.GET.get('tps')

    filtered_data_pemilih = DataPemilih.objects.all()
    if kabupaten:
        filtered_data_pemilih = filtered_data_pemilih.filter(kabupaten=kabupaten)

    if kecamatan:
        filtered_data_pemilih = filtered_data_pemilih.filter(kecamatan=kecamatan)

    if kelurahan:
        filtered_data_pemilih = filtered_data_pemilih.filter(kelurahan=kelurahan)

    if tps:
        filtered_data_pemilih = filtered_data_pemilih.filter(tps=tps)

    jumlah_data_pemilih_setelah_filter = filtered_data_pemilih.count()
    context = {
        'data_pemilih': filtered_data_pemilih,
        'jumlah_data_setelah_filter': jumlah_data_pemilih_setelah_filter,
    }
    return render(request, 'Pemilu/daftar_pemilih_filter.html', context)

@login_required
def filter_data_koordinator(request):
    tingkat_kerja = request.GET.get('tingkat_kerja')
    kabupaten_bertugas = request.GET.get('kabupaten_bertugas')
    kecamatan_bertugas = request.GET.get('kecamatan_bertugas')
    kelurahan_bertugas = request.GET.get('kelurahan_bertugas')
    tps_bertugas = request.GET.get('tps_bertugas')
    
    koordinator = DataKoordinator.objects.all()

    if tingkat_kerja != 'semua_tingkat':
        koordinator = koordinator.filter(tingkat_kerja=tingkat_kerja)

    if kabupaten_bertugas:
        koordinator = koordinator.filter(kabupaten_bertugas__iexact=kabupaten_bertugas)
    if kecamatan_bertugas:
        koordinator = koordinator.filter(kecamatan_bertugas__iexact=kecamatan_bertugas)
    if kelurahan_bertugas:
        koordinator = koordinator.filter(kelurahan_bertugas__iexact=kelurahan_bertugas)
    if tps_bertugas:
        koordinator = koordinator.filter(tps_bertugas__iexact=tps_bertugas)
            
    jumlah_data_koordinator_setelah_filter = koordinator.count()

    list_kabupaten = DataKoordinator.objects.values_list('kabupaten_bertugas', flat=True).distinct()
    list_kecamatan = DataKoordinator.objects.values_list('kecamatan_bertugas', flat=True).distinct()
    list_kelurahan = DataKoordinator.objects.values_list('kelurahan_bertugas', flat=True).distinct()
    list_tps = DataKoordinator.objects.values_list('tps_bertugas', flat=True).distinct()

    context = {
        'data_koordinator': koordinator,
        'jumlah_data_setelah_filter': jumlah_data_koordinator_setelah_filter,
        'list_kabupaten': list_kabupaten,
        'list_kecamatan': list_kecamatan,
        'list_kelurahan': list_kelurahan,
        'list_tps': list_tps,

    }

    return render(request, 'Pemilu/daftar_koordinator_filter.html', context)

import csv
from django.http import HttpResponse
from .models import DataPemilih

import pandas as pd

def unduh_data_pemilih(request):
    kabupaten = request.GET.get('kabupaten')
    kecamatan = request.GET.get('kecamatan')
    kelurahan = request.GET.get('kelurahan')
    tps = request.GET.get('tps')

    filtered_data_pemilih = DataPemilih.objects.all()

    if kabupaten:
        filtered_data_pemilih = filtered_data_pemilih.filter(kabupaten=kabupaten)
    if kecamatan:
        filtered_data_pemilih = filtered_data_pemilih.filter(kecamatan=kecamatan)
    if kelurahan:
        filtered_data_pemilih = filtered_data_pemilih.filter(kelurahan=kelurahan)

    if tps:
        filtered_data_pemilih = filtered_data_pemilih.filter(tps=tps)

    data_to_download = filtered_data_pemilih.values_list('nama', 'nik', 'kabupaten', 'kecamatan', 'kelurahan', 'tps', 'koordinator__nama')
    df = pd.DataFrame(list(data_to_download), columns=['Nama','NIK', 'Kabupaten', 'Kecamatan', 'Kelurahan', 'TPS','Koordinator'])
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="data_pemilih.csv"'
    df.to_csv(path_or_buf=response, index=False)

    return response


def unduh_data_koordinator(request):
    kabupaten_bertugas = request.GET.get('kabupaten_bertugas')
    kecamatan_bertugas = request.GET.get('kecamatan_bertugas')
    kelurahan_bertugas = request.GET.get('kelurahan_bertugas')
    tps_bertugas = request.GET.get('tps_bertugas')

    filtered_data_koordinator = DataKoordinator.objects.all()

    if kabupaten_bertugas:
        filtered_data_koordinator = filtered_data_koordinator.filter(kabupaten_bertugas=kabupaten_bertugas)
    if kecamatan_bertugas:
        filtered_data_koordinator = filtered_data_koordinator.filter(kecamatan_bertugas=kecamatan_bertugas)
    if kelurahan_bertugas:
        filtered_data_koordinator = filtered_data_koordinator.filter(kelurahan_bertugas=kelurahan_bertugas)

    if tps_bertugas:
        filtered_data_koordinator = filtered_data_koordinator.filter(tps_bertugas=tps_bertugas)

    data_to_download = filtered_data_koordinator.values_list('nama','nik','no_hp', 'tingkat_kerja', 'kabupaten_bertugas', 'kecamatan_bertugas', 'kelurahan_bertugas', 'tps_bertugas','jumlah_rekrutan')


    df = pd.DataFrame(list(data_to_download), columns=['Nama', 'NIK', 'NO HP', 'Tingkat Kerja','Kabupaten', 'Kecamatan', 'Kelurahan', 'TPS', 'Jumlah Rekrutan'])

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="data_koordinator.csv"'
    df.to_csv(path_or_buf=response, index=False)

    return response




from django.shortcuts import render
from .models import DataWarga

@login_required
def data_wilayah_view(request):
    kabupaten_list = DataWarga.objects.values('kabupaten').distinct()
    kecamatan_list = DataWarga.objects.values('kecamatan').distinct()
    kelurahan_list = DataWarga.objects.values('kelurahan').distinct()
    tps_list = DataWarga.objects.values('tps').distinct()

    total_kabupaten = len(kabupaten_list)
    total_kecamatan = len(kecamatan_list)
    total_kelurahan = len(kelurahan_list)

    data_kabupaten = []
    total_tps = 0
    for kabupaten in kabupaten_list:
        kecamatan_list = DataWarga.objects.filter(kabupaten=kabupaten['kabupaten']).values('kecamatan').distinct()
        data_kecamatan = []
        
        jumlah_koordinator_kabupaten = DataKoordinator.objects.filter(tingkat_kerja='kabupaten', kabupaten_bertugas__iexact=kabupaten['kabupaten']).count()
        jumlah_pemilih_kabupaten = DataPemilih.objects.filter(kabupaten=kabupaten['kabupaten']).count()
        
        
        for kecamatan in kecamatan_list:
            kelurahan_list = DataWarga.objects.filter(kabupaten=kabupaten['kabupaten'], kecamatan=kecamatan['kecamatan']).values('kelurahan').distinct()
            data_kelurahan = []
            
            jumlah_koordinator_kecamatan = DataKoordinator.objects.filter(tingkat_kerja='kecamatan', kabupaten_bertugas__iexact=kabupaten['kabupaten'], kecamatan_bertugas__iexact=kecamatan['kecamatan']).count()
            jumlah_pemilih_kecamatan = DataPemilih.objects.filter(kabupaten=kabupaten['kabupaten'], kecamatan=kecamatan['kecamatan']).count()

            for kelurahan in kelurahan_list:
                tps_list = DataWarga.objects.filter(kabupaten=kabupaten['kabupaten'], kecamatan=kecamatan['kecamatan'] ,kelurahan=kelurahan['kelurahan']).values('tps').distinct().order_by('tps')
                data_tps = []
                
                total_tps_kelurahan = len(tps_list)
                total_tps += total_tps_kelurahan
                
                jumlah_koordinator_kelurahan = DataKoordinator.objects.filter(tingkat_kerja='kelurahan', kabupaten_bertugas__iexact=kabupaten['kabupaten'], kecamatan_bertugas__iexact=kecamatan['kecamatan'], kelurahan_bertugas__iexact=kelurahan['kelurahan']).count()
                jumlah_pemilih_kelurahan = DataPemilih.objects.filter(kabupaten=kabupaten['kabupaten'], kecamatan=kecamatan['kecamatan'], kelurahan=kelurahan['kelurahan']).count()
                
                for tps in tps_list:
                    jumlah_koordinator_tps = DataKoordinator.objects.filter(tingkat_kerja='tps', kabupaten_bertugas__iexact=kabupaten['kabupaten'], kecamatan_bertugas__iexact=kecamatan['kecamatan'], kelurahan_bertugas__iexact=kelurahan['kelurahan'], tps_bertugas=tps['tps']).count()
                    jumlah_pemilih_tps = DataPemilih.objects.filter(kabupaten=kabupaten['kabupaten'], kecamatan=kecamatan['kecamatan'], kelurahan=kelurahan['kelurahan'], tps=tps['tps']).count()

                    data_tps.append({
                        'nama_tps': tps['tps'],
                        'jumlah_koordinator_tps': jumlah_koordinator_tps,
                        'jumlah_pemilih_tps': jumlah_pemilih_tps,
                    })
                
                data_kelurahan.append({
                    'nama_kelurahan': kelurahan['kelurahan'],
                    'jumlah_koordinator_kelurahan': jumlah_koordinator_kelurahan,
                    'jumlah_pemilih_kelurahan': jumlah_pemilih_kelurahan,
                    'tps_list': data_tps,
                })
                
            data_kecamatan.append({
                'nama_kecamatan': kecamatan['kecamatan'],
                'jumlah_koordinator_kecamatan': jumlah_koordinator_kecamatan,
                'jumlah_pemilih_kecamatan': jumlah_pemilih_kecamatan,
                'kelurahan_list': data_kelurahan,
            })
        
        data_kabupaten.append({
            'nama_kabupaten': kabupaten['kabupaten'], 
            'jumlah_koordinator_kabupaten':jumlah_koordinator_kabupaten, 
            'jumlah_pemilih_kabupaten':jumlah_pemilih_kabupaten,
            'kecamatan_list': data_kecamatan,
            })
        
    
    context = {
        'kabupaten_list' : kabupaten_list,

        'total_kabupaten': total_kabupaten,
        'total_kecamatan': total_kecamatan,
        'total_kelurahan': total_kelurahan,
        'total_tps': total_tps,
        
        'data_kabupaten': data_kabupaten,
        'data_kecamatan': data_kecamatan,
        'data_kelurahan': data_kelurahan,
        'data_tps': data_tps,

    }
    return render(request, 'Pemilu/data_wilayah.html', context)

from django.shortcuts import render
from .models import PengaturanWilayah
from .forms import PengaturanWilayahForm

@login_required
def setting_page(request):
    pengaturan = PengaturanWilayah.objects.first() 
    form = PengaturanWilayahForm(instance=pengaturan)

    if request.method == 'POST':
        form = PengaturanWilayahForm(request.POST, instance=pengaturan)
        if form.is_valid():
            form.save()
          
    return render(request, 'Pemilu/setting.html', {'form': form})

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
 
def user_login(request):
    if request.method == 'POST':
        print('test1')
        username = request.POST["username"]
        password = request.POST["password"]
        print(username)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            print("Login berhasil")
            return redirect('dashboard')
        else:
            print("Login gagal")
            return HttpResponse("Login gagal. Tampilkan pesan kesalahan atau kembali ke halaman login.")
    else:
        return render(request, 'registration/login.html')

def user_logout(request):
    logout(request)
    return redirect('login_user')

def redirect_to_login(request):
    return redirect('login_user') 


from Pemilu.models import DataPemilu
from django.db.models import Count, Sum

@login_required
def analisa (request):
    kabupaten_data = DataPemilu.objects.values('kabupaten').distinct()
    
    data_by_kabupaten = []
    for kabupaten in kabupaten_data:
        kabupaten_name = kabupaten['kabupaten'].strip()
        print(kabupaten_name)
        data_kabupaten = DataPemilu.objects.filter(kabupaten=kabupaten['kabupaten']).aggregate(
            suara_calon_1_2019=Sum('calon_1_2019'),
            suara_calon_2_2019=Sum('calon_2_2019'),
            suara_calon_3_2019=Sum('calon_3_2019'),
            suara_partai_2019=Sum('suara_Partai_2019'),
            total_suara_2019=Sum('calon_1_2019') + Sum('calon_2_2019') + Sum('calon_3_2019') + Sum('suara_Partai_2019'),
            suara_calon_1_2024=Sum('calon_1_2024'),
            total_suara_2024=Sum('total_suara_2024'),
        )
        data_kabupaten.update({'nama_kabupaten': kabupaten_name, 'id': kabupaten['kabupaten']})

        kecamatan_data = DataPemilu.objects.filter(kabupaten=kabupaten['kabupaten']).values('kecamatan').distinct()
    
        data_kabupaten['kecamatan'] = []
        for kecamatan in kecamatan_data:
            kecamatan_name = kecamatan['kecamatan'].strip()
            data_kecamatan = DataPemilu.objects.filter(kabupaten=kabupaten['kabupaten'], kecamatan=kecamatan_name).aggregate(
                suara_calon_1_2019=Sum('calon_1_2019'),
                suara_calon_2_2019=Sum('calon_2_2019'),
                suara_calon_3_2019=Sum('calon_3_2019'),
                suara_partai_2019=Sum('suara_Partai_2019'),
                total_suara_2019=Sum('calon_1_2019') + Sum('calon_2_2019') + Sum('calon_3_2019') + Sum('suara_Partai_2019'),
                suara_calon_1_2024=Sum('calon_1_2024'),
                total_suara_2024=Sum('total_suara_2024'),
            )
            data_kecamatan.update({'nama_kecamatan': kecamatan_name, 'id': f"{kabupaten_name}_{kecamatan_name}"})
            data_kabupaten['kecamatan'].append(data_kecamatan)
            
            kelurahan_data = DataPemilu.objects.filter(kabupaten=kabupaten['kabupaten'], kecamatan=kecamatan_name).values('kelurahan').distinct()
            data_kecamatan['kelurahan'] = []

            for kelurahan in kelurahan_data:
                kelurahan_name = kelurahan['kelurahan'].strip()
                data_kelurahan = DataPemilu.objects.filter(kabupaten=kabupaten['kabupaten'], kecamatan=kecamatan_name, kelurahan=kelurahan_name).aggregate(
                    suara_calon_1_2019=Sum('calon_1_2019'),
                    suara_calon_2_2019=Sum('calon_2_2019'),
                    suara_calon_3_2019=Sum('calon_3_2019'),
                    suara_partai_2019=Sum('suara_Partai_2019'),
                    total_suara_2019=Sum('calon_1_2019') + Sum('calon_2_2019') + Sum('calon_3_2019') + Sum('suara_Partai_2019'),
                    suara_calon_1_2024=Sum('calon_1_2024'),
                    total_suara_2024=Sum('total_suara_2024'),
                )
                data_kelurahan.update({'nama_kelurahan': kelurahan_name, 'id': f"{kecamatan_name}_{kelurahan_name}"})
                data_kecamatan['kelurahan'].append(data_kelurahan)

                tps_data = DataPemilu.objects.filter(kabupaten=kabupaten['kabupaten'], kecamatan=kecamatan_name, kelurahan=kelurahan_name).values('tps').distinct()
                data_kelurahan['tps'] = []

                for tps in tps_data:
                    tps_name = tps['tps'].strip()
                   
                    data_tps = DataPemilu.objects.filter(kabupaten=kabupaten['kabupaten'], kecamatan=kecamatan_name, kelurahan=kelurahan_name, tps=tps_name).aggregate(
                        suara_calon_1_2019=Sum('calon_1_2019'),
                        suara_calon_2_2019=Sum('calon_2_2019'),
                        suara_calon_3_2019=Sum('calon_3_2019'),
                        suara_partai_2019=Sum('suara_Partai_2019'),
                        total_suara_2019=Sum('calon_1_2019') + Sum('calon_2_2019') + Sum('calon_3_2019') + Sum('suara_Partai_2019'),
                        suara_calon_1_2024=Sum('calon_1_2024'),
                        total_suara_2024=Sum('total_suara_2024'),
                    )
                    data_tps.update({'nama_tps': tps_name, 'id': f"{kelurahan_name}_{tps_name}"})
                    data_kelurahan['tps'].append(data_tps)


        data_by_kabupaten.append(data_kabupaten)
        
    context = {

        'data_by_kabupaten' : data_by_kabupaten,
        'kabupaten_terpilih': request.GET.get('kabupaten'),
        'kecamatan_terpilih': request.GET.get('kecamatan'),
        'kelurahan_terpilih': request.GET.get('kelurahan'),
    }
        
    return render(request, 'Pemilu/analisa.html',context)

from .forms import DataPemiluForm

@login_required
def list_wilayah(request):
    kabupaten_data = DataPemilu.objects.values('kabupaten').distinct()
    
    data_kabupaten = []
    for kabupaten in kabupaten_data:
        kabupaten_name = kabupaten['kabupaten'].strip()
        kecamatan_data = DataPemilu.objects.filter(kabupaten=kabupaten['kabupaten']).values('kecamatan').distinct()
        
        data_kecamatan = []
        for kecamatan in kecamatan_data:
            kecamatan_name = kecamatan['kecamatan'].strip()
            kelurahan_data = DataPemilu.objects.filter(kabupaten=kabupaten['kabupaten'], kecamatan=kecamatan_name).values('kelurahan').distinct()

            data_kelurahan = []
            for kelurahan in kelurahan_data:
                kelurahan_name = kelurahan['kelurahan'].strip()
                tps_data = DataPemilu.objects.filter(kabupaten=kabupaten['kabupaten'], kecamatan=kecamatan_name, kelurahan=kelurahan_name)

                tps_data = sorted(tps_data, key=lambda x: int(x.tps))

                data_kelurahan.append({
                    'kelurahan_name': kelurahan_name,
                    'tps_data': tps_data,
                    'kelurahan_id': f'kelurahan_{kabupaten_name}_{kecamatan_name}_{kelurahan_name}'
                })

            data_kecamatan.append({
                'kecamatan_name': kecamatan_name,
                'kelurahan_data': data_kelurahan,
                'kecamatan_id': f'kecamatan_{kabupaten_name}_{kecamatan_name}'
            })

        data_kabupaten.append({
            'kabupaten_name': kabupaten_name,
            'kecamatan_data': data_kecamatan,
            'kabupaten_id': f'kabupaten_{kabupaten_name}'
        })
        
    context = {
    'data_kabupaten': data_kabupaten
    }
    
    return render(request, 'Pemilu/list_wilayah.html', context)

# views.py

from django.shortcuts import render, get_object_or_404
from .models import DataPemilu
from .forms import DataPemiluForm

from .forms import DataPemiluForm
# views.py

@login_required
def isi_hasil_pemilu(request, kelurahan_name):
    data_pemilu = DataPemilu.objects.filter(kelurahan=kelurahan_name)

    if request.method == 'POST':
        forms = [DataPemiluForm(request.POST, instance=pemilu, prefix=pemilu.tps) for pemilu in data_pemilu]
        if all(form.is_valid() for form in forms):
            for form in forms:
                form.save()
            return JsonResponse({'success': True, 'message': 'Data berhasil ditambahkan'})
        else:
            return JsonResponse({'success': False, 'message': 'Gagal menyimpan data'}, status=400)

    else:
        forms = [DataPemiluForm(instance=pemilu, prefix=pemilu.tps) for pemilu in data_pemilu]

    tps_names = sorted(set(pemilu.tps for pemilu in data_pemilu), key=lambda x: int(x))

    context = {
        'data_pemilu': data_pemilu,
        'forms': forms,
        'kelurahan_name': kelurahan_name,
        'tps_names': tps_names,
    }

    return render(request, 'Pemilu/isi_hasil_pemilu.html', context)
