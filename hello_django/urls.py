"""hello_django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from first_app.views import *

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', index),
    url(r'^get_json/$', ret_json_data),
    url(r'^inser_data', insert_data),
    url(r'^get_data', get_data),
    url(r'^upload_data', upload_data),
    url(r'^save_data', save_data),
    url(r'^upload_script', upload_script),
    url(r'^handout_script', handout_script),
    url(r'^scan_host', scan_host),
    url(r'^upload_file', upload_file),
    url(r'^deal_upload_file', deal_upload_file),
    url(r'^search_host_info', search_host_info),
    url(r'^get_host_info', get_host_info),
]
