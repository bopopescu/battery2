$(document).ready(function(){

get_echarts();

});



function get_echarts() {
  var myChart = echarts.init(document.getElementById('echarts_calendar'));
  var myChart2 = echarts.init(document.getElementById('echarts_bar'));
  
  var option = {
    title: {
        top: 10,
        left: 'center',
        text: '总能耗日历'
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
        max: 1500,
        type: 'piecewise',
        orient: 'horizontal'
    },
    calendar: {
        top: 100,
        cellSize: 'auto',
        range: ['2018-01-08', '2018-12-31']
    },
    series: {
        type: 'heatmap',
        name:'能耗日历',
        coordinateSystem: 'calendar',
        data: []
    }
  };



  var option2 = {
    title: {
        top: 50,
        left: 'center',
        text: '总能耗日分布图'
    },
    tooltip : {
        trigger: 'axis',
        axisPointer : {            // 坐标轴指示器,坐标轴触发有效
            type : 'shadow'        // 默认为直线,可选为：'line' | 'shadow'
        }
    },
    legend: {
        top:90,
        data:['一楼','二楼','三楼空调','三楼照明','5号楼总能耗']
    },
    grid: {
        top:120,
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true
    },
    xAxis : [
        {
            type : 'time',
            // boundaryGap: ['8', '6'],
            min: '2018-01-07',
            max: '2018-06-28'
            // data : ['周一','周二','周三','周四','周五','周六','周日']
        }
    ],
    yAxis : [
        {
            type : 'value',
            name: 'kWh',
            nameLocation: 'end'
        }
    ],
    series : [
        {
            name:'一楼',
            type:'bar',
            stack: '能耗',
            barWidth: 3,
            data: []
        },
        {
            name:'二楼',
            type:'bar',
            stack: '能耗',
            barWidth: 3,
            data:[]
        },
        {
            name:'三楼空调',
            type:'bar',
            stack: '能耗',
            barWidth: 3,
            data: []
        },
        {
            name:'三楼照明',
            type:'bar',
            stack: '能耗',
            barWidth: 3,
            data: []
           
        },
        {
            name:'5号楼总能耗',
            type:'bar',
            barWidth: 3,
            data:[]
           
        }
    ]
  };


  myChart.setOption(option);
  myChart2.setOption(option2);
  myChart.showLoading();
  myChart2.showLoading();
  getechartsdata(myChart,myChart2);
  getechartsdata2(myChart2);

}

//从数据库获取json
function getechartsdata(myChart,myChart2) {
        var chartsdata = [];

        $.ajax({url:'http://118.24.110.98/echarts_calendar',
        type : "get",
        dataType: 'json',
        async:false, //同步执行
        success:function(data){
               for (var i = 0; i < data.length; i++) {
                onedaydata = [data[i].date,data[i].addEnergy];
                chartsdata.push(onedaydata);
              }

        myChart.hideLoading();
       myChart.setOption({
        series: [{
            // 根据名字对应到相应的系列
            name: '能耗日历',
            data: chartsdata
        }]
    });
        myChart2.setOption({
        series: [{
            // 根据名字对应到相应的系列
            name: '5号楼总能耗',
            data: chartsdata
        }]
    });

       }
     });
        
 }


//从数据库获取json
function getechartsdata2(myChart2) {
        var chartsdata2;

        $.ajax({url:'http://118.24.110.98/echarts_calendar_bar',
        type : "get",
        dataType: 'json',
        // async:false, //同步执行
        success:function(data){
               chartsdata2 = data;

               myChart2.hideLoading();
               myChart2.setOption({
        series: [{
            // 根据名字对应到相应的系列
            name: '一楼',
            data: getbardata(chartsdata2,'0x11')
        },
        {
            // 根据名字对应到相应的系列
            name: '二楼',
            data: getbardata(chartsdata2,'0x12')
        },
        {
            // 根据名字对应到相应的系列
            name: '三楼空调',
            data: getbardata(chartsdata2,'0x10')
        },
        {
            // 根据名字对应到相应的系列
            name: '三楼照明',
            data: getbardata(chartsdata2,'0x13')
        },
        ]
    });


       }
     });

        
 }

function getbardata(data,mac) {
        var chartsdata = [];
          for (var i = 0; i < data.length; i++) {
                if (data[i].mac == mac) {
                  onedaydata = [data[i].date,data[i].addEnergy];
                  chartsdata.push(onedaydata);
                }
                              
              }
          return chartsdata;
}