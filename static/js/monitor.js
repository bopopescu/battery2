// 1.打开monitor界面，显示目前通道的状态，以及其正在执行的测试方案以及测试数据，若其处于停止状态，则没有数据
// 2.monitor页面仅显示目前正在执行测试的通道的数据，历史测试数据应从其他页面检索
// 3.无论选择的通道是不是在工作，当前页面都会不断请求数据


var myChart = echarts.init(document.getElementById('U_I_t_chart'));
var myChart1 = echarts.init(document.getElementById('Q_t_chart'));
var myChart2 = echarts.init(document.getElementById('T_t_chart'));
var myChart3 = echarts.init(document.getElementById('T0_t_chart'));

var intID1;
var intID2;
var intID3;

var I = [];
var U = [];
var Q = {
    Q_H2: [],
    Q_CH4: [],
    Q_N2: [],
    Q_CO2: [],
    Q_Air: [],
    Q_H2O: []
};
var T = {
    T0: [],
    T1: [],
    T2: [],
    T3: [],
    T4: []
};

var refresh = 3000;

function set_interval() {
    refresh = (isNaN(Number.parseInt($("#refresh-int").val())) || (Number.parseInt($("#refresh-int").val()) <= 3000) ? 3000 : Number.parseInt($("#refresh-int").val()));
    console.log(refresh);
    clearInterval(intID1);
    clearInterval(intID2);
    clearInterval(intID3);
    var box_num = $('#box_num_selected option:selected').val();//选中的值
    var channel_num = $('#channel_num_selected option:selected').val();//选中的值
    if (box_num != undefined && channel_num != undefined) {
        intID1 = setInterval(get_realtime_data, refresh);
        intID2 = setInterval(show_brief_info, refresh);
        intID3 = setInterval(show_testline_status, refresh);
        alert("设置成功，开始刷新");
    }
    else {
        alert("设置失败");
    }
}

function stop_refresh() {
    clearInterval(intID1);
    clearInterval(intID2);
    clearInterval(intID3);
    alert("停止成功");
}

$(document).ready(function () {
        get_boxes();
        get_oven_status();
        get_cells_info();
        get_tests_info();
        var box_num = $('#box_num_selected option:selected').val();//选中的值
        var channel_num = $('#channel_num_selected option:selected').val();//选中的值
        if (box_num != undefined && channel_num != undefined) {
            show_chart();
            intID1 = setInterval(get_realtime_data, refresh);
            intID2 = setInterval(show_brief_info, refresh);
            intID3 = setInterval(show_testline_status, refresh);
            show_test_scheme();
        }
        window.onresize = function () {
            myChart.resize();
            myChart1.resize();
            myChart2.resize();
            myChart3.resize();
        };
    }
)


var box;

function get_boxes() {
    $("#box_num_selected").empty();
    $.ajax({
            url: "/get_b_c_num/",
            type: "get",
            dataType: 'json',
            async: false, //同步执行
            success: function (data) {
                box = data.box;
            }
        }
    )
    var b_num = document.getElementById("box_num_selected");
    if (box.length != 0)
        for (var i = 0; i < box.length; i++) {
            var option = document.createElement("option");
            option.setAttribute("value", box[i].id);
            option.innerText = box[i].id;
            b_num.appendChild(option);
        }
    $("#channel_num_selected").empty();
    if (box.length != 0)
        get_channels(box[0].id);
}

function show_channel() {
    var bid = $('#box_num_selected option:selected').val();
    get_channels(bid);
}

function get_channels(bid) {
    $("#channel_num_selected").empty();
    var c_num = document.getElementById("channel_num_selected");
    var bs;
    for (var i = 0; i < box.length; i++) {
        if (box[i].id == bid) {
            bs = box[i];
            break;
        }
    }
    if (bs != undefined) {
        for (var i = 0; i < bs.channel.length; i++) {
            var option = document.createElement("option");
            option.setAttribute("value", bs.channel[i]);
            option.innerText = bs.channel[i];
            c_num.appendChild(option);
        }
    }
}

