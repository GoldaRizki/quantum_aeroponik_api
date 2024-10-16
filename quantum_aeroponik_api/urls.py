"""
URL configuration for quantum_aeroponik_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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

from django.urls import include, path   
from django.contrib import admin
from django.urls import path
from service_api import views as service_api_views



urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),

    path('sensor/get', service_api_views.data_terakhir, name='ambil_data'),
    path('sensor/get/sehari', service_api_views.data_sehari, name='data_sehari'),
    path('sensor/post', service_api_views.baca_sensor, name='upload_nilai_sensor'),


    path('setting/get', service_api_views.baca_konfigurasi, name='baca_konfigurasi'),
    path('setting/post', service_api_views.set_konfigurasi, name='upload_nilai_konfigurasi')

]
