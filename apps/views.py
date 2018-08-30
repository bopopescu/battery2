from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.views.generic.base import View
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.core import serializers
from django.db.models import Sum

# from apps import cellDeviceTable
from django.views.decorators.csrf import csrf_exempt
import json, decimal
from datetime import datetime

import time

from .backend_db_interface import *

current_milli_time = lambda: int(round(time.time() * 1000))


# Create your views here.


def get_b_c_num(request):
    data = get_box_info_interface()
    return JsonResponse(data)


def monitor(request):
    return render(request, 'monitor.html')


def gas_control(request):
    return render(request, 'gas_control.html')


def oven_control(request):
    return render(request, 'oven_control.html')


# todo
def testline_status(request, box_num, channel_num):
    # run/pause/stop
    testid = testInfoTable.objects.filter(boxID=box_num, chnNum=channel_num)
    if len(testid) == 0:
        print("找不到测试信息")
        data = {"testline_status": "err"}
        return JsonResponse(data)
    elif len(testid) > 1:
        print("当前通道有多条测试记录，选取最后一条")
    testid = testid.order_by("id").reverse()[0]
    try:
        crd = cellTestRealDataTable.objects.get(testID=testid)
        cs = crd.currState
    except:
        print("haha")
        cs = "stop"
    data = {"testline_status": cs}
    return JsonResponse(data)


def oven_status(request):
    data = get_oven_status_interface()
    return JsonResponse(data)


def cells_info(request):
    data = get_cells_info_interface()
    return JsonResponse(data)


def tests_info(request):
    data = get_tests_info_interface()
    return JsonResponse(data)


def get_testdata_from_start(request, box_num, channel_num):
    # 获取从测试开始的数据，返回一个具有多时间的数组
    # select scheme_num from scheme_table where box_num,channel_num
    # select data from history_data_table where box_num,channel_num,scheme_num
    # send data

    # data={"name": time.UTC(), "value":[UTC , value]}
    ##test
    data = get_history_test_data_interface(box_num, channel_num,
                                           test_id=get_latest_testid_interface(box_num, channel_num))
    ##test

    return JsonResponse(data)


def get_testdata_real_time(request, box_num, channel_num):
    # 获取实时数据，返回一条当前时间点的数据
    # data={"name": time.UTC(), "value":[UTC , value]}
    data = {
        'I': {"name": current_milli_time(), "value": [current_milli_time(), 1000]},
        'U': {"name": current_milli_time(), "value": [current_milli_time(), 2000]},
        'Q_N2': {"name": current_milli_time(), "value": [current_milli_time(), 100]},
        'Q_H2': {"name": current_milli_time(), "value": [current_milli_time(), 150]},
        'Q_CO2': {"name": current_milli_time(), "value": [current_milli_time(), 200]},
        'Q_CH4': {"name": current_milli_time(), "value": [current_milli_time(), 50]},
        'Q_Air': {"name": current_milli_time(), "value": [current_milli_time(), 25]},
        'Q_H2O': {"name": current_milli_time(), "value": [current_milli_time(), 10]},
        'T1': {"name": current_milli_time(), "value": [current_milli_time(), 1073]},
    }

    ##test
    data = get_real_time_test_data_interface(box_num, channel_num)
    ##test
    return JsonResponse(data)


def testline_info(request, box_num, channel_num):
    data = get_real_time_info_interface(box_num, channel_num)
    return JsonResponse(data)


def get_test_scheme(request, box_num, channel_num):
    # select * from schemeTable where box_num channel_num
    steps = []
    data = {
        "schemeID": 1,
        "steps": steps
    }
    data = get_current_scheme_interface(box_num, channel_num)
    return JsonResponse(data)


def control(request):
    return render(request, 'load_control.html')


def get_old_oven_scheme(request):
    ##test
    data = get_old_oven_test_scheme_interface()
    ##test
    return JsonResponse(data)


def get_old_scheme(request):
    ##test
    data = get_old_test_scheme_interface()
    ##test
    return JsonResponse(data)


