from .models import *
import datetime
from datetime import timezone
from datetime import timedelta
import datetime
import time

# 设置时区
TZ = 8


def get_current_scheme_interface(bid, cid):
    # 获取数据库中的测试方案数据
    if len(cellTestRealDataTable.objects.filter(boxID=bid, chnNum=cid)) == 0:
        print("当前通道无正在进行的测试")
        return {"schemeID": 0, "steps": []}
    tid = cellTestRealDataTable.objects.filter(boxID=bid, chnNum=cid)[0].testID
    if tid is None:
        return {"schemeID": 0, "steps": []}
    if len(testInfoTable.objects.filter(id=tid.id)) == 0:
        print("err1")
        return {"schemeID": 0, "steps": []}
    sid = testInfoTable.objects.filter(id=tid.id)[0].planID
    steps = cellPlanDetailTable.objects.filter(planID=sid).order_by("step")
    step_list = []
    if len(steps) != 0:
        for j in steps:
            step = {
                "step": j.step,
                "LoadMode": j.mode,
                "U": float(j.u) / 1000,
                "I": float(j.i) / 1000,
                "t_LM": float(j.tTH) / 1000,
                "U_LM": float(j.uTH) / 1000,
                "I_LM": float(j.iTH) / 1000,
            }
        step_list.append(step)
    data = {
        "schemeID": int(sid.id),
        "steps": step_list
    }
    return data


def get_oven_status_interface():
    ovens = ovenDeviceTable.objects.all()
    data = []
    for i in ovens:
        oven = {
            "ID": i.ID,
            "curr": i.currState,
            "next": i.nextState,
            "PlanID": i.ovenPlanID.id
        }
        bt = BigTestInfoTable.objects.filter(ovenID=i.ID, completeFlag=0)
        if len(bt) == 0:
            oven["T"] = -1
        else:
            crt = cellTestRealDataTable.objects.filter(bigTestID=bt[0])
            if len(crt) == 0:
                oven["T"] = -1
            else:
                oven["T"] = crt[0].T0
        data.append(oven)
    return {"oven": data}


def get_cells_info_interface():
    cells = cellDeviceTable.objects.all()
    data = []
    if len(cells) == 0:
        return {"cells": data}
    else:
        for c in cells:
            cell = {
                "cellID": c.cellID,
                "boxID": c.boxID.ID if c.boxID else None,
                "chnNum": c.chnNum,
                "ovenID": c.mT0ID.ID if c.mT0ID else None,
                "H2ID": c.mH2ID.ID if c.mH2ID else None,
                "H2OID": c.mH2OID.ID if c.mH2OID else None,
                "N2ID": c.mN2ID.ID if c.mN2ID else None,
                "CO2ID": c.mCO2ID.ID if c.mCO2ID else None,
                "CH4ID": c.mCH4ID.ID if c.mCH4ID else None,
                "AIRID": c.mAIRID.ID if c.mAIRID else None,
                "wdjID": c.mT1ID.ID if c.mT1ID else None
            }
            data.append(cell)
        return {"cells": data}


def get_tests_info_interface():
    bts = BigTestInfoTable.objects.all()
    data = []
    if len(bts) == 0:
        return {"tests": data}
    else:
        for bt in bts:
            sts = testInfoTable.objects.filter(bigTestID=bt)
            if len(sts) == 0:
                t = {
                    "BigTestID": bt.id,
                    "TestID": None,
                    "CellID": None,
                    "BoxID": None,
                    "ChnID": None,
                    "PlanID": None,
                    "OvenID": bt.ovenID.ID if bt.ovenID else None,
                    "OvenPlanID": bt.ovenPlanID.id if bt.ovenPlanID else None,
                    "H2ID": bt.H2ID.ID if bt.H2ID else None,
                    "H2OID": bt.H2OID.ID if bt.H2OID else None,
                    "N2ID": bt.N2ID.ID if bt.N2ID else None,
                    "CO2ID": bt.CO2ID.ID if bt.CO2ID else None,
                    "CH4ID": bt.CH4ID.ID if bt.CH4ID else None,
                    "AIRID": bt.AIRID.ID if bt.AIRID else None,
                    "StartTime": bt.startDate,
                    "EndTime": bt.endDate
                }
                data.append(t)
            else:
                for st in sts:
                    t = {
                        "BigTestID": bt.id,
                        "TestID": st.id,
                        "CellID": st.cellID.cellID if st.cellID else None,
                        "BoxID": st.boxID.ID if st.boxID else None,
                        "ChnID": st.chnNum,
                        "PlanID": st.planID.id if st.planID else None,
                        "OvenID": bt.ovenID.ID if bt.ovenID else None,
                        "OvenPlanID": bt.ovenPlanID.id if bt.ovenPlanID else None,
                        "H2ID": bt.H2ID.ID if bt.H2ID else None,
                        "H2OID": bt.H2OID.ID if bt.H2OID else None,
                        "N2ID": bt.N2ID.ID if bt.N2ID else None,
                        "CO2ID": bt.CO2ID.ID if bt.CO2ID else None,
                        "CH4ID": bt.CH4ID.ID if bt.CH4ID else None,
                        "AIRID": bt.AIRID.ID if bt.AIRID else None,
                        "wdjID": bt.wdjID.ID if bt.wdjID else None,
                        "StartTime": st.startDate,
                        "EndTime": st.endDate
                    }
                    data.append(t)
        return {"tests": data}


