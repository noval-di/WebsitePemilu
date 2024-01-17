from django import forms

class PendaftaranPemilihForm(forms.Form):
    nik = forms.CharField(label='NIK')
    # Tambahkan field-form lainnya sesuai kebutuhan
    
class PendaftaranKoordinatorForm(forms.Form):
    nik = forms.CharField(label='NIK')
    # Tambahkan field-form lainnya sesuai kebutuhan
    
from django import forms
from .models import DataKoordinator
from .models import DataPemilih

# Data wilayah yang Anda sediakan sebelumnya
dataWilayah = {
    "Belitung": {
        "Membalong": ["Bantan", "Gunung Riting", "Kembiri", "Lassar", "Membalong", "Mentigi", "Padang Kandis", "Perpat", "Pulau Seliu", "Pulau Sumedang", "Simpang Rusa", "Tanjungrusa"],
        "Tanjung Pandan": ["Air Ketekok", "Air Pelempang Jaya", "Air Rayak", "Air Merbau", "Air Saga", "Buluh Tumbang", "Dukong", "Juru Seberang", "Perawas", "Kampong Damai", "Kota", "Lesung Batang", "Paal Satu", "Pangkallalang", "Parit", "Tanjungpendam"],
        "Badau": ["Air Batu Buding", "Badau", "Cerucuk", "Ibul", "Kacang Butor", "Pegantungan", "Sungai Samak"],
        "Sijuk": ["Air Selumar", "Air Seruk", "Batu Itam", "Keciput", "Pelepak Pute", "Sijuk", "Sungai Padang", "Tanjong Tinggi", "Tanjung Binga", "Terong"],
        "Selat Nasik": ["Petaling", "Pulau Gersik", "Selat Nasik", "Suak Gual"],
    },
    "Belitung Timur": {
        "Damar": ["Air Kelik", "Burong Mandi", "Mempaya", "Mengkubang", "Sukamandi"],
        "Dendang": ["Balok", "Dendang", "Jangkang", "Nyuruk"],
        "Gantung": ["Batu Penyu", "Gantung", "Jangkar Asam", "Lenggang", "Lilangan", "Limbongan", "Selingsing"],
        "Kelapa Kampit": ["Buding", "Cendil", "Mayang", "Mentawak", "Pembaharuan", "Senyubuk"],
        "Manggar": ["Baru", "Bentaian Jaya", "Buku Limau", "Kelubi", "Kurnia Jaya", "Lalang", "Lalang Jaya", "Mekar Jaya", "Padang"],
        "Simpang Pesak": ["Dukong", "Simpang Pesak", "Tanjung Batu Itam", "Tanjung Kelumpang"],
        "Simpang Renggiang": ["Aik Madu", "Lintang", "Renggiang", "Simpang Tiga"],
    },
}

from django import forms

from django import forms

class KoordinatorForm(forms.ModelForm):
    class Meta:
        model = DataKoordinator
        exclude = ['jumlah_rekrutan']
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        nik = str(self.cleaned_data['nik'])
        instance.foto_ktp.name = f'foto_ktp_{nik}.jpg'

        if commit:
            instance.save()

        return instance

    def clean(self):
        cleaned_data = super().clean()
        kabupaten_bertugas = cleaned_data.get('kabupaten_bertugas')
        kecamatan_bertugas = cleaned_data.get('kecamatan_bertugas')
        kelurahan_bertugas = cleaned_data.get('kelurahan_bertugas')

        if not kabupaten_bertugas:
            # Set a default value for kecamatan and kelurahan if kabupaten is empty
            cleaned_data['kecamatan_bertugas'] = 'none'
            cleaned_data['kelurahan_bertugas'] = 'none'
        
        # Tambahkan validasi khusus jika diperlukan
        return cleaned_data



class PemilihForm(forms.ModelForm):
    class Meta:
        model = DataPemilih
        fields = '__all__' 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['koordinator'].queryset = DataKoordinator.objects.all()
        self.fields['koordinator'].widget = forms.HiddenInput()
        #self.fields['koordinator'].widget = forms.Select(choices=[('', 'Koordinator')] + list(DataKoordinator.objects.values_list('id', 'nama')))
    
    def clean(self):
        cleaned_data = super().clean()
        # Tambahkan validasi khusus jika diperlukan
        return cleaned_data
    
from django import forms
from .models import PengaturanWilayah

class PengaturanWilayahForm(forms.ModelForm):
    class Meta:
        model = PengaturanWilayah
        fields = '__all__'
        labels = {
            'kabupaten_bangka': 'Kabupaten Bangka',
            'kabupaten_bangka_selatan': 'Kabupaten Bangka Selatan',
            'kabupaten_bangka_tengah': 'Kabupaten Bangka Tengah',
            'kabupaten_bangka_barat': 'Kabupaten Bangka Barat',
            'kota_pangkal_pinang': 'Kota Pangkal Pinang',
            'kabupaten_belitung': 'Kabupaten Belitung',
            'kabupaten_belitung_timur': 'Kabupaten Belitung Timur',
            # Tambahkan label lain jika perlu
        }
        # Tambahkan field lain jika perlu

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    
from .models import DataPemilu

class DataPemiluForm(forms.ModelForm):
    class Meta:
        model = DataPemilu
        fields = ['calon_1_2024', 'total_suara_2024', ]

