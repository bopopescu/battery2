// 1.查询测试方案库，并显示历史测试方案
// 2.新建测试方案，并保存
// 3.在测试方案库中选择一测试方案，指定通道号，执行
var old_scheme_list = [];
var old_oven_scheme_list = [];
// $(document).ready(function () {
//     get_boxes();
//     show_old_scheme_table();
//     show_old_oven_scheme_table();
//     create_new_row();
//     oven_create_new_row();
//
//     show_gas_table();
//
// });

function show_old_oven_scheme_table() {
    $("#old-oven-scheme-table-body").empty();
    var old_scheme_num;
    $.ajax({
        url: "/control/get_old_oven_scheme/",
        type: "get",
        dataType: 'json',
        async: false, //同步执行
        success: function (data) {
            old_scheme_num = data.old_scheme_num;
            old_oven_scheme_list = data.old_scheme_list;
            var tb = document.getElementById("old-oven-scheme-table-body");
            create_old_table_body(tb, old_scheme_num, 3);
            complete_old_table_body(tb, old_oven_scheme_list);
            $("#oven_scheme_num_selected").empty();
            var sn = document.getElementById("oven_scheme_num_selected");
            for (var i = 0; i < old_oven_scheme_list.length; i++) {
                var option = document.createElement("option");
                option.setAttribute("value", old_oven_scheme_list[i].id);
                option.innerText = old_oven_scheme_list[i].id;
                sn.appendChild(option);
            }
        }
    });
}

function show_old_scheme_table() {
    $("#old-scheme-table-body").empty();
    var old_scheme_num;
    $.ajax({
        url: "/control/get_old_scheme/",
        type: "get",
        dataType: 'json',
        async: false, //同步执行
        success: function (data) {
            old_scheme_num = data.old_scheme_num;
            old_scheme_list = data.old_scheme_list;
            var tb = document.getElementById("old-scheme-table-body");
            create_old_table_body(tb, old_scheme_num, 3);
            complete_old_table_body(tb, old_scheme_list);
            $("#scheme_num_selected").empty();
            var sn = document.getElementById("scheme_num_selected");
            for (var i = 0; i < old_scheme_list.length; i++) {
                var option = document.createElement("option");
                option.setAttribute("value", old_scheme_list[i].id);
                option.innerText = old_scheme_list[i].id;
                sn.appendChild(option);
            }
        }
    });
}

function complete_old_table_body(tb, scheme_list) {
    for (var i = 0; i < scheme_list.length; i++) {
        var td = get_table_cell(tb, i + 1, 1);
        var checkbox = document.createElement("input");
        checkbox.setAttribute("type", "checkbox");
        td.appendChild(checkbox);
        td = get_table_cell(tb, i + 1, 2);
        td.innerText = scheme_list[i].name;
        td = get_table_cell(tb, i + 1, 3);
        td.innerText = scheme_list[i].id;
    }
}

function create_old_table_body(tb, rows, cols) {
    for (var i = 0; i < rows; i++) {
        var tr = document.createElement("tr");
        for (j = 0; j < cols; j++) {
            var td = document.createElement("td");
            tr.appendChild(td);
        }
        tb.appendChild(tr);
    }
}

function get_table_cell(tb, row, col) {
    var rows = tb.children.length;
    var cols = tb.children[0].length;
    if (row > rows || col > cols) {
        console.log("越界" + "rows:" + rows + "/" + row + "  " + "cols:" + cols + "/" + col);
        return;
    }
    var tr = tb.children[row - 1];
    var td = tr.children[col - 1];
    return td;
}