def get_old_oven_test_scheme_interface():
    # 获取数据库中的测试方案数据
    schemes = ovenPlanDetailTable.objects.values('ovenPlanID').distinct()
    scheme_num = len(schemes)
    scheme_list = []
    for i in schemes:
        step_list = []
        steps = ovenPlanDetailTable.objects.filter(ovenPlanID=i['ovenPlanID']).order_by('step')
        for j in steps:
            step = {
                "step": j.step,
                "T": j.T,
                "time": j.time,
            }
            step_list.append(step)
        scheme = {
            "id": i['ovenPlanID'],
            "name": ovenPlanTable.objects.filter(id=i['ovenPlanID']).values("name").distinct()[0]['name'],
            "steps": step_list
        }
        scheme_list.append(scheme)
    data = {
        "old_scheme_num": scheme_num,
        "old_scheme_list": scheme_list
    }
    return data


def get_old_test_scheme_interface():
    # 获取数据库中的测试方案数据
    schemes = cellPlanDetailTable.objects.values('planID').distinct()
    scheme_num = len(schemes)
    scheme_list = []
    for i in schemes:
        step_list = []
        steps = cellPlanDetailTable.objects.filter(planID=i['planID']).order_by('step')
        for j in steps:
            step = {
                "step": j.step,
                "LoadMode": j.mode,
                "U": float(j.u) / 1000,
                "I": float(j.i) / 1000,
                "t_LM": float(j.tTH) / 1000,
                "U_LM": float(j.uTH) / 1000,
                "I_LM": float(j.iTH) / 1000,
            }
            step_list.append(step)
        scheme = {
            "id": i['planID'],
            "name": cellPlanTable.objects.filter(id=i['planID'])[0].name,
            "steps": step_list
        }
        scheme_list.append(scheme)
    data = {
        "old_scheme_num": scheme_num,
        "old_scheme_list": scheme_list
    }
    return data


def save_test_scheme_interface(new_scheme):
    # 传入参数为新的测试方案，存入数据库
    planid = cellPlanTable.objects.values("id")
    if len(planid) == 0:
        newid = 1
        planinfo = cellPlanTable.objects.create(id=newid, name=new_scheme['name'], steps=len(new_scheme['steps']))
    else:
        maxid = planid.order_by("id").reverse()[0]['id']
        newid = maxid + 1
        planinfo = cellPlanTable.objects.create(id=newid, name=new_scheme['name'], steps=len(new_scheme['steps']))
    steps = new_scheme['steps']
    flag = True
    for i in steps:
        try:
            step = cellPlanDetailTable()
            step.planID = planinfo
            step.step = 0 if i['step'] is None else int(i['step'])
            step.mode = "" if i['LoadMode'] is None else i['LoadMode']
            step.i = 0 if i['I'] is None else int(i['I']) * 1000
            step.u = 0 if i['U'] is None else int(i['U']) * 1000
            step.iTH = 0 if i['I_LM'] is None else int(i['I_LM']) * 1000
            step.uTH = 0 if i['U_LM'] is None else int(i['U_LM']) * 1000
            step.tTH = 0 if i['t_LM'] is None else int(i['t_LM']) * 1000
        except Exception as e:
            print(e)
            print("出错啦 ")
            flag = False
            break
        step.save()

    return flag


