from django.db import models

# Create your models here.

class group(models.Model):
	groupID = models.CharField(default=0, max_length=20, verbose_name="电池组ID", unique=True)

class cellDeviceTable(models.Model):
	cellID = models.IntegerField(default=0, primary_key=True, verbose_name="cellID", unique=True)	
	boxNum = models.IntegerField(default=0, verbose_name="箱号")
	chnNum = models.IntegerField(default=0, verbose_name="通道号")
	
	i = models.IntegerField(default=0, verbose_name="实时电流")  #uA
	u = models.IntegerField(default=0, verbose_name="实时电压")  #mV
	q = models.IntegerField(default=0, verbose_name="实时容量")  #
	qA = models.IntegerField(default=0, verbose_name="累计容量") #
	r = models.IntegerField(default=0, verbose_name="当前内阻")  #
	T = models.IntegerField(default=0, verbose_name="当前温度")  #
	n = models.IntegerField(default=0, verbose_name="当前工步号")   #
	k = models.IntegerField(default=0, verbose_name="当前过程号")   #
	state = models.IntegerField(default=0, verbose_name="通道状态") #
	mode = models.IntegerField(default=0, verbose_name="工作模式")  #
	tc = models.IntegerField(default=0, verbose_name="本工步已完成时间") #ms
	ta = models.IntegerField(default=0, verbose_name="本工步累计时间")   #ms
	celldata_time = models.DateTimeField(auto_now=True, verbose_name="电池数据修改时间")
	
	qH2 = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="H2流量", editable=False)
	qN2 = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="N2流量", editable=False)
	qCH4 = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="CH4流量", editable=False)
	qAIR = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="空气流量", editable=False)
	qH2O = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="水流量", editable=False)
		
	gasdata_time = models.DateTimeField(auto_now=True, verbose_name="气体数据修改时间")
	
	T1 = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="温度监测点1", editable=False)
	T2 = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="温度监测点2", editable=False)
	T3 = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="温度监测点3", editable=False)	
	
class gasDeviceDataType(models.Model):
	name = models.CharField(max_length=30,verbose_name="数据类型名称")
	type = models.CharField(max_length=30,verbose_name="数据类型标识",primary_key=True, unique=True)
	def __str__(self):
		return self.name
	
	class Meta:
		verbose_name = "数据类型名称"
		verbose_name_plural = verbose_name

class gasDeviceTable(models.Model):
	gasID = models.IntegerField(default=0, primary_key=True, verbose_name="气体流量计的ID", unique=True)
	cellID = models.ForeignKey(cellDeviceTable,to_field ='cellID',verbose_name="cellID", on_delete=models.DO_NOTHING)
	type = models.ForeignKey(gasDeviceDataType,to_field ='type',verbose_name="数据类型标识", on_delete=models.DO_NOTHING)
	qCoef = models.DecimalField(max_digits=2, decimal_places=1, default=0, verbose_name="比例系数", editable=False)
	qIP = models.GenericIPAddressField(default='192.168.1.2', verbose_name="IP地址")
	qPort = models.IntegerField(default=0, verbose_name="端口号")
	
class gasDeviceHistoryData(models.Model):
	gasID = models.ForeignKey(gasDeviceTable,to_field ='gasID',verbose_name="gasID", on_delete=models.DO_NOTHING)	
	type = models.ForeignKey(gasDeviceDataType,to_field ='type',verbose_name="数据类型标识", on_delete=models.DO_NOTHING)
	value = models.FileField(verbose_name="原始报文")
	time = models.DateTimeField(auto_now_add=True,verbose_name="时间")
	
class boxDeviceTable(models.Model):
	boxID = models.IntegerField(default=0, primary_key=True, verbose_name="boxID", unique=True)
	cellID = models.ForeignKey(cellDeviceTable,to_field ='cellID',verbose_name="cellID", on_delete=models.DO_NOTHING)
	boxNum = models.IntegerField(default=0, verbose_name="箱号")
	chnNum = models.IntegerField(default=0, verbose_name="通道号")
	boxIP = models.GenericIPAddressField(default='192.168.1.1', verbose_name="IP地址")
	boxPort = models.IntegerField(default=0, verbose_name="端口号")

class boxDeviceDataType(models.Model):
	name = models.CharField(max_length=30,verbose_name="数据类型名称")
	type = models.CharField(max_length=30,verbose_name="数据类型标识",primary_key=True, unique=True)	
	def __str__(self):
		return self.name
	
	class Meta:
		verbose_name = "数据类型名称"
		verbose_name_plural = verbose_name
		
		