function show_old_scheme() {
    var tb = document.getElementById("old-scheme-table-body");
    var checked_scheme;
    for (var i = 1; i <= old_scheme_list.length; i++) {
        var checkbox = get_table_cell(tb, i, 1);
        if (checkbox.children[0].checked) {
            checked_scheme = old_scheme_list[i - 1];
            break
        }
    }
    $("#new-scheme-table-body").empty();
    var tb = document.getElementById("new-scheme-table-body");
    for (var i = 0; i < checked_scheme.steps.length; i++) {
        create_new_row();
    }
    for (var i = 1; i <= checked_scheme.steps.length; i++) {
        for (var j = 3; j <= 8; j++) {
            var td = get_table_cell(tb, i, j);
            switch (j) {
                case 3:
                    td.children[0].value = checked_scheme.steps[i - 1].LoadMode;
                    break;
                case 4:
                    td.children[0].value = checked_scheme.steps[i - 1].U;
                    break;
                case 5:
                    td.children[0].value = checked_scheme.steps[i - 1].I;
                    break;
                case 6:
                    td.children[0].value = checked_scheme.steps[i - 1].t_LM;
                    break;
                case 7:
                    td.children[0].value = checked_scheme.steps[i - 1].U_LM;
                    break;
                case 8:
                    td.children[0].value = checked_scheme.steps[i - 1].I_LM;
                    break;
            }
        }
    }
}

function show_old_oven_scheme() {
    var tb = document.getElementById("old-oven-scheme-table-body");
    var checked_scheme;
    for (var i = 1; i <= old_oven_scheme_list.length; i++) {
        var checkbox = get_table_cell(tb, i, 1);
        if (checkbox.children[0].checked) {
            checked_scheme = old_oven_scheme_list[i - 1];
            break
        }
    }
    $("#new-oven-scheme-table-body").empty();
    var tb = document.getElementById("new-oven-scheme-table-body");
    for (var i = 0; i < checked_scheme.steps.length; i++) {
        oven_create_new_row();
    }
    for (var i = 1; i <= checked_scheme.steps.length; i++) {
        for (var j = 3; j <= 4; j++) {
            var td = get_table_cell(tb, i, j);
            switch (j) {
                case 3:
                    td.children[0].value = checked_scheme.steps[i - 1].T;
                    break;
                case 4:
                    td.children[0].value = checked_scheme.steps[i - 1].time;
                    break;
            }
        }
    }

}


function delete_old_scheme() {
    var tb = document.getElementById("old-scheme-table-body");
    var checked_row;
    for (var i = 1; i <= old_scheme_list.length; i++) {
        var checkbox = get_table_cell(tb, i, 1);
        if (checkbox.children[0].checked) {
            checked_row = i;
            break
        }
        //console.log(checkbox.children[0].checked);
    }
    $.ajax({
        url: "/control/delete_old_scheme/" + checked_row.toString(),
        type: "get",
        dataType: 'json',
        async: false, //同步执行
        success: function (data) {
            show_old_scheme_table();
        }
    });
}

function save_scheme() {
    var new_scheme = parse_new_scheme();
    $.ajax({
        url: "/control/save_scheme/",
        type: "post",
        data: JSON.stringify(new_scheme),
        dataType: 'json',
        async: false, //同步执行
        success: function (data) {
            show_old_scheme_table();
        }
    });
}

function save_oven_scheme() {
    var new_scheme = parse_new_oven_scheme();
    $.ajax({
        url: "/control/save_oven_scheme/",
        type: "post",
        data: JSON.stringify(new_scheme),
        dataType: 'json',
        async: false, //同步执行
        success: function (data) {
            show_old_oven_scheme_table();
        }
    });
}

function parse_new_scheme() {
    var tb = document.getElementById("new-scheme-table-body");
    var tr = tb.getElementsByTagName("tr");
    var new_scheme = {};
    new_scheme.name = $("#new-scheme-name").val();
    new_scheme.steps = [];
    for (var i = 0; i < tr.length; i++) {
        var step = {};
        for (var j = 2; j <= 8; j++) {
            var td = get_table_cell(tb, i + 1, j);
            switch (j) {
                case 2:
                    step.step = parseInt(td.innerText);
                    break;
                case 3:
                    step.LoadMode = td.children[0].value;
                    break;
                case 4:
                    step.U = parseFloat(td.children[0].value);
                    break;
                case 5:
                    step.I = parseFloat(td.children[0].value);
                    break;
                case 6:
                    step.t_LM = parseFloat(td.children[0].value);
                    break;
                case 7:
                    step.U_LM = parseFloat(td.children[0].value);
                    break;
                case 8:
                    step.I_LM = parseFloat(td.children[0].value);
                    break;

            }
        }
        new_scheme.steps.push(step);
    }
    return new_scheme;
}

