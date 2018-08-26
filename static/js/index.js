$(document).ready(function(){

get_initialize();

});

function Datetime(){
     //默认获取当前日期
    var today = new Date();
    var yesterday = new Date(new Date()-24*60*60*1000);
    this.nowdate = (today.getFullYear()) + "-" + (today.getMonth() + 1) + "-" + today.getDate();
    this.nowmonth = (today.getFullYear()) + "-" + (today.getMonth() + 1);

    function getdatetext(date){ // 定义一个方法 getdatetext()
        var mon = date.getMonth() + 1;
        var day = date.getDate();
        return date.getFullYear() + "-" + (mon < 10 ? "0" + mon : mon) + "-" + (day < 10 ? "0" + day : day);
    }

    //对日期格式进行处理
    this.todaydatetext = getdatetext(today);
    this.todaymonthtext = today.getFullYear() + "-" + ((today.getMonth() + 1) < 10 ? "0" + (today.getMonth() + 1) : (today.getMonth() + 1));
    this.yesterdaydatetext = getdatetext(yesterday);

}

function get_initialize() {
    date_time = new Datetime();
    // get_today_echarts();
    get_recent_echarts();
    get_rank_echarts();
    // get_pie_echarts();
    get_calendar_echarts();
    // get_realtime_echarts();
    get_comp_echarts();
}

function get_recent_echarts() {
    var myChart = echarts.init(document.getElementById('echarts1'));
  var chartsdata = getrecentdata();
  var option = {
            title: {
                text: '10小时能耗图'
            },
            tooltip: {
              trigger: 'axis'
            },
            legend: {
                data:['小时能耗'],
                top:30
            },
            toolbox: {
                feature: {
                // saveAsImage: {}
                        }
            },
            xAxis: {
                type: 'category',
                data: chartsdata[0]
            },
            yAxis: {
              type: 'value',
              name: 'kWh',
              nameLocation: 'end'
            },
            series: [
            {
            name:'小时能耗',
            type:'bar',
                barWidth:'70%',
            data:chartsdata[1]
            }
            ]
        };
  myChart.setOption(option);
}


//hour data
function getrecentdata() {
    var seriesdata = [];
    var chartsdata = [];
    var Hourdataobj = new Object()
    Hourdataobj.sid =$('#sid').text();
    dataurl = $.param(Hourdataobj);
    $.ajax({
        url:'/getcustomerrecenthourdata/?'+dataurl,
        type:'get',
        dataType: 'json',
        async:false,
        success:function (data) {
            for(i=data.length-1;i>=0;i--){
                seriesdata.push(data[i].hour_time)
                chartsdata.push(data[i].hour_e);
            }
        }

    });

    return [seriesdata,chartsdata]
}

function get_today_echarts() {
    var myChart = echarts.init(document.getElementById('echarts1'));
  var hourdata = gethourdata();
  // var devicename = $('#devicename').text();
  chartsdata = getchartsdata(hourdata);
  var option = {
            title: {
                text: '今日分时能耗'
            },
            tooltip: {
              trigger: 'axis'
            },
            legend: {
                data:['小时能耗'],
                top:30
            },
            toolbox: {
                feature: {
                // saveAsImage: {}
                        }
            },
            xAxis: {
                type: 'category',
                // data:chartsdata[0]
                data: ["0","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23"]
            },
            yAxis: {
              type: 'value',
              name: 'kWh',
              nameLocation: 'end'
            },
            series: [
            {
            name:'小时能耗',
            type:'line',
            data:chartsdata[1]
            }
            ]
        };
  myChart.setOption(option);
}