def save_oven_test_scheme_interface(new_scheme):
    # 传入参数为新的测试方案，存入数据库
    planid = ovenPlanTable.objects.values("id")
    if len(planid) == 0:
        newid = 1
        planinfo = ovenPlanTable.objects.create(id=newid, name=new_scheme['name'], steps=len(new_scheme['steps']))
    else:
        maxid = planid.order_by("id").reverse()[0]['id']
        newid = maxid + 1
        planinfo = ovenPlanTable.objects.create(id=newid, name=new_scheme['name'], steps=len(new_scheme['steps']))
    steps = new_scheme['steps']
    flag = True
    for i in steps:
        try:
            step = ovenPlanDetailTable()
            step.ovenPlanID = planinfo
            step.step = 0 if i['step'] is None else int(i['step'])
            step.T = 0 if i['T'] is None else int(i['T'])
            step.time = 0 if i['time'] is None else int(i['time'])
        except:
            print("出错啦 ")
            flag = False
            break
        step.save()

    return flag


def delete_test_scheme_interface(schemeID):
    return


def get_box_info_interface():
    # 给出所有接着电池的箱号以及对应通道号
    box_list = []
    oven_list = []
    boxes = cellDeviceTable.objects.values('boxID').distinct()
    if len(boxes) == 0:
        print("没有任何箱号")
    #        return {"box": box_list}
    else:
        for i in boxes:
            bid = i['boxID']
            channels = cellDeviceTable.objects.filter(boxID=bid).values('chnNum').distinct()
            channel_list = []
            for j in channels:
                channel_list.append(j['chnNum'])
            box = {
                "id": bid,
                "channel": channel_list
            }
            box_list.append(box)
    ovens = ovenDeviceTable.objects.all()
    if len(ovens) == 0:
        print("没有任何电炉")
    else:
        for i in ovens:
            oven = {"id": i.ID}
            oven_list.append(oven)
    data = {"box": box_list, "oven": oven_list}
    return data


def get_real_time_test_data_interface(box_id, cha_id):
    # 获取给定通道的实时数据
    # 首先获取该通道的最近测试ID
    test_id = get_latest_testid_interface(box_id, cha_id)
    data = {
        'I': {},
        'U': {},
        'Q_N2': {},
        'Q_H2': {},
        'Q_CO2': {},
        'Q_CH4': {},
        'Q_Air': {},
        'Q_H2O': {},
        'T0': {},
        'T1': {},
        'T2': {},
        'T3': {},
        'T4': {},
    }
    if test_id == -1:
        return data
    try:
        rt_data = cellTestRealDataTable.objects.get(testID=test_id)  # 数据的时间戳是秒级，而js默认是ms级，因此需要*1000
    except:
        print("boxID:" + str(box_id) + "  chaID:" + str(cha_id) + "  testID:" + str(test_id) + "    不存在实时数据")
        return data

    data = {
        'I': {"name": int(rt_data.celldata_time.replace(tzinfo=timezone(timedelta(hours=TZ))).timestamp() * 1000),
              "value": [int(rt_data.celldata_time.replace(tzinfo=timezone(timedelta(hours=TZ))).timestamp() * 1000),
                        float(rt_data.i) / 1000]},
        'U': {"name": int(rt_data.celldata_time.replace(tzinfo=timezone(timedelta(hours=TZ))).timestamp() * 1000),
              "value": [int(rt_data.celldata_time.replace(tzinfo=timezone(timedelta(hours=TZ))).timestamp() * 1000),
                        float(rt_data.u) / 1000]},
        'Q_N2': {"name": int(rt_data.tN2.replace(tzinfo=timezone(timedelta(hours=TZ))).timestamp() * 1000),
                 "value": [int(rt_data.tN2.replace(tzinfo=timezone(timedelta(hours=TZ))).timestamp() * 1000),
                           rt_data.qN2]},
        'Q_H2': {"name": int(rt_data.tH2.replace(tzinfo=timezone(timedelta(hours=TZ))).timestamp() * 1000),
                 "value": [int(rt_data.tH2.replace(tzinfo=timezone(timedelta(hours=TZ))).timestamp() * 1000),
                           rt_data.qH2]},
        'Q_CO2': {"name": int(rt_data.tCO2.replace(tzinfo=timezone(timedelta(hours=TZ))).timestamp() * 1000),
                  "value": [int(rt_data.tCO2.replace(tzinfo=timezone(timedelta(hours=TZ))).timestamp() * 1000),
                            rt_data.qCO2]},
        'Q_CH4': {"name": int(rt_data.tCH4.replace(tzinfo=timezone(timedelta(hours=TZ))).timestamp() * 1000),
                  "value": [int(rt_data.tCH4.replace(tzinfo=timezone(timedelta(hours=TZ))).timestamp() * 1000),
                            rt_data.qCH4]},
        'Q_Air': {"name": int(rt_data.tAIR.replace(tzinfo=timezone(timedelta(hours=TZ))).timestamp() * 1000),
                  "value": [int(rt_data.tAIR.replace(tzinfo=timezone(timedelta(hours=TZ))).timestamp() * 1000),
                            rt_data.qAIR]},
        'Q_H2O': {"name": int(rt_data.tH2O.replace(tzinfo=timezone(timedelta(hours=TZ))).timestamp() * 1000),
                  "value": [int(rt_data.tH2O.replace(tzinfo=timezone(timedelta(hours=TZ))).timestamp() * 1000),
                            rt_data.qH2O]},
        'T0': {"name": int(rt_data.tT0.timestamp() * 1000),
               "value": [int(rt_data.tT0.replace(tzinfo=timezone(timedelta(hours=TZ))).timestamp() * 1000),
                         float(rt_data.T0)]},
        'T1': {"name": int(rt_data.tT1.timestamp() * 1000),
               "value": [int(rt_data.tT1.replace(tzinfo=timezone(timedelta(hours=TZ))).timestamp() * 1000),
                         float(rt_data.T1)]},
        'T2': {"name": int(rt_data.tT2.timestamp() * 1000),
               "value": [int(rt_data.tT2.replace(tzinfo=timezone(timedelta(hours=TZ))).timestamp() * 1000),
                         float(rt_data.T2)]},
        'T3': {"name": int(rt_data.tT3.timestamp() * 1000),
               "value": [int(rt_data.tT3.replace(tzinfo=timezone(timedelta(hours=TZ))).timestamp() * 1000),
                         float(rt_data.T3)]},
        'T4': {"name": int(rt_data.tT4.timestamp() * 1000),
               "value": [int(rt_data.tT4.replace(tzinfo=timezone(timedelta(hours=TZ))).timestamp() * 1000),
                         float(rt_data.T4)]},
    }
    return data