function parse_new_oven_scheme() {
    var tb = document.getElementById("new-oven-scheme-table-body");
    var tr = tb.getElementsByTagName("tr");
    var new_scheme = {};
    new_scheme.name = $("#new-oven-scheme-name").val();
    new_scheme.steps = [];
    for (var i = 0; i < tr.length; i++) {
        var step = {};
        for (var j = 2; j <= 4; j++) {
            var td = get_table_cell(tb, i + 1, j);
            switch (j) {
                case 2:
                    step.step = parseInt(td.innerText);
                    break;
                case 3:
                    step.T = parseFloat(td.children[0].value);
                    break;
                case 4:
                    step.time = parseFloat(td.children[0].value);
                    break;
            }
        }
        new_scheme.steps.push(step);
    }
    return new_scheme;
}


function create_new_scheme() {
    $("#new-scheme-table-body").empty();
    create_new_row();
}

function create_new_oven_scheme() {
    $("#new-oven-scheme-table-body").empty();
    oven_create_new_row();
}


function oven_delete_row() {
    var tbody = document.getElementById("new-oven-scheme-table-body");
    var tr = tbody.getElementsByTagName("tr");
    var tr_num = tr.length;
    for (var i = 0; i < tr_num;) {
        var button = tr[i].childNodes[0].childNodes[0];
        if (button.checked) {
            tr_num--;
            tbody.removeChild(tr[i]);
        }
        else {
            i++;
        }
    }
    oven_table_number_refresh();
}

function delete_row() {
    var tbody = document.getElementById("new-scheme-table-body");
    var tr = tbody.getElementsByTagName("tr");
    var tr_num = tr.length;
    for (var i = 0; i < tr_num;) {
        var button = tr[i].childNodes[0].childNodes[0];
        if (button.checked) {
            tr_num--;
            tbody.removeChild(tr[i]);
        }
        else {
            i++;
        }
    }
    table_number_refresh();
}

function oven_insert_row() {
    var tbody = document.getElementById("new-oven-scheme-table-body");
    var tr = tbody.getElementsByTagName("tr");
    var tr_num = tr.length;
    for (var i = 0; i < tr_num;) {
        var button = tr[i].childNodes[0].childNodes[0];
        if (button.checked) {
            var tr_new = document.createElement("tr");
            tbody.insertBefore(tr_new, tr[i]);
            var thead = document.getElementById("oven-table-head-content");
            for (var j = 0; j < thead.getElementsByTagName("th").length; j++) {
                var td = document.createElement("td");
                tr_new.appendChild(td);
                var cellcontent = null;
                if (j == 0) {
                    cellcontent = document.createElement("input");
                    cellcontent.setAttribute("type", "checkbox");
                    td.appendChild(cellcontent);
                }
                else if (j == 1) {
                    //cellcontent=document.createTextNode("1");
                }
                else {
                    cellcontent = document.createElement("input");
                    cellcontent.setAttribute("type", "text");
                    td.appendChild(cellcontent);
                }
            }
            i = i + 2;
            tr_num++;
        }
        else {
            i++;
        }
    }
    oven_table_number_refresh();
}

function insert_row() {
    var tbody = document.getElementById("new-scheme-table-body");
    var tr = tbody.getElementsByTagName("tr");
    var tr_num = tr.length;
    for (var i = 0; i < tr_num;) {
        var button = tr[i].childNodes[0].childNodes[0];
        if (button.checked) {
            var tr_new = document.createElement("tr");
            tbody.insertBefore(tr_new, tr[i]);
            var thead = document.getElementById("table-head-content");
            for (var j = 0; j < thead.getElementsByTagName("th").length; j++) {
                var td = document.createElement("td");
                tr_new.appendChild(td);
                var cellcontent = null;
                if (j == 0) {
                    cellcontent = document.createElement("input");
                    cellcontent.setAttribute("type", "checkbox");
                    td.appendChild(cellcontent);
                }
                else if (j == 1) {
                    //cellcontent=document.createTextNode("1");
                }
                else {
                    cellcontent = document.createElement("input");
                    cellcontent.setAttribute("type", "text");
                    td.appendChild(cellcontent);
                }
            }
            i = i + 2;
            tr_num++;
        }
        else {
            i++;
        }
    }
    table_number_refresh();
}