class boxDeviceHistoryData(models.Model):
	boxID = models.ForeignKey(boxDeviceTable,to_field ='boxID',verbose_name="boxID", on_delete=models.DO_NOTHING)	
	type = models.ForeignKey(boxDeviceDataType,to_field ='type',verbose_name="数据类型标识", on_delete=models.DO_NOTHING)
	value = models.FileField(verbose_name="原始报文")
	time = models.DateTimeField(auto_now_add=True,verbose_name="时间")	

'''		
	cellID = models.IntegerField(default=0, primary_key=True, verbose_name="电池ID", unique=True)	
	boxNum = models.IntegerField(default=0, verbose_name="箱号")
	chnNum = models.IntegerField(default=0, verbose_name="通道号")
	boxIP = models.GenericIPAddressField(default='192.168.1.1', verbose_name="IP地址")
	boxPort = models.IntegerField(default=0, verbose_name="端口号")
	
	qH2ID = models.ForeignKey(gasDeviceTable,to_field ='gasID',verbose_name="H2流量计", on_delete=models.DO_NOTHING)
	qH2Coef = models.DecimalField(max_digits=2, decimal_places=2, default=0, verbose_name="H2流量计", editable=False)
	qH2IP = models.GenericIPAddressField(default='192.168.1.2', verbose_name="IP地址")
	qH2Port = models.IntegerField(default=0, verbose_name="端口号")
	
	qN2ID = models.ForeignKey(gasDeviceTable,to_field ='gasID',verbose_name="N2流量计", on_delete=models.DO_NOTHING)
	qN2Coef = models.DecimalField(max_digits=2, decimal_places=2, default=0, verbose_name="H2流量计", editable=False)
	qN2IP = models.GenericIPAddressField(default='192.168.1.2', verbose_name="IP地址")
	qN2Port = models.IntegerField(default=0, verbose_name="端口号")
	
	qCH4ID = models.ForeignKey(gasDeviceTable,to_field ='gasID',verbose_name="CH4流量计", on_delete=models.DO_NOTHING)
	qCH4Coef = models.DecimalField(max_digits=2, decimal_places=2, default=0, verbose_name="H2流量计", editable=False)
	qCH4IP = models.GenericIPAddressField(default='192.168.1.2', verbose_name="IP地址")
	qCH4Port = models.IntegerField(default=0, verbose_name="端口号")

	qH2OID = models.ForeignKey(gasDeviceTable,to_field ='gasID',verbose_name="H2O流量计", on_delete=models.DO_NOTHING)
	qH2OCoef = models.DecimalField(max_digits=2, decimal_places=2, default=0, verbose_name="H2流量计", editable=False)
	qH2OIP = models.GenericIPAddressField(default='192.168.1.2', verbose_name="IP地址")
	qH2OPort = models.IntegerField(default=0, verbose_name="端口号")	
	
	qAIRID = models.ForeignKey(gasDeviceTable,to_field ='gasID',verbose_name="AIR流量计", on_delete=models.DO_NOTHING)
	qAIRCoef = models.DecimalField(max_digits=2, decimal_places=2, default=0, verbose_name="H2流量计", editable=False)
	qAIRIP = models.GenericIPAddressField(default='192.168.1.2', verbose_name="IP地址")
	qAIRPort = models.IntegerField(default=0, verbose_name="端口号")
	
	qTempID = models.ForeignKey(gasDeviceTable,to_field ='gasID',verbose_name="TEMP流量计", on_delete=models.DO_NOTHING)
	qTempCoef = models.DecimalField(max_digits=2, decimal_places=2, default=0, verbose_name="H2流量计", editable=False)
	qTempIP = models.GenericIPAddressField(default='192.168.1.2', verbose_name="IP地址")
	qTempPort = models.IntegerField(default=0, verbose_name="端口号")	

class cellRealDataTable(models.Model):
	cellID = models.CharField(max_length=20, verbose_name="电池ID", primary_key=True, unique=True)
	groupID = models.ForeignKey(group,to_field ='groupID',verbose_name="电池组ID", on_delete=models.DO_NOTHING)
	boxNum = models.IntegerField(default=0, verbose_name="箱号")
	chnNum = models.IntegerField(default=0, verbose_name="通道号")
	i = models.IntegerField(default=0, verbose_name="实时电流")  #uA
	u = models.IntegerField(default=0, verbose_name="实时电压")  #mV
	q = models.IntegerField(default=0, verbose_name="实时容量")  # 
	qA = models.IntegerField(default=0, verbose_name="累计容量") #
	r = models.IntegerField(default=0, verbose_name="当前内阻")  #
	T = models.IntegerField(default=0, verbose_name="当前温度")  #
	n = models.IntegerField(default=0, verbose_name="当前工步号")   #
	k = models.IntegerField(default=0, verbose_name="当前过程号")   #
	state = models.IntegerField(default=0, verbose_name="通道状态") #
	mode = models.IntegerField(default=0, verbose_name="工作模式")  #
	tc = models.IntegerField(default=0, verbose_name="本工步已完成时间") #ms
	ta = models.IntegerField(default=0, verbose_name="本工步累计时间")   #ms
	celldata_time = models.DateTimeField(auto_now=True, verbose_name="电池数据修改时间")
	
	qH2 = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="H2流量", editable=False)
	qN2 = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="N2流量", editable=False)
	qCH4 = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="CH4流量", editable=False)
	qAIR = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="空气流量", editable=False)
	qH2O = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="水流量", editable=False)
	
	gasdata_time = models.DateTimeField(auto_now=True, verbose_name="气体数据修改时间")
	
	T1 = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="温度监测点1", editable=False)
	T2 = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="温度监测点2", editable=False)
	T3 = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="温度监测点3", editable=False)

	
class cell(models.Model):
	cellID = models.CharField(max_length=20, verbose_name="电池ID", primary_key=True, unique=True)
	groupID = models.ForeignKey(group,to_field ='groupID',verbose_name="电池组ID", on_delete=models.DO_NOTHING)
	boxNum = models.IntegerField(default=0, verbose_name="箱号")
	chnNum = models.IntegerField(default=0, verbose_name="通道号")
	i = models.IntegerField(default=0, verbose_name="实时电流")  #uA
	u = models.IntegerField(default=0, verbose_name="实时电压")  #mV
	q = models.IntegerField(default=0, verbose_name="实时容量")  # 
	qA = models.IntegerField(default=0, verbose_name="累计容量") #
	r = models.IntegerField(default=0, verbose_name="当前内阻")  #
	T = models.IntegerField(default=0, verbose_name="当前温度")  #
	n = models.IntegerField(default=0, verbose_name="当前工步号")   #
	k = models.IntegerField(default=0, verbose_name="当前过程号")   #
	state = models.IntegerField(default=0, verbose_name="通道状态") #
	mode = models.IntegerField(default=0, verbose_name="工作模式")  #
	tc = models.IntegerField(default=0, verbose_name="本工步已完成时间") #ms
	ta = models.IntegerField(default=0, verbose_name="本工步累计时间")   #ms
	celldata_time = models.DateTimeField(auto_now=True, verbose_name="电池数据修改时间")
	
	qH2 = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="H2流量", editable=False)
	qN2 = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="N2流量", editable=False)
	qCH4 = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="CH4流量", editable=False)
	qAIR = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="空气流量", editable=False)
	qH2O = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="水流量", editable=False)
	
	gasdata_time = models.DateTimeField(auto_now=True, verbose_name="气体数据修改时间")
	
	T1 = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="温度监测点1", editable=False)
	T2 = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="温度监测点2", editable=False)
	T3 = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="温度监测点3", editable=False)	

class cell_data_type(models.Model):
	name = models.CharField(max_length=30,verbose_name="电池数据类型名称")
	type = models.CharField(max_length=30,verbose_name="电池数据类型标识",unique=True)
	
class cell_data(models.Model):
	cellID = models.ForeignKey(cell,verbose_name="电池ID", on_delete=models.DO_NOTHING)
	type = models.ForeignKey(cell_data_type,to_field ='type',verbose_name="电池数据类型标识", on_delete=models.DO_NOTHING)
	value = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="值",editable=False)	
	time = models.DateTimeField(auto_now_add=True,verbose_name="电池数据获取时间")

class gas_data_type(models.Model):
	gasDeviceID = models.CharField(max_length=30,verbose_name="气体流量计ID", primary_key=True)
	name = models.CharField(max_length=30,verbose_name="气体数据类型名称")	
	type = models.CharField(max_length=30,verbose_name="气体数据类型标识",unique=True)
	
class gas_data(models.Model):
	cellID = models.ForeignKey(cell,verbose_name="电池ID", on_delete=models.DO_NOTHING)
	type = models.ForeignKey(gas_data_type,to_field ='type',verbose_name="气体数据类型标识", on_delete=models.DO_NOTHING)
	value = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="值",editable=False)
	time = models.DateTimeField(auto_now_add=True,verbose_name="气体数据获取时间")
'''	