def get_history_test_data_interface(box_id, cha_id, test_id):
    # 获取给定通道，给定测试id的历史数据
    ## bug:数据必须按照时间顺序排列 否则显示会有问题
    hs_data = cellTestHistoryDataTable.objects.filter(testID=test_id).order_by("celldata_time")
    data = {
        'I': [],
        'U': [],
        'Q_N2': [],
        'Q_H2': [],
        'Q_CO2': [],
        'Q_CH4': [],
        'Q_Air': [],
        'Q_H2O': [],
        'T1': [],
        'T2': [],
        'T3': [],
        'T4': [],
    }
    if len(hs_data) == 0:
        print("boxID:" + str(box_id) + "  chaID:" + str(cha_id) + "  testID:" + str(test_id) + "    不存在历史数据")
        return data
    for i in hs_data:
        data['I'].append({
            "name": int(i.celldata_time.replace(tzinfo=timezone(timedelta(hours=TZ))).timestamp() * 1000),
            "value": [int(i.celldata_time.replace(tzinfo=timezone(timedelta(hours=TZ))).timestamp() * 1000),
                      float(i.i) / 1000]})
        data['U'].append({
            "name": int(i.celldata_time.replace(tzinfo=timezone(timedelta(hours=TZ))).timestamp() * 1000),
            "value": [int(i.celldata_time.replace(tzinfo=timezone(timedelta(hours=TZ))).timestamp() * 1000),
                      float(i.u) / 1000]})
        data['Q_N2'].append({
            "name": int(i.tN2.replace(tzinfo=timezone(timedelta(hours=TZ))).timestamp() * 1000),
            "value": [int(i.tN2.replace(tzinfo=timezone(timedelta(hours=TZ))).timestamp() * 1000), i.qN2]})
        data['Q_H2'].append({
            "name": int(i.tH2.replace(tzinfo=timezone(timedelta(hours=TZ))).timestamp() * 1000),
            "value": [int(i.tH2.replace(tzinfo=timezone(timedelta(hours=TZ))).timestamp() * 1000), i.qH2]})
        data['Q_CO2'].append({
            "name": int(i.tCO2.replace(tzinfo=timezone(timedelta(hours=TZ))).timestamp() * 1000),
            "value": [int(i.tCO2.replace(tzinfo=timezone(timedelta(hours=TZ))).timestamp() * 1000), i.qCO2]})
        data['Q_CH4'].append({
            "name": int(i.tCH4.replace(tzinfo=timezone(timedelta(hours=TZ))).timestamp() * 1000),
            "value": [int(i.tCH4.replace(tzinfo=timezone(timedelta(hours=TZ))).timestamp() * 1000), i.qCH4]})
        data['Q_Air'].append({
            "name": int(i.tAIR.replace(tzinfo=timezone(timedelta(hours=TZ))).timestamp() * 1000),
            "value": [int(i.tAIR.replace(tzinfo=timezone(timedelta(hours=TZ))).timestamp() * 1000), i.qAIR]})
        data['Q_H2O'].append({
            "name": int(i.tH2O.replace(tzinfo=timezone(timedelta(hours=TZ))).timestamp() * 1000),
            "value": [int(i.tH2O.replace(tzinfo=timezone(timedelta(hours=TZ))).timestamp() * 1000), i.qH2O]})
        data['T0'].append({
            "name": int(i.tT0.replace(tzinfo=timezone(timedelta(hours=TZ))).timestamp() * 1000),
            "value": [int(i.tT0.replace(tzinfo=timezone(timedelta(hours=TZ))).timestamp() * 1000), float(i.T0)]})
        data['T1'].append({
            "name": int(i.tT1.replace(tzinfo=timezone(timedelta(hours=TZ))).timestamp() * 1000),
            "value": [int(i.tT1.replace(tzinfo=timezone(timedelta(hours=TZ))).timestamp() * 1000), float(i.T1)]})
        data['T2'].append({
            "name": int(i.tT2.replace(tzinfo=timezone(timedelta(hours=TZ))).timestamp() * 1000),
            "value": [int(i.tT2.replace(tzinfo=timezone(timedelta(hours=TZ))).timestamp() * 1000), float(i.T2)]})
        data['T3'].append({
            "name": int(i.tT3.replace(tzinfo=timezone(timedelta(hours=TZ))).timestamp() * 1000),
            "value": [int(i.tT3.replace(tzinfo=timezone(timedelta(hours=TZ))).timestamp() * 1000), float(i.T3)]})
        data['T4'].append({
            "name": int(i.tT4.replace(tzinfo=timezone(timedelta(hours=TZ))).timestamp() * 1000),
            "value": [int(i.tT4.replace(tzinfo=timezone(timedelta(hours=TZ))).timestamp() * 1000), float(i.T4)]})
    return data