function oven_row_go_up() {
    var tbody = document.getElementById("new-oven-scheme-table-body");
    var tr = tbody.getElementsByTagName("tr");
    var tr_num = tr.length;
    for (var i = 0; i < tr_num; i++) {
        var button = tr[i].childNodes[0].childNodes[0];
        if (button.checked) {
            if (i == 0)
                continue;
            else {
                var tr_up = tr[i - 1].cloneNode(true);
                var tr_down = tr[i].cloneNode(true);
                tbody.replaceChild(tr_down, tr[i - 1]);
                tbody.replaceChild(tr_up, tr[i]);
            }
        }
    }
    oven_table_number_refresh();
}

function row_go_up() {
    var tbody = document.getElementById("new-scheme-table-body");
    var tr = tbody.getElementsByTagName("tr");
    var tr_num = tr.length;
    for (var i = 0; i < tr_num; i++) {
        var button = tr[i].childNodes[0].childNodes[0];
        if (button.checked) {
            if (i == 0)
                continue;
            else {
                var tr_up = tr[i - 1].cloneNode(true);
                var tr_down = tr[i].cloneNode(true);
                tbody.replaceChild(tr_down, tr[i - 1]);
                tbody.replaceChild(tr_up, tr[i]);
            }

        }
    }
    table_number_refresh();
}

function oven_row_go_down() {
    var tbody = document.getElementById("new-oven-scheme-table-body");
    var tr = tbody.getElementsByTagName("tr");
    var tr_num = tr.length;
    for (var i = tr_num - 1; i >= 0; i--) {
        var button = tr[i].childNodes[0].childNodes[0];
        if (button.checked) {
            if (i == (tr_num - 1))
                continue;
            else {
                var tr_up = tr[i].cloneNode(true);
                var tr_down = tr[i + 1].cloneNode(true);
                tbody.replaceChild(tr_down, tr[i]);
                tbody.replaceChild(tr_up, tr[i + 1]);
            }

        }
    }
    oven_table_number_refresh();
}

function row_go_down() {
    var tbody = document.getElementById("new-scheme-table-body");
    var tr = tbody.getElementsByTagName("tr");
    var tr_num = tr.length;
    for (var i = tr_num - 1; i >= 0; i--) {
        var button = tr[i].childNodes[0].childNodes[0];
        if (button.checked) {
            if (i == (tr_num - 1))
                continue;
            else {
                var tr_up = tr[i].cloneNode(true);
                var tr_down = tr[i + 1].cloneNode(true);
                tbody.replaceChild(tr_down, tr[i]);
                tbody.replaceChild(tr_up, tr[i + 1]);
            }

        }
    }
    table_number_refresh();
}

function oven_create_new_row() {
    var tbody = document.getElementById("new-oven-scheme-table-body");
    var tr = document.createElement("tr");
    tbody.appendChild(tr);
    var thead = document.getElementById("oven-table-head-content");
    for (var i = 0; i < thead.getElementsByTagName("th").length; i++) {
        var td = document.createElement("td");
        tr.appendChild(td);
        var cellcontent = null;
        if (i == 0) {
            cellcontent = document.createElement("input");
            cellcontent.setAttribute("type", "checkbox");
            td.appendChild(cellcontent);
        }
        else if (i == 1) {
            //cellcontent=document.createTextNode("1");
        }
        else {
            cellcontent = document.createElement("input");
            cellcontent.setAttribute("type", "text");
            cellcontent.setAttribute("style", "width:100px");
            td.appendChild(cellcontent);
        }
    }
    oven_table_number_refresh();
}

function create_new_row() {
    var tbody = document.getElementById("new-scheme-table-body");
    var tr = document.createElement("tr");
    tbody.appendChild(tr);
    var thead = document.getElementById("table-head-content");
    for (var i = 0; i < thead.getElementsByTagName("th").length; i++) {
        var td = document.createElement("td");
        tr.appendChild(td);
        var cellcontent = null;
        if (i == 0) {
            cellcontent = document.createElement("input");
            cellcontent.setAttribute("type", "checkbox");
            td.appendChild(cellcontent);
        }
        else if (i == 1) {
            //cellcontent=document.createTextNode("1");
        }
        else {
            cellcontent = document.createElement("input");
            cellcontent.setAttribute("type", "text");
            cellcontent.setAttribute("style", "width:100px");
            td.appendChild(cellcontent);
        }
    }
    table_number_refresh();
}