function show_test_scheme() {
    var box_num = $('#box_num_selected option:selected').val();//选中的值
    var channel_num = $('#channel_num_selected option:selected').val();//选中的值
    var th = document.getElementById("table_head");
    var tb = document.getElementById("table_body");
    tb.innerHTML = "";
    if (box_num != undefined && channel_num != undefined)
        $.ajax({
            url: "get_test_scheme/" + box_num + "/" + channel_num + "/",
            type: "get",
            dataType: 'json',
            async: false, //同步执行
            success: parse_scheme_data
        });
}

function parse_scheme_data(data) {
    console.log(Object.keys(data));
    var sID = data.schemeID;
    var steps = data.steps;
    var tb = document.getElementById("table_body");
    var th = document.getElementById("table_head");

    create_table_body(tb, steps.length, $("#table_head").children().children().length);
    if (steps.length == 0)
        return false;
    insert_into_table(tb, 1, 1, sID);
    var col_name = Object.keys(steps[0]);
    console.log(col_name);
    for (var i = 1; i <= steps.length; i++) {
        for (var j = 1; j <= col_name.length; j++) {
            switch (col_name[j - 1]) {
                case "step":
                    insert_into_table(tb, i, 2, steps[i - 1][col_name[j - 1]]);
                    break;
                case "LoadMode":
                    insert_into_table(tb, i, 3, steps[i - 1][col_name[j - 1]]);
                    break;
                case "U":
                    insert_into_table(tb, i, 4, steps[i - 1][col_name[j - 1]]);
                    break;
                case "I":
                    insert_into_table(tb, i, 5, steps[i - 1][col_name[j - 1]]);
                    break;
                case "t_LM":
                    insert_into_table(tb, i, 6, steps[i - 1][col_name[j - 1]]);
                    break;
                case "U_LM":
                    insert_into_table(tb, i, 7, steps[i - 1][col_name[j - 1]]);
                    break;
                case "I_LM":
                    insert_into_table(tb, i, 8, steps[i - 1][col_name[j - 1]]);
                    break;
            }
        }
    }

}

function create_table_body(tb, rows, cols) {
    for (var i = 0; i < rows; i++) {
        var tr = document.createElement("tr");
        for (var j = 0; j < cols; j++) {
            var td = document.createElement("td");
            tr.appendChild(td);
        }
        tb.appendChild(tr);
    }
}

function insert_into_table(tb, row, col, content) {
    var rows = tb.children.length;
    var cols = tb.children[0].length;
    if (row > rows || col > cols) {
        console.log("越界");
        return;
    }
    var tr = tb.children[row - 1];
    var td = tr.children[col - 1];
    td.innerHTML = content;
}


function refresh_page() {
    clearInterval(intID1);
    clearInterval(intID2);
    clearInterval(intID3);
    var box_num = $('#box_num_selected option:selected').val();//选中的值
    var channel_num = $('#channel_num_selected option:selected').val();//选中的值
    if (box_num != undefined && channel_num != undefined) {
        show_chart();
        intID1 = setInterval(get_realtime_data, refresh);
        intID2 = setInterval(show_brief_info, refresh);
        intID3 = setInterval(show_testline_status, refresh);
        show_test_scheme();
        alert("成功");
    }
    else {
        alert("失败");
    }
}

function continue_testline() {
    var bid = parseInt($('#box_num_selected option:selected').val());
    var cid = parseInt($('#channel_num_selected option:selected').val());
    var data = {box: bid, channel: cid, plan: 0};
    if (bid != undefined && cid != undefined)
        $.ajax({
                url: "/control/continue_channel/",
                type: "post",
                data: JSON.stringify(data),
                dataType: 'json',
                async: false, //同步执行
                success: function (data) {
                    alert(data.Message);
                }
            }
        )
}