function get_comp_echarts() {
    var myChart = echarts.init(document.getElementById('echarts5'));
  var hourdata = gethourdata();
  // var devicename = $('#devicename').text();
  chartsdata = getchartsdata(hourdata);
  var option = {
            title: {
                text: '今日分时能耗曲线'
            },
            tooltip: {
              trigger: 'axis'
            },
            legend: {
                data:['小时能耗'],
                top:30
            },
            toolbox: {
                feature: {
                // saveAsImage: {}
                        }
            },
            xAxis: {
                type: 'category',
                // data:chartsdata[0]
                data: ["0","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23"]
            },
            yAxis: {
              type: 'value',
              name: 'kWh',
              nameLocation: 'end'
            },
            series: [
            {
            name:'小时能耗',
            type:'line',
            data:chartsdata[1]
            }
            ]
        };
  myChart.setOption(option);
}

//hour data
function gethourdata() {
    var result;
    date_time = new Datetime();
    var Hourdataobj = new Object()
    Hourdataobj.date = date_time.todaydatetext;
    Hourdataobj.sid =$('#sid').text();
    dataurl = $.param(Hourdataobj);
    $.ajax({
        url:'/getcustomerhourdata/?'+dataurl,
        type:'get',
        dataType: 'json',
        async:false,
        success:function (data) {
            result = data;
        }

    });

    return result;
}

function getchartsdata(hourdata) {
    var seriesdata = [];
    var chartsdata = [];
    for(i=0;i<hourdata.length;i++){
        seriesdata.push(hourdata[i].hour_time);
        chartsdata.push(hourdata[i].hour_e);
    }
    return [seriesdata,chartsdata]
}



function get_rank_echarts() {
    var myChart = echarts.init(document.getElementById('echarts2'));
    var chartsdata = get_ranking_data();
    option = {
    title: {
        text: '今日能耗排名',
    },
    tooltip: {
        trigger: 'axis',
        axisPointer: {
            type: 'shadow'
        }
    },
    legend: {
        data: ['今日能耗'],
                top:30
    },
    grid: {
        left: '3%',
        right: '4%',
        bottom: '13%',
        containLabel: true
    },
    yAxis: {
        type: 'value',
        boundaryGap: [0, 0.01]
    },
    xAxis: {
        type: 'category',
        axisLabel: { //xAxis，yAxis，axis都有axisLabel属性对象
            show: true, //默认为true，设为false后下面都没有意义了
            interval: 0, //此处关键， 设置文本标签全部显示
            rotate: 45
        },
        data: chartsdata[0]
    },
    series: [
        {
            name: '今日能耗',
            type: 'bar',
            barWidth: '50%',
            data: chartsdata[1]
        }
    ]
};
    myChart.setOption(option);
}


function get_ranking_data() {
    var seriesdata = [];
    var chartsdata = [];
    var optObj=new Object();
    optObj.typeOption ='device';
    optObj.date = date_time.todaydatetext+'~'+date_time.todaydatetext;
    var urlopt = $.param(optObj);
    var result;
    $.ajax({
        url:'/getranking/?' + urlopt,
        type:'GET',
        dataType: 'json',
        async:false,
        success:function(rankingdata){
            for(i=0;i<rankingdata.length;i++){
            seriesdata.push(rankingdata[i].sid_id);
            chartsdata.push(rankingdata[i].add_e);
            }
        }
    });

    return [seriesdata,chartsdata];
}




function get_pie_echarts() {
    var myChart = echarts.init(document.getElementById('echarts3'));
    var chatrsdata = get_pie_data();
  option = {
    title :
          {
            text: '不同类型能耗占比',
            top: '0',
            x:'6%'
          },
    tooltip : {
        trigger: 'item',
        formatter: "{a} <br/>{b} : {c} ({d}%)"
    },
    legend:
          {
            // orient: 'vertical',
            top: '35',
            x: '30%',
            data: ['照明','应急','办公','动力','其他']
          },
    series :
        {
            name: '负荷能耗',
            type: 'pie',
            radius : '55%',
            center: ['50%', '60%'],
            data:chatrsdata,
            itemStyle: {
                emphasis: {
                    shadowBlur: 10,
                    shadowOffsetX: 0,
                    shadowColor: 'rgba(0, 0, 0, 0.5)'
                }
            }
        }
  };


  myChart.setOption(option);
}