function oven_table_number_refresh() {
    var tbody = document.getElementById("new-oven-scheme-table-body");
    var tr = tbody.getElementsByTagName("tr");
    var row_num = tr.length;
    for (var i = 1; i <= tr.length; i++) {
        var td = tr[i - 1].getElementsByTagName("td");
        td[1].innerText = i.toString();
    }
}

function table_number_refresh() {
    var tbody = document.getElementById("new-scheme-table-body");
    var tr = tbody.getElementsByTagName("tr");
    var row_num = tr.length;
    for (var i = 1; i <= tr.length; i++) {
        var td = tr[i - 1].getElementsByTagName("td");
        td[1].innerText = i.toString();
    }
}

function clear_table() {
    $("#test-scheme-table").empty();
}

function create_tablehead() {
    var table = document.getElementById("test-scheme-table");
    var tablehead = document.createElement("thead");
    table.appendChild(tablehead);
    var tableheadcontent = document.createElement("tr");
    tablehead.appendChild(tableheadcontent);
    tableheadcontent.setAttribute("id", "table-head-content");
    tablehead.setAttribute("id", "table-head");
    tablehead.setAttribute("class", "thead-dark");

    var tablebody = document.createElement("tbody");
    table.appendChild(tablebody);
    tablebody.setAttribute("id", "tbody");

    var columns = ["#", "工步号", "负载工作模式", "U/I", "H2", "Air", "N2", "CH4", "CO2", "T", "停止方式", "停止条件"];
    for (var i in columns) {
        var para = document.createElement("th");
        var node = document.createTextNode(columns[i]);
        para.appendChild(node);
        tableheadcontent.appendChild(para);
    }


}

var box;
var oven;

function get_boxes() {
    $("#box_num_selected").empty();
    $.ajax({
            url: "/get_b_c_num/",
            type: "get",
            dataType: 'json',
            async: false, //同步执行
            success: function (data) {
                box = data.box;
                oven = data.oven;
            }
        }
    )
    var b_num = document.getElementById("box_num_selected");
    if (b_num != undefined)
        for (var i = 0; i < box.length; i++) {
            var option = document.createElement("option");
            option.setAttribute("value", box[i].id);
            option.innerText = box[i].id;
            b_num.appendChild(option);
        }
    var o_num = document.getElementById("oven_num_selected");
    if (o_num != undefined)
        for (var i = 0; i < oven.length; i++) {
            var option = document.createElement("option");
            option.setAttribute("value", oven[i].id);
            option.innerText = oven[i].id;
            o_num.appendChild(option);
        }
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
    if (c_num != undefined)
        for (var i = 0; i < bs.channel.length; i++) {
            var option = document.createElement("option");
            option.setAttribute("value", bs.channel[i]);
            option.innerText = bs.channel[i];
            c_num.appendChild(option);
        }
}

function start_channel() {
    var bid = parseInt($('#box_num_selected option:selected').val());
    var cid = parseInt($('#channel_num_selected option:selected').val());
    var sid = parseInt($('#scheme_num_selected option:selected').val());
    var osid = parseInt($('#scheme_num_selected option:selected').val());
    var data = {box: bid, channel: cid, plan: sid, oplan: osid};
    $.ajax({
            url: "/control/start_channel/",
            type: "post",
            data: JSON.stringify(data),
            dataType: 'json',
            async: false, //同步执行
            success: function (data) {
                //window.location.href = "/monitor/";
            }
        }
    )
}


function make_test() {
    var bid = parseInt($('#box_num_selected option:selected').val());
    var cid = parseInt($('#channel_num_selected option:selected').val());
    var sid = parseInt($('#scheme_num_selected option:selected').val());
    var osid = parseInt($('#scheme_num_selected option:selected').val());
    var data = {box: bid, channel: cid, plan: sid, oplan: osid};
    $.ajax({
            url: "/control/make_test/",
            type: "post",
            data: JSON.stringify(data),
            dataType: 'json',
            async: false, //同步执行
            success: function (data) {

            }
        }
    )
}

