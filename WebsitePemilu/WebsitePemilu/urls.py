"""
URL configuration for WebsitePemilu project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Pemilu.views import *
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashboard/', dashboard, name= 'dashboard'),
    path('', redirect_to_login),
    path('login/', user_login, name='login_user'),
    path('logout/', user_logout, name='logout_user'),
    path('daftar-pemilih', daftar_pemilih, name='daftar_pemilih'),
    path('data-pemilih/', data_pemilih, name= 'data_pemilih'),
    path('data-koordinator/', data_koordinator, name= 'data_koordinator'),
    path('verifikasi-nik/', verifikasi_nik, name='verifikasi_nik'),
    path('edit-koordinator/<int:coordinator_id>/', edit_koordinator, name='edit_koordinator'),
    path('delete-koordinator/<int:coordinator_id>/', delete_koordinator, name='delete_koordinator'),
    path('tambah-koordinator/', tambah_koordinator, name='tambah_koordinator'),
    path('tambah-pemilih/', tambah_pemilih, name='tambah_pemilih'),
    path('delete-pemilih/<int:pemilih_id>/', delete_pemilih, name='delete_pemilih'),
    path('edit-pemilih/<int:pemilih_id>/', edit_pemilih, name='edit_pemilih'),
    path('filter-data-pemilih/', filter_data_pemilih, name='filter_data_pemilih'),
    path('filter-data-koordinator/', filter_data_koordinator, name='filter_data_koordinator'),
    path('unduh-data-pemilih/', unduh_data_pemilih, name='unduh_data_pemilih'),
    path('unduh-data-koordinator/', unduh_data_koordinator, name='unduh_data_koordinator'),
    path('data-wilayah/', data_wilayah_view, name='data_wilayah'),
    path('setting/', setting_page, name='setting_page'),
    path('analisa/', analisa, name='analisa'),
    path('list-wilayah/', list_wilayah, name='list_wilayah'),
    path('isi-hasil-pemilu/<str:kecamatan_name>/<str:kelurahan_name>/', isi_hasil_pemilu, name='isi_hasil_pemilu'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
