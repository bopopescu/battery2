$(document).ready(function(){

// changeoption('company');
get_initialize();
get_pie_echarts();
get_pie_echarts1();


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

    $('#device_tab').prop("checked",true);
    // $('#all_tab').prop("checked",true);
    // $('#company_tab1').prop("checked",true);


    date_time = new Datetime();

    var beginTimeStore = '';
    var endTimeStore = '';
    $('#daterangepicker').daterangepicker({
        "linkedCalendars": true,
        "autoUpdateInput": false,
        "opens":"right",
        // "startDate":moment().subtract(2,'days'),
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
        }
    },function(start, end, label) {
                beginTimeStore = start;
                endTimeStore = end;
                if(!this.startDate){
                    this.element.val('');
                }else{
                    this.element.val(this.startDate.format(this.locale.format) + this.locale.separator + this.endDate.format(this.locale.format));
                }
    });

    $('#daterangepicker1').daterangepicker({
        "linkedCalendars": true,
        "autoUpdateInput": false,
        "opens":"right",
        // "startDate":moment().subtract(2,'days'),
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
        }
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
    // document.getElementById("daterangepicker1").value = date_time.todaydatetext+"~"+date_time.todaydatetext;
}




function get_pie_echarts() {
    var myChart = echarts.init(document.getElementById('echarts_pie'));
    var rankingdata = get_ranking_data();
    var chartsdata = getchartsdata(rankingdata);
  option = {
    title : [
          {
            // text: '能耗用量对比',
            top: '10',
             x:'65%'

          },
        ],
    tooltip : {
        trigger: 'item',
        formatter: "{a} <br/>{b} : {c} ({d}%)"
    },
    legend: [
          {
            orient: 'vertical',
            // top: '50',
              left:'left',
            data: chartsdata[0]
          },
        ],
    series : [
        {
            name: '能耗比例',
            type: 'pie',
            radius : '55%',
            center: ['70%', '55%'],
            data:chartsdata[1],
            itemStyle: {
                emphasis: {
                    shadowBlur: 10,
                    shadowOffsetX: 0,
                    shadowColor: 'rgba(0, 0, 0, 0.5)'
                }
            }
        }
    ]
  };


  myChart.setOption(option);

}


function get_ranking_data() {
    var optObj=new Object();
    optObj.typeOption =$('[name=inlineRadioOptions]:checked').val();
    optObj.date =$('[name=date1]').val();
    var urlopt = $.param(optObj);
    var result;
    $.ajax({
        url:'/getranking/?' + urlopt,
        type:'GET',
        dataType: 'json',
        async:false,
        success:function(data_result){
            result = data_result;
        }
    });

    return result;
}

function getchartsdata(rankingdata) {
    var seriesdata = [];
    var chartsdata = [];
    for(i=rankingdata.length-1;i>=0;i--){
        seriesdata.push(rankingdata[i].sid_id);
        // chartsdata.push(rankingdata[i].add_e);
        var datadict = {'name':rankingdata[i].sid_id,'value':rankingdata[i].add_e}
        chartsdata.push(datadict)
    }
    return [seriesdata,chartsdata]
}




function get_pie_echarts1() {
  var myChart = echarts.init(document.getElementById('echarts_pie1'));
    var piedata = get_pie_data();
    // var chartsdata = getchartsdata(piedata);
  option = {
    title : [
          {
            text: '能耗类型对比',
            // subtext: '纯属虚构',
            top: '10',
             x:'39%'

          },
        ],
    tooltip : {
        trigger: 'item',
        formatter: "{a} <br/>{b} : {c} ({d}%)"
    },
    legend: [
          {
            orient: 'vertical',
            // top: '50',
              left:'left',
            data: ['动力','办公','照明','应急','其他']
          },
        ],
    series : [
        {
            name: '能耗比例',
            type: 'pie',
            radius : '55%',
            center: ['50%', '65%'],
            data:piedata,
            itemStyle: {
                emphasis: {
                    shadowBlur: 10,
                    shadowOffsetX: 0,
                    shadowColor: 'rgba(0, 0, 0, 0.5)'
                }
            }
        }
    ]
  };


  myChart.setOption(option);

}


function get_pie_data() {
    var result;
    var optObj=new Object();
    optObj.typeOption =$('[name=inlineRadioOptions2]:checked').val();
    optObj.objOption =$('[name=objOption]').val();
    optObj.date =$('[name=date2]').val();
    var urlopt = $.param(optObj);
    $.ajax({
        url:'/gettypedata1/?' + urlopt,
        type:'GET',
        dataType: 'json',
        async:false,
        success:function(data){
            result = data;
        }
    });

    return result;
}

//从数据库获取json
function getechartsdata(timetype,pienum) {
        var floordata = [];
        var typedata = [];
        var data = {};
        data['sqlkey'] = timetype;
        $.ajax({url:'http://118.24.110.98/echarts_pie',
        type : "post",
        dataType: 'json',
        data:data,
        async:false, //同步执行
        success:function(data){
               for (var i = 0; i < data.length; i++) {
                if (data[i].mac == '0x11') {
                  floordata.push({value:data[i].value,name:'一层'});
                }
                else if (data[i].mac == '0x12') {
                  floordata.push({value:data[i].value,name:'二层'});
                }
                else if (data[i].mac == '0x13') {
                  floordata.push({value:data[i].value,name:'三层'});
                  typedata.push({value:data[i].value,name:'照明'});
                }
                else if (data[i].mac == '0x10') {
                  typedata.push({value:data[i].value,name:'空调'});
                }
              }
       }
     });
        var chartsdata
        if (pienum ==1) {
          chartsdata = floordata;
        }
        else if (pienum ==2) {
          chartsdata = typedata;
        }
        return chartsdata;
 }

function get_option(obj_type) {
    var data = {};
    var result;
    data['obj_type'] = obj_type;
    $.ajax({
        url:'/getobj/',
        type:'POST',
        dataType: 'json',
        data:data,
        async:false,
        success:function(data_result){
            result = data_result;
        }
    });
    return result;
}

function changeoption(obj_type) {
    var seloption = document.getElementById('selectoption');
    seloption.options.length = 0;  //清空option
    optionlist=get_option(obj_type);
    // optionlist=get_option_api(obj_type);

    // seloption.options.add(new Option("所有","all"));
    for(i=0;i<optionlist.length;i++){
        seloption.options.add(new Option(optionlist[i].name,optionlist[i].sid));
    }
}
