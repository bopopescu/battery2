from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse

# Create your views here.
def home(request):
    context          = {}
    context['para1'] = 'Hello World!'
    context['static_dir'] = settings.STATIC_URL
    return render(request, 'home.html', context)
	
# 数据库操作
from apps.models import SystemInfo

def testdb(request):
    # 修改其中一个id=1的name字段，再save，相当于SQL中的UPDATE
    test1 = SystemInfo.objects.get(id=1)
    test1.name = 'Google'
    test1.save()
    
    # 另外一种方式
    #Test.objects.filter(id=1).update(name='Google')
    
    # 修改所有的列
    # Test.objects.all().update(name='Google')
    
    return HttpResponse("<p>修改成功</p>")