def get_real_time_info_interface(box_id, cha_id):
    test_id = get_latest_testid_interface(box_id, cha_id)
    data = {
        "I": 0,
        "U": 0,
        "T0": 0,
        "T1": 0,
        "T2": 0,
        "T3": 0,
        "T4": 0,
        "Q_H2": 0,
        "Q_CO2": 0,
        "Q_N2": 0,
        "Q_CH4": 0,
        "Q_Air": 0,
        "Q_H2O": 0,
        "q": 0,
        "k": 0
    }
    if test_id == -1:
        return data
    try:
        rt_data = cellTestRealDataTable.objects.get(testID=test_id)  # 数据的时间戳是秒级，而js默认是ms级，因此需要*1000
    except:
        print("boxID:" + str(box_id) + "  chaID:" + str(cha_id) + "  testID:" + str(test_id) + "    不存在实时信息")
        return data
    data['I'] = float(rt_data.i) / 1000
    data['U'] = float(rt_data.u) / 1000
    data['T0'] = float(rt_data.T0)
    data['T1'] = float(rt_data.T1)
    data['T2'] = float(rt_data.T2)
    data['T3'] = float(rt_data.T3)
    data['T4'] = float(rt_data.T4)
    data['Q_N2'] = rt_data.qN2
    data['Q_H2'] = rt_data.qH2
    data['Q_CO2'] = rt_data.qCO2
    data['Q_CH4'] = rt_data.qCH4
    data['Q_Air'] = rt_data.qAIR
    data['Q_H2O'] = rt_data.qH2O
    data['q'] = rt_data.q
    data['k'] = rt_data.n
    return data


def get_latest_testid_interface(box_id, cha_id):
    # 获取给定通道的当前测试id
    # 假定最近的id存在最后面，即test_id只会递增
    try:
        test_id = testInfoTable.objects.filter(boxID=box_id, chnNum=cha_id).order_by('id').reverse()[0].id
    except:
        print("boxID:" + str(box_id) + "  chaID:" + str(cha_id) + "    还没有进行过测试")
        return -1
    return test_id


