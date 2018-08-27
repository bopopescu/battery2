from django.db import models

# Create your models here.
class SystemInfo(models.Model):
    name = models.CharField(max_length=20, primary_key=True)
	
# Create your models here.
class Group(models.Model):
	GroupID = models.CharField(max_length=20,verbose_name="客户ID(0开头6位)",primary_key=True,unique=True)
	GroupName = models.CharField(max_length=50, verbose_name="GroupName(0开头6位)")	
	U = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="电流", editable=False)
	I = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="电压", editable=False)
	QH2 = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="H2流量", editable=False)
	QN2 = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="N2流量", editable=False)
	QCH4 = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="CH4流量", editable=False)
	QAIR = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="空气流量", editable=False)
	QH2O = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="水流量", editable=False)
	TIN = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="进气口温度", editable=False)
	TOUT = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="出气口温度", editable=False)
	t = models.DateTimeField(auto_now=True,verbose_name="时间")

	class gas_data(models.Model):
    sid = models.ForeignKey(cell,verbose_name="系统ID")
    data_type = models.ForeignKey(Data_type,to_field ='data_type',verbose_name="数据类型")
    data_value = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="数据值",editable=False)
    update_time = models.DateTimeField(auto_now_add=True,verbose_name="数据时间")		
	
class cell(models.Model):
	sid = models.CharField(max_length=20, verbose_name="系统ID", primary_key=True, unique=True)
	boxNum = models.IntegerField(default=0, verbose_name="箱号")
	chnNum = models.IntegerField(default=0, verbose_name="通道号")
	i = models.IntegerField(default=0, verbose_name="实时电流")  #uA
	u = models.IntegerField(default=0, verbose_name="实时电压")  #mV
	q = models.IntegerField(default=0, verbose_name="实时容量")  # 
	qA = models.IntegerField(default=0, verbose_name="累计容量")  #
	r = models.IntegerField(default=0, verbose_name="当前内阻")  #
	T = models.IntegerField(default=0, verbose_name="当前温度")  #
	n = models.IntegerField(default=0, verbose_name="当前工步号")   #
	k = models.IntegerField(default=0, verbose_name="当前过程号")   #	
	state = models.IntegerField(default=0, verbose_name="通道状态") #
	mode = models.IntegerField(default=0, verbose_name="工作模式")  #
	tc = models.IntegerField(default=0, verbose_name="本工步已完成时间") #ms
	ta = models.IntegerField(default=0, verbose_name="本工步累计时间")   #ms

	update_time = models.DateTimeField(auto_now=True, verbose_name="修改时间")