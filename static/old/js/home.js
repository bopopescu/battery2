$(function () {
    $('#ydl_data').dynamo({
        speed: 100,
        delay: 2500,
        lines: ['25.7KW', '25.5KW', '25.4KW','25.5KW','25.7KW', '25.8KW'],
    });
    $('#ysl_data').dynamo({
        speed: 100,
        delay: 2500,
        lines: ['5.7L/S', '7.5L/S', '9.4L/S','5.5L/S','9.7L/S', '8.8L/S'],
    });
    $('#yql_data').dynamo({
        speed: 100,
        delay: 2500,
        lines: ['3.7Nm³/s', '3.5Nm³/s', '3.4Nm³/s','3.5Nm³/s','3.7Nm³/s', '3.8Nm³/s'],
    });
});

$(function () {

})