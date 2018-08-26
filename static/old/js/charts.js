$(document).ready(function(){
    get_chart();
});

function get_chart() {
    // 基于准备好的dom，初始化echarts图表
    var page_title = document.title;
    var echarts_id,echarts_option;
    if (page_title === 'demo'){
        echarts_id = 'echarts';
        echarts_option = get_option(echarts_id);
        var myChart = echarts.init(document.getElementById(echarts_id));
        // 为echarts对象加载数据
        myChart.setOption(echarts_option);
    }
    else{
        echarts_id = ['one_charts','two_charts','three_charts'];
        for (var i of echarts_id) {
            echarts_option = get_option(i);
            var myChart = echarts.init(document.getElementById(i));
            // 为echarts对象加载数据
            myChart.setOption(echarts_option);
        }

    }

}

function get_hours() {
    var myDate = new Date();
    var thour = myDate.getHours();
    var hours = [];
    for (var i = 0; i < 7; i++) {
        var tthour = parseInt(thour)-6+i;
        hours.push(tthour.toString() + ':' +'00');
    }
    return hours;
}


function get_option(id) {
    var option;
    if (id === 'echarts'){
        option = {
            tooltip: {
                show: true
            },
            legend: {
                data:['销量']
            },
            xAxis : [
                {
                    type : 'category',
                    data : ["衬衫","羊毛衫","雪纺衫","裤子","高跟鞋","袜子"]
                }
            ],
            yAxis : [
                {
                    type : 'value'
                }
            ],
            series : [
                {
                    "name":"销量",
                    "type":"bar",
                    "data":[5, 20, 40, 10, 10, 20]
                }
            ]
        };
    }
    else{
        option = {
            tooltip : {
                trigger: 'axis'
            },
            legend: {
                data:['温度','湿度','空气质量']
            },
            xAxis : [
                {
                    type : 'category',
                    boundaryGap : false,
                    data : get_hours()
                }
            ],
            yAxis : [
                {
                    type : 'value',
                }
            ],
            series : [
                {
                    name:'温度',
                    type:'line',
                    data:[24, 23, 25, 26, 27, 23, 22]
                },
                {
                    name:'湿度',
                    type:'line',
                    data:[55, 66, 74, 76, 67, 65, 52]
                },
                {
                    name:'空气质量',
                    type:'line',
                    data:[22, 36, 42, 50, 38, 32, 32]
                }
            ]
        };

    }

    return option;
}