def get_schemeid_interface(box_id, cha_id, test_id):
    # 获取给定测试的测试id
    pass


def start_channel_interface(box_id, cha_id, scheme_id):
    # cellid = cellDeviceTable.objects.filter(boxID=box_id, chnNum=cha_id).order_by('cellID').reverse()
    cellid = cellTestRealDataTable.objects.filter(boxID=box_id, chnNum=cha_id)
    if len(cellid) == 0:
        # print("当前通道下找不到电池")
        print("startchannel:当前通道还未创建realdatatable")
        return False
    cellid = cellid[0].cellID
    bigtest = BigTestInfoTable.objects.filter(cellID=cellid, boxID=box_id, chnNum=cha_id, completeFlag=0).order_by(
        "startDate").reverse()
    if len(bigtest) == 0:
        print("startchannel:还没有创建bigtest!")
        return False
    bigtest = bigtest[0]
    try:
        planid = cellPlanTable.objects.get(id=scheme_id)
    except:
        print("startchannel:找不到测试方案！")
        return False
    try:
        box_id = boxDeviceTable.objects.get(ID=box_id)
    except:
        print("startchannel:没有该box")
        return False
    testid = testInfoTable(boxID=box_id, chnNum=cha_id, bigTestID=bigtest, planID=planid, cellID=cellid, completeFlag=0,
                           startDate=datetime.datetime.now())
    testid.save()
    steps = cellPlanDetailTable.objects.filter(id=scheme_id).order_by('step')
    x = cellTestRealDataTable.objects.filter(cellID=cellid, boxID=box_id, chnNum=cha_id, currState="stop",
                                             nextState="stop")
    if len(x) == 0:
        print("启动通道：还未创建realdatatable！")
        testid.delete()
    elif len(x) > 1:
        print("启动通道：不止一条realdatatable")
        x.update(cellID=cellid, boxID=box_id, chnNum=cha_id, testID=testid, totalStepN=len(steps), currState="stop",
                 nextState="start")
    else:
        x.update(boxID=box_id, chnNum=cha_id, testID=testid, totalStepN=len(steps), currState="stop", nextState="start")


def stop_channel_interface(box_id, cha_id):
    tid = testInfoTable.objects.filter(boxID=box_id, chnNum=cha_id, completeFlag=0)
    if len(tid) == 0:
        print("stop通道：未查询到该通道的testID！")
        return False
    crt = cellTestRealDataTable.objects.filter(boxID=box_id, chnNum=cha_id, testID=tid[0], bigTestID=tid[0].bigTestID)
    if len(crt) == 0:
        print("stop通道：还未创建realdatatable！")
        return False
    elif len(crt) > 1:
        print("stop通道：多个realdatatable！")
        return False
    if crt[0].currState == "stop":
        print("stop通道：已停止！")
        if crt[0].testID is not None:
            testInfoTable.objects.filter(id=crt[0].testID.id).update(completeFlag=1, endDate=datetime.datetime.now())
            crt.update(nextState="stop", testID=None)
        return True
    if crt.nextState == "stop":
        print("stop通道：正尝试停止！")
        return False

    if crt[0].testID is not None:
        testInfoTable.objects.filter(id=crt[0].testID.id).update(completeFlag=1, endDate=datetime.datetime.now())
        crt.update(nextState="stop", testID=None)
    return True

    # testid = testInfoTable.objects.filter(boxID=box_id, chnNum=cha_id)
    # if len(testid) == 0:
    #     print("stopchannel:testid not found")
    #     return False
    # elif len(testid) > 1:
    #     print("stopchannel:当前通道有多条测试记录，选取最后一条")
    # testid = testid.order_by("id").reverse()[0]
    # rows = cellTestRealDataTable.objects.filter(testID=testid).update(nextState="stop")
    # testid.completeFlag = 1
    # testid.endDate = datetime.datetime.now()
    # return rows


def pause_channel_interface(box_id, cha_id):
    testid = testInfoTable.objects.filter(boxID=box_id, chnNum=cha_id, completeFlag=0)
    if len(testid) == 0:
        print("pausechannel:testid not found")
        return 0
    elif len(testid) > 1:
        print("pausechannel:当前通道有多条测试记录，选取最后一条")
    testid = testid.order_by("id").reverse()[0]
    rows = cellTestRealDataTable.objects.filter(testID=testid, currState="start").update(nextState="pause")
    return rows