function pause_testline() {
    var bid = parseInt($('#box_num_selected option:selected').val());
    var cid = parseInt($('#channel_num_selected option:selected').val());
    var data = {box: bid, channel: cid, plan: 0};
    if (bid != undefined && cid != undefined)
        $.ajax({
                url: "/control/pause_channel/",
                type: "post",
                data: JSON.stringify(data),
                dataType: 'json',
                async: false, //同步执行
                success: function (data) {
                    alert(data.Message);
                }
            }
        )
}

function stop_testline() {
    var bid = parseInt($('#box_num_selected option:selected').val());
    var cid = parseInt($('#channel_num_selected option:selected').val());
    var data = {box: bid, channel: cid, plan: 0};
    if (bid != undefined && cid != undefined)
        $.ajax({
                url: "/control/stop_channel/",
                type: "post",
                data: JSON.stringify(data),
                dataType: 'json',
                async: false, //同步执行
                success: function (data) {
                    alert(data.Message);
                }
            }
        )
}


function show_chart() {
    var box_num = $('#box_num_selected option:selected').val();//选中的值
    var channel_num = $('#channel_num_selected option:selected').val();//选中的值
    if (box_num != undefined && channel_num != undefined)
        $.ajax({
            url: "get_testdata_from_start/" + box_num + "/" + channel_num + "/",
            type: "get",
            dataType: 'json',
            async: false, //同步执行
            success: function (data) {
                //console.log(data);
                I = data.I;
                U = data.U;
                Q.Q_CO2 = data.Q_CO2;
                Q.Q_CH4 = data.Q_CH4;
                Q.Q_Air = data.Q_Air;
                Q.Q_N2 = data.Q_N2;
                Q.Q_H2 = data.Q_H2;
                Q.Q_H2O = data.Q_H2O;
                T.T0 = data.T0;
                T.T1 = data.T1;
                T.T2 = data.T2;
                T.T3 = data.T3;
                T.T4 = data.T4;
                var option_U_I = {
                    legend: {
                        data: ["电压", "电流"]
                    },
                    axisPointer: {
                        animation: false
                    },
                    dataZoom: [{
                        type: 'slider',
                        show: true,
                        start: 0,
                        end: 100
                    },

                    ],
                    xAxis: {
                        type: "time",
                        splitLine: {
                            lineStyle: {
                                type: 'dashed'
                            }
                        },
                    },
                    yAxis: [{
                        name: '电压/mV',
                        type: 'value',
                        nameTextStyle: {
                            fontSize: 14
                        },
                        splitLine: {
                            lineStyle: {
                                type: 'dashed'
                            }
                        },
                        position: 'left',
                        boundaryGap: [0, '10%'],
                    }, {
                        name: '电流/mA',
                        type: 'value',
                        nameTextStyle: {
                            fontSize: 14
                        },
                        splitLine: {
                            lineStyle: {
                                type: 'dashed'
                            }
                        },
                        position: 'right',
                        boundaryGap: [0, '15%'],
                    }],
                    series: [{
                        name: '电压',
                        type: 'line',
                        showSymbol: false,
                        hoverAnimation: false,
                        data: U,
                        yAxisIndex: 0
                    }, {
                        name: '电流',
                        type: 'line',
                        showSymbol: false,
                        hoverAnimation: false,
                        data: I,
                        yAxisIndex: 1
                    }]
                };
                var option_Q = {
                    legend: {
                        data: ["氢气", "氮气", "甲烷", "二氧化碳", "空气", "水蒸汽"]
                    },
                    dataZoom: [{
                        type: 'slider',
                        show: true,
                        start: 0,
                        end: 100
                    },

                    ],
                    xAxis: {
                        type: "time",
                        splitLine: {
                            lineStyle: {
                                type: 'dashed'
                            }
                        },
                    },
                    yAxis: {
                        name: '流量/ccm',
                        type: 'value',
                        nameTextStyle: {
                            fontSize: 14
                        },
                        splitLine: {
                            lineStyle: {
                                type: 'dashed'
                            }
                        },
                        position: 'left',
                        boundaryGap: [0, '10%'],
                    },
                    series: [{
                        name: '氢气',
                        type: 'line',
                        showSymbol: false,
                        hoverAnimation: false,
                        data: Q.Q_H2,
                    }, {
                        name: '氮气',
                        type: 'line',
                        showSymbol: false,
                        hoverAnimation: false,
                        data: Q.Q_N2,
                    }, {
                        name: '空气',
                        type: 'line',
                        showSymbol: false,
                        hoverAnimation: false,
                        data: Q.Q_Air,
                    }, {
                        name: '甲烷',
                        type: 'line',
                        showSymbol: false,
                        hoverAnimation: false,
                        data: Q.Q_CH4,
                    }, {
                        name: '二氧化碳',
                        type: 'line',
                        showSymbol: false,
                        hoverAnimation: false,
                        data: Q.Q_CO2,
                    }, {
                        name: '水蒸汽',
                        type: 'line',
                        showSymbol: false,
                        hoverAnimation: false,
                        data: Q.Q_H2O,
                    }]
                };
                var option_T = {
                    legend: {
                        data: ["测温点1", "测温点2", "测温点3", "测温点4"]
                    },
                    dataZoom: [{
                        type: 'slider',
                        show: true,
                        start: 0,
                        end: 100
                    },
                    ],
                    xAxis: {
                        type: "time",
                        splitLine: {
                            lineStyle: {
                                type: 'dashed'
                            }
                        },
                    },
                    yAxis: {
                        name: '温度/°C',
                        type: 'value',
                        nameTextStyle: {
                            fontSize: 14
                        },
                        splitLine: {
                            lineStyle: {
                                type: 'dashed'
                            }
                        },
                        position: 'left',
                        boundaryGap: [0, '10%'],
                    },
                    series: [{
                        name: '测温点1',
                        type: 'line',
                        showSymbol: false,
                        hoverAnimation: false,
                        data: T.T1,
                    }, {
                        name: '测温点2',
                        type: 'line',
                        showSymbol: false,
                        hoverAnimation: false,
                        data: T.T2,
                    }, {
                        name: '测温点3',
                        type: 'line',
                        showSymbol: false,
                        hoverAnimation: false,
                        data: T.T3,
                    }, {
                        name: '测温点4',
                        type: 'line',
                        showSymbol: false,
                        hoverAnimation: false,
                        data: T.T4,
                    }]
                };
                var option_T0 = {
                    legend: {
                        data: ["控温点"]
                    },
                    dataZoom: [{
                        type: 'slider',
                        show: true,
                        start: 0,
                        end: 100
                    },
                    ],
                    xAxis: {
                        type: "time",
                        splitLine: {
                            lineStyle: {
                                type: 'dashed'
                            }
                        },
                    },
                    yAxis: {
                        name: '温度/°C',
                        type: 'value',
                        nameTextStyle: {
                            fontSize: 14
                        },
                        splitLine: {
                            lineStyle: {
                                type: 'dashed'
                            }
                        },
                        position: 'left',
                        boundaryGap: [0, '10%'],
                    },
                    series: [{
                        name: '控温点',
                        type: 'line',
                        showSymbol: false,
                        hoverAnimation: false,
                        data: T.T0,
                    }]
                };
                myChart.setOption(option_U_I);
                myChart1.setOption(option_Q);
                myChart2.setOption(option_T);
                myChart3.setOption(option_T0);

            }
        });
}