function start_oven() {
    var bid = parseInt($('#box_num_selected option:selected').val());
    var cid = parseInt($('#channel_num_selected option:selected').val());
    var oid = parseInt($('#oven_num_selected option:selected').val());
    var osid = parseInt($('#oven_scheme_num_selected option:selected').val());
    var data = {box: bid, channel: cid, oven: oid, oplan: osid};
    $.ajax({
            url: "/control/start_oven/",
            type: "post",
            data: JSON.stringify(data),
            dataType: 'json',
            async: false, //同步执行
            success: function (data) {

            }
        }
    )
}


function show_gas_table() {
    $("#gas-table-body").empty();
    var box_num = $('#box_num_selected option:selected').val();//选中的值
    var channel_num = $('#channel_num_selected option:selected').val();//选中的值
    var old_scheme_num;
    if (box_num != undefined && channel_num != undefined)
        $.ajax({
            url: "/control/get_gas_info/" + box_num + '/' + channel_num + '/',
            type: "get",
            dataType: 'json',
            async: false, //同步执行
            success: function (data) {
                var gastypes = Object.keys(data);
                var tb = document.getElementById("gas-table-body");
                create_old_table_body(tb, gastypes.length, 3);
                for (var i = 0; i < gastypes.length; i++) {
                    var td = get_table_cell(tb, i + 1, 1);
                    td.innerText = gastypes[i];
                    td = get_table_cell(tb, i + 1, 2);
                    td.innerText = data[gastypes[i]];
                    td = get_table_cell(tb, i + 1, 3);
                    var text = document.createElement("input");
                    text.setAttribute("type", "text");
                    text.setAttribute("style", "width:50px");
                    text.setAttribute("id", gastypes[i] + "_val");
                    td.appendChild(text);
                }
            }
        });
}

function set_gas() {
    var box_num = $('#box_num_selected option:selected').val();//选中的值
    var channel_num = $('#channel_num_selected option:selected').val();//选中的值
    var gas_data = {H2: 0, N2: 0, CO2: 0, H2O: 0, Air: 0, CH4: 0}
    gas_data.H2 = Number.parseFloat($('#H2_val').val());
    gas_data.N2 = Number.parseFloat($('#N2_val').val());
    gas_data.H2O = Number.parseFloat($('#H2O_val').val());
    gas_data.CH4 = Number.parseFloat($('#CH4_val').val());
    gas_data.CO2 = Number.parseFloat($('#CO2_val').val());
    gas_data.Air = Number.parseFloat($('#Air_val').val());
    console.log(gas_data)
    $.ajax({
        url: "/control/set_gas/" + box_num + '/' + channel_num + '/',
        type: "post",
        data: JSON.stringify(gas_data),
        dataType: 'json',
        async: false, //同步执行
        success: function (data) {
            show_gas_table();
        }
    })
}


function stop_oven() {
    var bid = parseInt($('#box_num_selected option:selected').val());
    var cid = parseInt($('#channel_num_selected option:selected').val());
    var oid = parseInt($('#oven_num_selected option:selected').val());
    var osid = parseInt($('#oven_scheme_num_selected option:selected').val());
    var data = {box: bid, channel: cid, oven: oid, oplan: osid};
    $.ajax({
            url: "/control/stop_oven/",
            type: "post",
            data: JSON.stringify(data),
            dataType: 'json',
            async: false, //同步执行
            success: function (data) {

            }
        }
    )
}

function pause_oven() {
    var bid = parseInt($('#box_num_selected option:selected').val());
    var cid = parseInt($('#channel_num_selected option:selected').val());
    var oid = parseInt($('#oven_num_selected option:selected').val());
    var osid = parseInt($('#oven_scheme_num_selected option:selected').val());
    var data = {box: bid, channel: cid, oven: oid, oplan: osid};
    $.ajax({
            url: "/control/pause_oven/",
            type: "post",
            data: JSON.stringify(data),
            dataType: 'json',
            async: false, //同步执行
            success: function (data) {

            }
        }
    )
}