def continue_channel_interface(box_id, cha_id):
    testid = testInfoTable.objects.filter(boxID=box_id, chnNum=cha_id, completeFlag=0)
    if len(testid) == 0:
        print("continuechannel:testid not found")
        return 0
    elif len(testid) > 1:
        print("continuechannel:当前通道有多条测试记录，选取最后一条")
    testid = testid.order_by("id").reverse()[0]
    rows = cellTestRealDataTable.objects.filter(testID=testid, currState="pause").update(nextState="resume")
    return rows


# def make_test_interface(box_id, cha_id, scheme_id, oven_scheme_id):
#     # 创建父测试
#     cellid = cellDeviceTable.objects.filter(boxID=box_id, chnNum=cha_id).order_by('cellID').reverse()[0]
#     planid = planInfoTable.objects.get(id=scheme_id)
#     oplanid = ovenPlanInfoTable.objects.get(id=oven_scheme_id)
#     testid = testInfoTable(boxID=box_id, chnNum=cha_id, planID=planid, cellID=cellid)
#     testid.save()
#     steps = planTable.objects.filter(planID=scheme_id).order_by('step')
#     x = cellRealDataTable.objects.filter(cellID=cellid)
#     if len(x) == 0:
#         crd = cellRealDataTable(cellID=cellid, boxID=box_id, chnNum=cha_id, testID=testid, planID=planid,
#                                 totalStepN=len(steps), currState="stop", nextState="stop", ovenPlanID=oplanid,
#                                 currOvenState="stop", nextOvenState="stop")
#         crd.save()
#     elif len(x) > 1:
#         print("不止一条测试")
#         x.update(boxID=box_id, chnNum=cha_id, ovenPlanID=oplanid, currOvenState="stop", nextOvenState="stop")
#     else:
#         x.update(boxID=box_id, chnNum=cha_id, ovenPlanID=oplanid, currOvenState="stop", nextOvenState="stop")


def start_oven_interface(box_id, cha_id, oven_id, oven_scheme_id):
    # 创建父测试
    try:
        ovenid = ovenDeviceTable.objects.get(ID=oven_id)
    except:
        print("startoven:没有该电炉")
        return False
    if ovenid.currState == "start":
        print("startoven:该电炉已启动")
        return False
    if ovenid.nextState == "start":
        print("startoven:该电炉正在尝试启动")
        return False
    try:
        ovenplanid = ovenPlanTable.objects.get(id=oven_scheme_id)
    except:
        print("startoven:没有该电炉测试方案")
        return False
    cell = cellDeviceTable.objects.filter(mT0ID=ovenid)
    if len(cell) == 0:
        print("startoven:该电炉里面没有电池！")
        bt = BigTestInfoTable(ovenID=ovenid, ovenPlanID=ovenplanid, completeFlag=0)
        bt.save()
        crt = cellTestRealDataTable.objects.filter(bigTestID=None, boxID=None, chnNum=None)
        if len(crt) == 0:
            crt = cellTestRealDataTable(bigTestID=bt, currState="stop", nextState="stop")
            crt.save()
        else:
            crt.update(bigTestID=bt, currState="stop", nextState="stop")
    for i in cell:
        bt = BigTestInfoTable(cellID=i, boxID=i.boxID, chnNum=i.chnNum, H2ID=i.mH2ID, N2ID=i.mN2ID, CO2ID=i.mCO2ID,
                              CH4ID=i.mCH4ID, AIRID=i.mAIRID, H2OID=i.mH2OID, ovenID=ovenid, ovenPlanID=ovenplanid,wdjID=i.mT1ID,
                              completeFlag=0)
        bt.save()
        crt = cellTestRealDataTable.objects.filter(boxID=i.boxID, chnNum=i.chnNum)
        if len(crt) == 0:
            crt = cellTestRealDataTable(cellID=i, boxID=i.boxID, chnNum=i.chnNum, bigTestID=bt, currState="stop",
                                        nextState="stop")
            crt.save()
        else:
            crt.update(cellID=i, bigTestID=bt, currState="stop", nextState="stop")
    ovenDeviceTable.objects.filter(ID=oven_id, currState="stop").update(ovenPlanID=ovenplanid, nextState="start")
    print("startoven:成功！")
    return True