function get_realtime_data() {
    var box_num = $('#box_num_selected option:selected').val();//选中的值
    var channel_num = $('#channel_num_selected option:selected').val();//选中的值
    if (box_num != undefined && channel_num != undefined)
        $.ajax({
            url: "get_testdata_real_time/" + box_num + "/" + channel_num + "/",
            type: "get",
            dataType: 'json',
            async: false, //同步执行
            success: function (data) {
                //console.log(data);
                if (data.I != I[I.length - 1])
                    I.push(data.I);
                if (data.U != U[U.length - 1])
                    U.push(data.U);
                if (data.Q_CO2 != Q.Q_CO2[Q.Q_CO2.length - 1])
                    Q.Q_CO2.push(data.Q_CO2);
                if (data.Q_CH4 != Q.Q_CH4[Q.Q_CH4.length - 1])
                    Q.Q_CH4.push(data.Q_CH4);
                if (data.Q_Air != Q.Q_Air[Q.Q_Air.length - 1])
                    Q.Q_Air.push(data.Q_Air);
                if (data.Q_N2 != Q.Q_N2[Q.Q_N2.length - 1])
                    Q.Q_N2.push(data.Q_N2);
                if (data.Q_H2 != Q.Q_H2[Q.Q_H2.length - 1])
                    Q.Q_H2.push(data.Q_H2);
                if (data.Q_H2O != Q.Q_H2O[Q.Q_H2O.length - 1])
                    Q.Q_H2O.push(data.Q_H2O);
                if (data.T0 != T.T0[T.T0.length - 1])
                    T.T0.push(data.T0);
                if (data.T1 != T.T1[T.T1.length - 1])
                    T.T1.push(data.T1);
                if (data.T2 != T.T2[T.T2.length - 1])
                    T.T2.push(data.T2);
                if (data.T3 != T.T3[T.T3.length - 1])
                    T.T3.push(data.T3);
                if (data.T4 != T.T4[T.T4.length - 1])
                    T.T4.push(data.T4);
                myChart.setOption({
                    series: [{
                        data: U
                    }, {
                        data: I
                    }]
                });
                myChart1.setOption({
                    series: [{
                        data: Q.Q_N2
                    }, {
                        data: Q.Q_N2
                    }, {
                        data: Q.Q_Air
                    }, {
                        data: Q.Q_CH4
                    }, {
                        data: Q.Q_CO2
                    }, {
                        data: Q.Q_H2O
                    }]
                });
                myChart2.setOption({
                    series: [{
                        data: T.T1
                    }, {
                        data: T.T2
                    }, {
                        data: T.T3
                    }, {
                        data: T.T4
                    }]
                });
                myChart3.setOption({
                    series: [{
                        data: T.T0
                    }]
                });
            }
        });
}

