$(document).ready(function(){

get_initialize();
// get_table();

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

    $('#hour_tab').prop("checked",true);
    $('#meter_tab').prop("checked",true);

    date_time = new Datetime();

    var beginTimeStore = '';
    var endTimeStore = '';
    $('#daterangepicker').daterangepicker({
        "linkedCalendars": true,
        "autoUpdateInput": false,
        "opens":"right",
        // "startDate":moment().subtract(2,'days'),
        "minDate":"2018-01-09",
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
    changeoption('device');
    document.getElementById("daterangepicker").value = date_time.todaydatetext+"~"+date_time.todaydatetext;
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

function get_option_api(obj_type) {
    var objurl = obj_type + 'list';
    var result;
    $.ajax({
        url:'/api/'+ objurl,
        type:'GET',
        dataType: 'json',
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

function get_report() {
    var optObj=new Object();
    optObj.timeOption =$('[name=timeOption]:checked').val();
    optObj.typeOption =$('[name=typeOption]:checked').val();
    optObj.objOption =$('[name=objOption]').val();
    optObj.date =$('[name=date]').val();
    var urlopt = $.param(optObj);
    var result;
    $.ajax({
        url:'/getreport/?' + urlopt,
        type:'GET',
        dataType: 'json',
        async:false,
        success:function(data_result){
            result = data_result;
        }
    });

    return result;


}


function get_csv() {
    $('#table').tableExport({type:'csv'});
}

function get_table() {
    $('#table').bootstrapTable('destroy');
    var optObj=new Object();
    optObj.timeOption =$('[name=timeOption]:checked').val();
    optObj.typeOption =$('[name=typeOption]:checked').val();
    optObj.objOption =$('[name=objOption]').val();
    optObj.date =$('[name=date]').val();
    var urlopt = $.param(optObj);
        $('#table').bootstrapTable({
            url: '/getreport/?' + urlopt,                           //请求后台的URL（*）
            method: 'get',                     //请求方式（*）
            // toolbar: toolbar,                   //工具按钮用哪个容器
            striped: true,                      //是否显示行间隔色
            cache: false,                       //是否使用缓存，默认为true，所以一般情况下需要设置一下这个属性（*）
            pagination: true,                   //是否显示分页（*）
            sortable: true,                    //是否启用排序
            sortOrder: "asc",                   //排序方式
            queryParams: queryParams,           //传递参数（*），这里应该返回一个object，即形如{param1:val1,param2:val2}
            sidePagination: "client",           //分页方式：client客户端分页，server服务端分页（*）
            pageNumber:1,                       //初始化加载第一页，默认第一页
            pageSize: 20,                       //每页的记录行数（*）
            pageList: [20, 50, 100],            //可供选择的每页的行数（*）
            search: false,                       //是否显示表格搜索，此搜索是客户端搜索，不会进服务端，所以，个人感觉意义不大
            strictSearch: true,
            showColumns: true,                  //是否显示所有的列
            showRefresh: false,                  //是否显示刷新按钮
            minimumCountColumns: 2,             //最少允许的列数
            clickToSelect: true,                //是否启用点击选中行
            //height: 500,                      //行高，如果没有设置height属性，表格自动根据记录条数觉得表格高度
            uniqueId: "id",                     //每一行的唯一标识，一般为主键列
            showToggle:false,                    //是否显示详细视图和列表视图的切换按钮
            cardView: false,                    //是否显示详细视图
            detailView: false,                  //是否显示父子表
            showExport: true,
            exportDataType:'all',
            exportTypes:['csv'],
            columns:getcolumns(optObj.objOption)
            // columns: createCols(params,'标题',true),
            // data: [{
            //     id: 1,
            //     name: 'Item 1',
            //     price: '$1'
            // }, {
            //     id: 2,
            //     name: 'Item 2',
            //     price: '$2'
            // }]
            });
}

function getcolumns(obj) {
    var columns;
    if(obj === 'all'){

    }else {
        columns =[
                {
                    field: 'time',
                    title: '时间',
                    align: 'center',
                    valign: 'middle',
                    sortable: true
                    }, {
                    field: 'adde',
                    title: '能耗(kWh)',
                    align: 'center',
                    valign: 'top',
                    sortable: true
                    }
            ];
    }
    return columns;
}

function createCols(params,titles,hasCheckbox) {
        if(params.length!=titles.length)
            return null;
        var arr = [];
        if(hasCheckbox)
        {
            var objc = {};
            objc.checkbox = true;
            arr.push(objc);
        }
        for(var i = 0;i<params.length;i++)
        {
            var obj = {};
            obj.field = params[i];
            obj.title = titles[i];
            arr.push(obj);
        }
        return arr;
    }

//可发送给服务端的参数：limit->pageSize,offset->pageNumber,search->searchText,sort->sortName(字段),order->sortOrder('asc'或'desc')
function queryParams(params) {
        return {   //这里的键的名字和控制器的变量名必须一直，这边改动，控制器也需要改成一样的
            limit: params.limit,   //页面大小
            offset: params.offset  //页码
            //name: $("#txt_name").val()//关键字查询
        };
    }
    