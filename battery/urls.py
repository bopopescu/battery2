"""battery URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.conf.urls import url, include
from django.conf import settings

import apps.views
from apps.views import IndexView, monitor, control, testline_status, testline_info, \
    get_testdata_from_start, get_testdata_real_time, get_test_scheme, get_old_scheme, delete_old_scheme, save_scheme, \
    get_b_c_num, start_channel, pause_channel, stop_channel, continue_channel, get_old_oven_scheme, \
    delete_old_oven_scheme, save_oven_scheme, make_test, start_oven, get_gas_info, set_gas, gas_control, oven_control, \
    stop_oven, pause_oven
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^users/', include('django.contrib.auth.urls')),
    url('^$', IndexView.as_view(), name="index"),
    url(r'^setting/$', TemplateView.as_view(template_name="setting.html"), name="setting"),

    url(r'^get_b_c_num/$', get_b_c_num, name="get_b_c_num"),

    url(r'^monitor/$', monitor, name="monitor"),
    url(r'^monitor/testline_status/(\d+)/(\d+)/$', testline_status, name="get_status"),
    url(r'^monitor/testline_info/(\d+)/(\d+)/$', testline_info, name="get_info"),
    url(r'^monitor/get_testdata_from_start/(\d+)/(\d+)/$', get_testdata_from_start, name="get_testdata_from_start"),
    url(r'^monitor/get_testdata_real_time/(\d+)/(\d+)/$', get_testdata_real_time, name="get_testdata_real_time"),
    url(r'^monitor/get_test_scheme/(\d+)/(\d+)/$', get_test_scheme, name="get_test_scheme"),

    url(r'^control/$', control, name="control"),
    url(r'^control/get_old_scheme/$', get_old_scheme, name="get_old_scheme"),
    url(r'^control/delete_old_scheme/$', delete_old_scheme, name="delete_old_scheme"),
    url(r'^control/save_scheme/$', save_scheme, name="save_scheme"),

    url(r'^control/get_old_oven_scheme/$', get_old_oven_scheme, name="get_old_oven_scheme"),
    url(r'^control/delete_old_oven_scheme/$', delete_old_oven_scheme, name="delete_old_oven_scheme"),
    url(r'^control/save_oven_scheme/$', save_oven_scheme, name="save_oven_scheme"),

    url(r'^control/start_channel/$', start_channel, name="start_channel"),
    url(r'^control/stop_channel/$', stop_channel, name="stop_channel"),
    url(r'^control/pause_channel/$', pause_channel, name="pause_channel"),
    url(r'^control/continue_channel/$', continue_channel, name="continue_channel"),
    url(r'^control/make_test/$', make_test, name="make_test"),
    url(r'^control/start_oven/$', start_oven, name="start_oven"),
    url(r'^control/stop_oven/$', stop_oven, name="stop_oven"),
    url(r'^control/pause_oven/$', pause_oven, name="pause_oven"),
    url(r'^control/get_gas_info/(\d+)/(\d+)/$', get_gas_info, name="get_gas_info"),
    url(r'^control/set_gas/(\d+)/(\d+)/$', set_gas, name="set_gas"),
    url(r'^gas_control/$', gas_control, name="gas_control"),
    url(r'^oven_control/$', oven_control, name="oven_control"),
]