function show_brief_info() {
    var box_num = $('#box_num_selected option:selected').val();//选中的值
    var channel_num = $('#channel_num_selected option:selected').val();//选中的值

    if (box_num != undefined && channel_num != undefined)
        $.ajax({
            url: "testline_info/" + box_num + "/" + channel_num + "/",
            type: "get",
            dataType: 'json',
            async: false, //同步执行
            success: get_info_success
        })
}

function get_info_success(data) {
    for (var i in data) {
        var variables = document.getElementById(i + "_val");
        if (variables != null)
            variables.innerText = data[i];
    }
}

function show_testline_status() {
    var box_num = $('#box_num_selected option:selected').val();//选中的值
    var channel_num = $('#channel_num_selected option:selected').val();//选中的值
    if (box_num != undefined && channel_num != undefined)
        $.ajax({
            url: "testline_status/" + box_num + "/" + channel_num + "/",
            type: "get",
            dataType: 'json',
            async: false, //同步执行
            success: get_status_success
        })
}

function get_status_success(data) {
    //console.log(data);
    var status = document.getElementById("testline_status");
    if (data.testline_status == "start") {
        status.setAttribute("class", "label label-success");
        status.innerText = "正在运行";
    }
    else if (data.testline_status == "pause") {
        status.setAttribute("class", "label label-warning");
        status.innerText = "暂停中";
    }
    else if (data.testline_status == "stop") {
        status.setAttribute("class", "label label-danger");
        status.innerText = "已停止";
    }
    else {
        status.setAttribute("class", "label label-default");
        status.innerText = "未知";
    }
}


