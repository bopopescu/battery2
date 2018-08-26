from django.contrib import admin
from .models import *
from django.forms.models import model_to_dict

# Register your models here.

# class cellDeviceTableAdmin(admin.ModelAdmin):
#     list_display = list(model_to_dict(cellDeviceTable()).keys())
#     list_display_links = None
#     list_editable = list_display
#     list_filter = ["cellID", "boxID", "chnNum"]
#     #list_display = ["cellID", "boxID", "chnNum","eIP","ePort","mN2Type",]
#
#
# class planTableAdmin(admin.ModelAdmin):
#     list_display = list(model_to_dict(planTable()).keys())
#     list_display_links = None
#     list_editable = list_display
#     list_filter = ["planID"]
#     # list_display = ["planID", "name", "step", "mode", "i", "u", "cH2", "cN2", "cCO2", "cAIR", "cH2O", "cCH4", "changeT",
#     #                 "cT1", "timeT", "stepTime", "stepStopMode", "stepStopCondition", "recordMode"]
#     # list_display_links = None
#     # list_editable = ["planID", "name", "step", "mode", "i", "u", "cH2", "cN2", "cCO2", "cAIR", "cH2O", "cCH4", "changeT",
#     #                 "cT1", "timeT", "stepTime", "stepStopMode", "stepStopCondition", "recordMode"]
#
# class cellRealDataTableAdmin(admin.ModelAdmin):
#     # list_display = ["testID", "totalStepN", "currState", "nextState", "n", "k", "tc", "ta", "i", "u", "celldata_time",
#     #                 "qH2", "tH2", "qN2", "tN2", "qCO2", "tCO2", "qCH4", "tCH4", "qAIR", "tAIR", "qH2O", "tH2O", "T1",
#     #                 "tT1"]
#     list_display = list(model_to_dict(cellRealDataTable()).keys())
#     list_display_links = None
#     list_editable = list_display
#     list_filter = ["testID","cellID"]
#
# class cellHistoryDataTableAdmin(admin.ModelAdmin):
#     # list_display = ["testID", "totalStepN", "currState", "nextState", "n", "k", "tc", "ta", "i", "u", "celldata_time",
#     #                 "qH2", "tH2", "qN2", "tN2", "qCO2", "tCO2", "qCH4", "tCH4", "qAIR", "tAIR", "qH2O", "tH2O", "T1",
#     #                 "tT1"]
#     list_display = list(model_to_dict(cellHistoryDataTable()).keys())
#     list_display_links = None
#     list_editable = list_display
#     list_filter = ["testID", "cellID"]
#
# class testInfoTableAdmin(admin.ModelAdmin):
#     # list_display = ["cellID", "planID", "boxID", "chnNum"]
#     # list_display_links=None
#     # list_editable = ("cellID", "planID", "boxID", "chnNum")
#     list_display = list(model_to_dict(testInfoTable()).keys())
#     list_display_links = None
#     list_editable = list_display
#
# class planInfoTableAdmin(admin.ModelAdmin):
#     # list_display = ["cellID", "planID", "boxID", "chnNum"]
#     # list_display_links=None
#     # list_editable = ("cellID", "planID", "boxID", "chnNum")
#     list_display = list(model_to_dict(planInfoTable()).keys())
#     list_display_links = None
#     list_editable = list_display
#
# class eventTableAdmin(admin.ModelAdmin):
#     # list_display = ["cellID", "planID", "boxID", "chnNum"]
#     # list_display_links=None
#     # list_editable = ("cellID", "planID", "boxID", "chnNum")
#     list_display = list(model_to_dict(eventTable()).keys())
#     list_display_links = None
#     list_editable = list_display

admin.site.register(boxDeviceTable)
admin.site.register(wdjDeviceTable)
admin.site.register(H2DeviceTable)
admin.site.register(H2ODeviceTable)
admin.site.register(CH4DeviceTable)
admin.site.register(CO2DeviceTable)
admin.site.register(AIRDeviceTable)
admin.site.register(N2DeviceTable)
admin.site.register(ovenDeviceTable)
admin.site.register(ovenPlanTable)
admin.site.register(ovenPlanDetailTable)
admin.site.register(cellDeviceTable)
admin.site.register(cellPlanTable)
admin.site.register(cellPlanDetailTable)
admin.site.register(BigTestInfoTable)
admin.site.register(testInfoTable)
admin.site.register(cellTestRealDataTable)
admin.site.register(eventTable)
admin.site.register(cellTestHistoryDataTable)










