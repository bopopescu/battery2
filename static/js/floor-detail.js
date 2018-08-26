$(document).ready(function(){

get_hour();

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



function get_hour() {
    getactivebtn('todaychart');
    $('#daterangepickerdiv').hide();
    $('#datecompdiv').hide();
    $('#onedatepickerdiv').show();
    $('#echarts').css('margin-top','70px');
    date_time = new Datetime();
    $('#datepicker').datepicker('destroy');


    $('#datepicker').datepicker({
        language: 'zh-CN',//显示中文
        format: 'yyyy-mm-dd',//显示格式
        startDate: '2018-06-08',
        endDate: date_time.nowdate,
        minView: "month",//设置只显示到月份
        defaultViewDate : date_time.today ,
        autoclose: true,//选中自动关闭
        locale: moment.locale('zh-cn')
    });

    document.getElementById("datepicker").value = date_time.todaydatetext;
    get_hour_charts();
}


function get_month() {
    getactivebtn('monthchart');
    $('#daterangepickerdiv').hide();
    $('#datecompdiv').hide();
    $('#onedatepickerdiv').show();
    $('#echarts').css('margin-top','70px');
    date_time = new Datetime();
    $('#datepicker').datepicker('destroy');

    $('#datepicker').datepicker({
        language: 'zh-CN',//显示中文
        format: 'yyyy-mm',//显示格式
        startDate: '2018-06',
        endDate: date_time.nowmonth,
        minViewMode: "year",//设置只显示到年
        autoclose: true,//选中自动关闭
        locale: moment.locale('zh-cn')
    });

    document.getElementById("datepicker").value = date_time.todaymonthtext;
    get_month_echarts();
}


function get_customize() {
    getactivebtn('customizechart');
    $('#onedatepickerdiv').hide();
    $('#datecompdiv').hide();
    $('#daterangepickerdiv').show();
    $('#echarts').css('margin-top','70px');
    date_time = new Datetime();

    var beginTimeStore = '';
    var endTimeStore = '';
    $('#daterangepicker').daterangepicker({
        "linkedCalendars": true,
        "autoUpdateInput": false,
        "opens":"right",
        "minDate":"2018-06-08",
        "maxDate":date_time.nowdate,
        "locale": {
            format: 'YYYY-MM-DD',
            separator: '~',
            applyLabel: "应用",
            cancelLabel: "取消",
            resetLabel: "重置",
            fromLabel : '起始时间',
            toLabel : '结束时间',
            customRangeLabel : '自定义',
        },
        ranges : {
            //'最近1小时': [moment().subtract('hours',1), moment()],
            '今日': [moment().startOf('day'), moment()],
            '昨日': [moment().subtract(1,'days').startOf('day'), moment().subtract(1,'days').endOf('day')],
            '最近7日': [moment().subtract(6,'days'), moment()],
            '最近30日': [moment().subtract(29,'days'), moment()],
            '本月': [moment().startOf("month"),moment().endOf("month")],
            '上个月': [moment().subtract(1,"month").startOf("month"),moment().subtract(1,"month").endOf("month")]
        },
    },function(start, end, label) {
                beginTimeStore = start;
                endTimeStore = end;
                if(!this.startDate){
                    this.element.val('');
                }else{
                    this.element.val(this.startDate.format(this.locale.format) + this.locale.separator + this.endDate.format(this.locale.format));
                }
    });

    document.getElementById("daterangepicker").value = date_time.todaydatetext+"~"+date_time.todaydatetext;
    get_customize_echarts();
}

function get_comp() {
    getactivebtn('comparechart');
    date_time = new Datetime();
    // $('#datepicker').datepicker('destroy');
    $('#onedatepickerdiv').hide();
    $('#daterangepickerdiv').hide();
    $('#datecompdiv').show();
    $('#echarts').css('margin-top','70px');

    $('#datecomppicker1').datepicker({
        language: 'zh-CN',//显示中文
        format: 'yyyy-mm-dd',//显示格式
        startDate: '2018-06-08',
        endDate: date_time.nowdate,
        minView: "month",//设置只显示到月份
        initialDate: new Date(),
        autoclose: true,//选中自动关闭
        locale: moment.locale('zh-cn')
    });

    $('#datecomppicker2').datepicker({
        language: 'zh-CN',//显示中文
        format: 'yyyy-mm-dd',//显示格式
        startDate: '2018-06-08',
        endDate: date_time.nowdate,
        minView: "month",//设置只显示到月份
        initialDate: new Date(),
        autoclose: true,//选中自动关闭
        locale: moment.locale('zh-cn')
    });

    document.getElementById("datecomppicker1").value = date_time.yesterdaydatetext;
    document.getElementById("datecomppicker2").value = date_time.todaydatetext;
    get_comp_echarts();
}

function get_realtime() {
    getactivebtn('realtimechart');
    $('#onedatepickerdiv').hide();
    $('#daterangepickerdiv').hide();
    $('#datecompdiv').hide();
    $('#echarts').css('margin-top',0);

     var myChart = echarts.init(document.getElementById('echarts'));
    myChart.clear();
    sid = $('#sid').text();
    openrealtimechart(sid)
}

function get_calendar() {
    getactivebtn('calendarchart');
    $('#onedatepickerdiv').hide();
    $('#daterangepickerdiv').hide();
    $('#datecompdiv').hide();
    $('#echarts').css('margin-top',0);


    get_calendar_echarts();
}




function get_hour_charts() {
  var myChart = echarts.init(document.getElementById('echarts'));
  myChart.clear();
  var hourdata = gethourdata('datepicker');
  var devicename = $('#devicename').text();
  chartsdata = getchartsdata(hourdata);
  var option = {
            title: {
                text: '能耗曲线'
            },
            tooltip: {
              trigger: 'axis'
            },
            legend: {
                data:[devicename]
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
            name:devicename,
            type:'line',
            // stack: '能耗',
            data:chartsdata[1]
            }
            ]
        };
  myChart.setOption(option);
}

function get_month_echarts() {
    var myChart = echarts.init(document.getElementById('echarts'));
    myChart.clear();
  var daydata = getdaydata('datepicker');
  var devicename = $('#devicename').text();
  chartsdata = getdatechartsdata(daydata);
  var option = {
            title: {
                text: '能耗曲线'
            },
            tooltip: {
              trigger: 'axis'
            },
            legend: {
                data:[devicename]
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
            name:devicename,
            type:'bar',
            barWidth:'12',
            // stack: '能耗',
            data:chartsdata[1]
            }
            ]
        };
  myChart.setOption(option);
}