def delete_old_scheme(request, num):
    return JsonResponse({"Message": "unknown"})


def delete_old_oven_scheme(request, num):
    return JsonResponse({"Message": "unknown"})


@csrf_exempt
def save_scheme(request):
    print(request.body)
    print(json.loads(request.body.decode()))
    scheme = json.loads(request.body.decode())
    if save_test_scheme_interface(scheme):
        print("保存成功")
        message = "保存成功"
    else:
        print("保存过程中出错")
        message = "保存过程中出错"
    return JsonResponse({"Message":message})


@csrf_exempt
def save_oven_scheme(request):
    print(request.body)
    print(json.loads(request.body.decode()))
    scheme = json.loads(request.body.decode())
    if save_oven_test_scheme_interface(scheme):
        print("保存成功")
        message = "保存成功"
    else:
        print("保存过程中出错")
        message = "保存过程中出错"
    return JsonResponse({"Message":message})


@csrf_exempt
def start_channel(request):
    datarecv = json.loads(request.body.decode())
    print(datarecv)
    message=start_channel_interface(datarecv['box'], datarecv['channel'], datarecv['plan'])
    return JsonResponse({"Message":message})


@csrf_exempt
def start_oven(request):
    datarecv = json.loads(request.body.decode())
    print(datarecv)
    message=start_oven_interface(datarecv['box'], datarecv['channel'], datarecv['oven'], datarecv['oplan'])
    return JsonResponse({"Message":message})


@csrf_exempt
def stop_oven(request):
    datarecv = json.loads(request.body.decode())
    print(datarecv)
    message=stop_oven_interface(datarecv['box'], datarecv['channel'], datarecv['oven'], datarecv['oplan'])
    return JsonResponse({"Message":message})


@csrf_exempt
def pause_oven(request):
    datarecv = json.loads(request.body.decode())
    print(datarecv)
    message=pause_oven_interface(datarecv['box'], datarecv['channel'], datarecv['oven'], datarecv['oplan'])
    return JsonResponse({"Message":message})


@csrf_exempt
def resume_oven(request):
    datarecv = json.loads(request.body.decode())
    print(datarecv)
    message=resume_oven_interface(datarecv['box'], datarecv['channel'], datarecv['oven'], datarecv['oplan'])
    return JsonResponse({"Message":message})


@csrf_exempt
def make_test(request):
    datarecv = json.loads(request.body.decode())
    print(datarecv)
    make_test_interface(datarecv['box'], datarecv['channel'], datarecv['plan'], datarecv['oplan'])
    return JsonResponse({})


@csrf_exempt
def pause_channel(request):
    datarecv = json.loads(request.body.decode())
    print(datarecv)
    message=pause_channel_interface(datarecv['box'], datarecv['channel'])
    return JsonResponse({"Message":message})


@csrf_exempt
def stop_channel(request):
    datarecv = json.loads(request.body.decode())
    print(datarecv)
    message=stop_channel_interface(datarecv['box'], datarecv['channel'])
    return JsonResponse({"Message":message})


@csrf_exempt
def continue_channel(request):
    datarecv = json.loads(request.body.decode())
    print(datarecv)
    message=continue_channel_interface(datarecv['box'], datarecv['channel'])
    return JsonResponse({"Message":message})


def get_gas_info(request, box_id, chn_id):
    data = get_gas_info_interface(box_id, chn_id)
    return JsonResponse(data)


@csrf_exempt
def set_gas(request, box_id, chn_id):
    datarecv = json.loads(request.body.decode())
    print(datarecv)
    if set_gas_interface(box_id, chn_id, datarecv):
        print("气体设置成功")
        message="气体设置成功"
    else:
        print("气体设置失败！")
        message="气体设置失败"
    return JsonResponse({"Message":message})


class IndexView(View):
    def get(self, request):
        customer = 'finacial'
        # return render(request, "monitor.html")
        return render(request, "index.html", {
            "customer": customer,
        })