function get_pie_data() {
    var result;
    var optObj=new Object();
    optObj.date = date_time.todaydatetext+'~'+date_time.todaydatetext;
    var urlopt = $.param(optObj);
    $.ajax({
        url:'/gettypedata/?' + urlopt,
        type:'GET',
        dataType: 'json',
        async:false,
        success:function(data){
            result = data;
        }
    });

    return result;
}



function get_calendar_echarts() {
    var myChart = echarts.init(document.getElementById('echarts4'));
var chartsdata = getcalendardata();
  var option = {
    title: {
        top: 10,
        left: 'center',
        text: '能耗日历'
    },
    tooltip : {
      formatter : '{c0}'+'kWh',
      position: 'top'
    },
    visualMap: {
        // show: false,
        left: 'center',
        top: 50,
        min: 0,
        max: 5000,
        type: 'piecewise',
        orient: 'horizontal'
    },
    calendar: {
        top: 100,
        bottom:30,
        cellSize: 'auto',
        range: ['2018-07-01', '2018-12-31']
    },
    series: {
        type: 'heatmap',
        name:'能耗日历',
        coordinateSystem: 'calendar',
        data: chartsdata
    }
  };

  myChart.setOption(option);
}


function getcalendardata() {
    var Daydataobj = new Object();
    Daydataobj.date = 'all';
    Daydataobj.sid = $('#sid').text();
    dataurl = $.param(Daydataobj);
    var result = [];
    $.ajax({
        url: '/getcustomercustomizedaydata/?' + dataurl,
        type: 'get',
        dataType: 'json',
        async: false,
        success: function (data) {
            for (var i = 0; i < data.length; i++) {
                onedaydata = [data[i].date, data[i].day_e];
                result.push(onedaydata);
            }
        }

    });
    return result;
}




function get_realtime_echarts() {
  var myChart = echarts.init(document.getElementById('echarts5'));
  var chartsdata =  getrealtimechartdata();
    var option = {
            title: {
                text: '实时功率'
            },
            grid:{
                left:'20%',
                right:'0',
                bottom:'10%'
            },
            tooltip: {
              trigger: 'axis'
            },
            legend: {
                top:30,
                data:['功率（W）']
            },
            toolbox: {
                feature: {
                        }
            },
            xAxis: {
                type: 'category',
                boundaryGap: false,
                data: getdata(chartsdata,'xAxis')
            },
            yAxis: {
              type: 'value',
              name: 'W',
               min: 'dataMin',
              nameLocation: 'end'
            },
            series: [
            {
            name:'功率（W）',
            type:'line',
            smooth:true, //平滑曲线
            stack: 'a',
            data:getdata(chartsdata,'series')
            }

            ]
        };


    myChart.setOption(option);
    setInterval(function () {
    var dynamicchartsdata = getrealtimechartdata();
    myChart.setOption({
        xAxis: {
            data: getdata(dynamicchartsdata,'xAxis')
        },
        series: [{
            name:'功率（W）',
            type:'line',
            data: getdata(dynamicchartsdata,'series')
        }]
    });
}, 20000);

}

function getrealtimechartdata() {
        var chartsdata;
        var sid =$('#sid').text();
        $.ajax({url:'/device/realtimedata/'+sid+'/',
        type : "get",
        dataType: 'json',
        async:false, //同步执行
        success:function(data){

          chartsdata = data;
       }
     });
        return chartsdata;
}


function getdata(chartsdata,type) {
  var xAxisdata = [];
  var seriesdata = [];
  for (var i = chartsdata.length-1; i >= 0; i--) {
      xAxisdata.push(chartsdata[i].time);
      seriesdata.push(chartsdata[i].p);
    }
  if (type == 'xAxis') {

    return xAxisdata;
  } else if (type == 'series')  {
    return seriesdata;
  }
}