function get_customize_echarts() {
    var myChart = echarts.init(document.getElementById('echarts'));
    myChart.clear();
  var daydata = getcustomizedata('daterangepicker');
  var devicename = $('#devicename').text();
  chartsdata = getdatechartsdata(daydata);
  var option = {
            title: {
                text: '能耗曲线'
            },
            tooltip: {
              trigger: 'axis'
            },
            legend: {
                data:[devicename]
            },
            toolbox: {
                feature: {
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
            name:devicename,
            type:'bar',
            barWidth:'12',
            // stack: '能耗',
            data:chartsdata[1]
            }
            ]
        };
  myChart.setOption(option);
}


function get_calendar_echarts() {
    var myChart = echarts.init(document.getElementById('echarts'));
    myChart.clear();
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
        max: 3000,
        type: 'piecewise',
        orient: 'horizontal'
    },
    calendar: {
        top: 100,
        bottom:30,
        right:30,
        cellSize: 'auto',
        range: ['2018-06-08', '2018-12-31']
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

//btn改class active
function getactivebtn(btnid) {
  var btnactive = $('#'+ btnid);
  var btn = $('.btn');
  btn.removeClass('active');
  btnactive.addClass('active');
}

//曲线对比
function get_comp_echarts() {
  var myChart = echarts.init(document.getElementById('echarts'));
  myChart.clear();
  var hourdata1 = gethourdata('datecomppicker1');
  var hourdata2 = gethourdata('datecomppicker2');
  var chartsdata1 = getchartsdata(hourdata1);
  var chartsdata2 = getchartsdata(hourdata2);
  datecomp1 = document.getElementById("datecomppicker1").value;
  datecomp2 = document.getElementById("datecomppicker2").value;
  var option = {
            title: {
                text: '能耗曲线'
            },
            tooltip: {
              trigger: 'axis'
            },
            legend: {
                data:[datecomp1,datecomp2]
            },
            toolbox: {
                feature: {
                // saveAsImage: {}
                        }
            },
            xAxis: {
                type: 'category',
                // boundaryGap: false,
                data: ["0","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23"]
            },
            yAxis: {
              type: 'value',
              name: 'kWh',
              nameLocation: 'end'
            },
            series: [
            {
            name:datecomp1,
            type:'line',
            data:chartsdata1[1]
            },
             {
            name:datecomp2,
            type:'line',
            data:chartsdata2[1]
            }
            ]
        };
  myChart.setOption(option);

}



function openrealtimechart(page) {
   window.open('/customer/realtime/'+page, 'newwindow','height=380, width=650, top=50%,left=50%, toolbar=no, menubar=no, scrollbars=no, resizable=no,location=no,status=no');
}



//hour data
function gethourdata(dateinput) {
    var result;
    var Hourdataobj = new Object()
    Hourdataobj.date = $('#'+dateinput).val();
    Hourdataobj.sid =$('#sid').text();
    dataurl = $.param(Hourdataobj);
    $.ajax({
        url:'/getfloorhourdata/?'+dataurl,
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

//day data
function getdaydata(dateinput) {
    var result;
    var Daydataobj = new Object()
    Daydataobj.date = $('#'+dateinput).val();
    Daydataobj.sid =$('#sid').text();
    dataurl = $.param(Daydataobj);
    $.ajax({
        url:'/getfloordaydata/?'+dataurl,
        type:'get',
        dataType: 'json',
        async:false,
        success:function (data) {
            result = data;
        }

    });

    return result;
}

function getdatechartsdata(datedata) {
    var seriesdata = [];
    var chartsdata = [];
    for(i=0;i<datedata.length;i++){
        seriesdata.push(datedata[i].date);
        chartsdata.push(datedata[i].day_e);
    }
    return [seriesdata,chartsdata]
}

function getcustomizedata(daterange) {
    var result;
    var Daydataobj = new Object()
    Daydataobj.date = $('#'+daterange).val();
    Daydataobj.sid =$('#sid').text();
    dataurl = $.param(Daydataobj);
    $.ajax({
        url:'/getfloorcustomizedaydata/?'+dataurl,
        type:'get',
        dataType: 'json',
        async:false,
        success:function (data) {
            result = data;
        }

    });
    return result;
}


function getcalendardata() {
    var Daydataobj = new Object();
    Daydataobj.date = 'all';
    Daydataobj.sid =$('#sid').text();
    dataurl = $.param(Daydataobj);
    var result = [];
    $.ajax({
        url:'/getfloorcustomizedaydata/?'+dataurl,
        type:'get',
        dataType: 'json',
        async:false,
        success:function (data) {
            for (var i = 0; i < data.length; i++) {
                onedaydata = [data[i].date, data[i].day_e];
                result.push(onedaydata);
            }
        }

    });

    return result;

}