function get_oven_status() {
    $.ajax({
        url: "oven_status/",
        type: "get",
        dataType: 'json',
        async: false, //同步执行
        success: function (data) {
            data = data.oven;
            var oven_num = data.length;
            if (oven_num != 0) {
                var tb = document.getElementById("oven_status_tablebody");
                create_table_body(tb, oven_num, 5);
                for (var i = 1; i <= oven_num; i++) {
                    insert_into_table(tb, i, 1, data[i - 1].ID);
                    insert_into_table(tb, i, 2, data[i - 1].curr);
                    insert_into_table(tb, i, 3, data[i - 1].next);
                    insert_into_table(tb, i, 4, data[i - 1].T);
                    insert_into_table(tb, i, 5, data[i - 1].PlanID);
                }

            }
        }
    })
}

function get_cells_info() {
    $.ajax({
        url: "cells_info/",
        type: "get",
        dataType: 'json',
        async: false, //同步执行
        success: function (data) {
            data = data.cells;
            var cell_num = data.length;
            if (cell_num != 0) {
                var tb = document.getElementById("device_relation_tablebody");
                create_table_body(tb, cell_num, 11);
                for (var i = 1; i <= cell_num; i++) {
                    insert_into_table(tb, i, 1, data[i - 1].cellID);
                    insert_into_table(tb, i, 2, data[i - 1].boxID);
                    insert_into_table(tb, i, 3, data[i - 1].chnNum);
                    insert_into_table(tb, i, 4, data[i - 1].ovenID);
                    insert_into_table(tb, i, 5, data[i - 1].H2ID);
                    insert_into_table(tb, i, 6, data[i - 1].N2ID);
                    insert_into_table(tb, i, 7, data[i - 1].H2OID);
                    insert_into_table(tb, i, 8, data[i - 1].CO2ID);
                    insert_into_table(tb, i, 9, data[i - 1].CH4ID);
                    insert_into_table(tb, i, 10, data[i - 1].AIRID);
                    insert_into_table(tb, i, 11, data[i - 1].wdjID);
                }

            }
        }
    })
}

function get_tests_info() {
    $.ajax({
        url: "tests_info/",
        type: "get",
        dataType: 'json',
        async: false, //同步执行
        success: function (data) {
            data = data.tests;
            var test_num = data.length;
            if (test_num != 0) {
                var tb = document.getElementById("tests_info_tablebody");
                create_table_body(tb, test_num, 16);
                for (var i = 1; i <= test_num; i++) {
                    insert_into_table(tb, i, 1, data[i - 1].BigTestID);
                    insert_into_table(tb, i, 2, data[i - 1].TestID);
                    insert_into_table(tb, i, 3, data[i - 1].CellID);
                    insert_into_table(tb, i, 4, data[i - 1].BoxID);
                    insert_into_table(tb, i, 5, data[i - 1].ChnID);
                    insert_into_table(tb, i, 6, data[i - 1].PlanID);
                    insert_into_table(tb, i, 7, data[i - 1].OvenID);
                    insert_into_table(tb, i, 8, data[i - 1].OvenPlanID);
                    insert_into_table(tb, i, 9, data[i - 1].H2ID);
                    insert_into_table(tb, i, 10, data[i - 1].N2ID);
                    insert_into_table(tb, i, 11, data[i - 1].H2OID);
                    insert_into_table(tb, i, 12, data[i - 1].CO2ID);
                    insert_into_table(tb, i, 13, data[i - 1].CH4ID);
                    insert_into_table(tb, i, 14, data[i - 1].AIRID);
                    insert_into_table(tb, i, 15, data[i - 1].StartTime);
                    insert_into_table(tb, i, 16, data[i - 1].EndTime);
                }

            }
        }
    })
}