def stop_oven_interface(box_id, cha_id, oven_id, oven_scheme_id):
    # 创建父测试
    print("oid" + str(oven_id))
    print("opid" + str(oven_scheme_id))
    try:
        ovenid = ovenDeviceTable.objects.get(ID=oven_id)
    except:
        print("stopoven:没有该电炉")
        return False
    if ovenid.currState == "stop" and ovenid.nextState == "stop":
        print("stopoven:该电炉已停止")
        return False
    if ovenid.nextState == "stop":
        print("stopoven:该电炉正尝试停止")
        return False
    cell = cellDeviceTable.objects.filter(mT0ID=ovenid)
    bt = BigTestInfoTable.objects.filter(ovenID=ovenid, completeFlag=0)
    if len(bt) == 1 and bt[0].cellID is None:
        cellTestRealDataTable.objects.get(bigTestID=bt[0]).delete()
    if len(testInfoTable.objects.filter(bigTestID__in=bt, completeFlag=0)) != 0:
        print("stopoven:该父测试下还有未完成的子测试，结束失败")
        return False
    ovenDeviceTable.objects.filter(ID=oven_id).update(nextState="stop")
    bt.update(completeFlag=1, endDate=datetime.datetime.now())
    return True


def pause_oven_interface(box_id, cha_id, oven_id, oven_scheme_id):
    # 创建父测试
    print("oid" + str(oven_id))
    print("opid" + str(oven_scheme_id))
    try:
        ovenid = ovenDeviceTable.objects.get(ID=oven_id)
    except:
        print("pauseoven:没有该电炉")
        return False
    if ovenid.currState == "pause":
        print("pasueoven:该电炉已暂停")
        return False
    if ovenid.nextState == "pause":
        print("pasueoven:该电炉正尝试暂停")
        return False
    cell = cellDeviceTable.objects.filter(mT0ID=ovenid)
    ovenDeviceTable.objects.filter(ID=oven_id).update(nextState="pause")
    bt = BigTestInfoTable.objects.filter(ovenID=ovenid, completeFlag=0)
    return True


def get_gas_info_interface(box_id, chn_id):
    testid = BigTestInfoTable.objects.filter(boxID=box_id, chnNum=chn_id,completeFlag=0)
    data = {'H2': -1, 'N2': -1, 'H2O': -1, 'Air': -1, 'CH4': -1, 'CO2': -1}
    if len(testid) == 0:
        print("getgasinfo:没有气体数据")
        return data
    elif len(testid) > 1:
        print("getgasinfo:当前通道有多条测试记录，选取最后一条")
    testid = testid.order_by("id").reverse()[0]
    try:
        print(testid.cellID)
        cellid = testid.cellID
    except:
        print("getgasinfo:没有找到该通道下的电池")
        return data
    data['H2'] = cellid.mH2ID.currState if cellid.mH2ID is not None else -1
    data['N2'] = cellid.mN2ID.currState if cellid.mN2ID is not None else -1
    data['H2O'] = cellid.mH2OID.currState if cellid.mH2OID is not None else -1
    data['CO2'] = cellid.mCO2ID.currState if cellid.mCO2ID is not None else -1
    data['CH4'] = cellid.mCH4ID.currState if cellid.mCH4ID is not None else -1
    data['Air'] = cellid.mAIRID.currState if cellid.mAIRID is not None else -1
    return data


def set_gas_interface(box_id, chn_id, data):
    testid = BigTestInfoTable.objects.filter(boxID=box_id, chnNum=chn_id,completeFlag=0)
    if len(testid) == 0:
        print("setgas:没有气体数据")
        return False
    elif len(testid) > 1:
        print("setgas:当前通道有多条测试记录，选取最后一条")
    testid = testid.order_by("id").reverse()[0]
    try:
        print(testid.cellID)
        cellid = testid.cellID
    except:
        print("setgas:没有找到该通道下的电池")
        return False
    if data['H2'] is not None and cellid.mH2ID is not None:
        cellid.mH2ID.nextState = data['H2']
        cellid.mH2ID.save()
    if data['N2'] is not None and cellid.mN2ID is not None:
        cellid.mN2ID.nextState = data['N2']
        cellid.mN2ID.save()
    if data['CH4'] is not None and cellid.mCH4ID is not None:
        cellid.mCH4ID.nextState = data['CH4']
        cellid.mCH4ID.save()
    if data['Air'] is not None and cellid.mAIRID is not None:
        cellid.mAIRID.nextState = data['Air']
        cellid.mAIRID.save()
    if data['CO2'] is not None and cellid.mCO2ID is not None:
        cellid.mCO2ID.nextState = data['CO2']
        cellid.mCO2ID.save()
    if data['H2O'] is not None and cellid.mH2OID is not None:
        cellid.mH2OID.nextState = data['H2O']
        cellid.mH2OID.save()
    return True
