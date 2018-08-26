$(document).ready(function(){

get_initialize();
get_rank_echarts();

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

    document.getElementById("daterangepicker").value = date_time.todaydatetext+"~"+date_time.todaydatetext;
}

function get_ranking_data() {
    var optObj=new Object();
    optObj.typeOption =$('[name=typeOption]:checked').val();
    optObj.date =$('[name=date]').val();
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
    // for(i=rankingdata.length-1;i>=0;i--){
    for(i=0;i<rankingdata.length;i++){
        seriesdata.push(rankingdata[i].sid_id);
        chartsdata.push(rankingdata[i].add_e);
    }
    return [seriesdata,chartsdata]
}

function get_rank_echarts() {
    var myChart = echarts.init(document.getElementById('echarts'));
    var rankingdata = get_ranking_data();
    var chartsdata = getchartsdata(rankingdata);
    option = {
    title: {
        text: '能耗排名',
    },
    tooltip: {
        trigger: 'axis',
        axisPointer: {
            type: 'shadow'
        }
    },
    legend: {
        data: ['能耗(kWh)']
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
            name: '能耗(kWh)',
            type: 'bar',
            // barWidth: 21,
            data: chartsdata[1]
        }
    ]
};
    myChart.setOption(option);
}
