let chartTrendOptions = {
    chart: {
        type: 'line',
        zoomType: 'x'
    },
    title: title,
    xAxis: xAxis,
    yAxis: yAxis,
    series: [],
    tooltip: {
        crosshairs: {
            width: 1,
            color: 'gray',
            dashStyle: 'ShortDashDot'
        },
        shared: true,
        split: false,
        enabled: true
    },
    exporting: {
        buttons: {
            linScale: {
                text: 'Lin',
                onclick: function () {
                    this.yAxis[0].update({
                        type: 'linear'
                    });
                }
            },
            logScale: {
                text: 'Log',
                onclick: function () {
                    this.yAxis[0].update({
                        type: 'logarithmic'
                    });
                }
            },
        }
    },
    subtitle: subtitle,
    credits: credits,
    plotOptions: {
        series: {
            visible: true
        }
    }
}


let chartTrendDailyOptions = Object.assign({}, chartTrendOptions);
chartTrendDailyOptions.series = seriesDaily;
let chartTrendCurrentOptions = Object.assign({}, chartTrendOptions);
chartTrendCurrentOptions.series = seriesCurrent;
let chartTrendCumOptions = Object.assign({}, chartTrendOptions);
chartTrendCumOptions.series = seriesCum;

let chartDailyTrend = Highcharts.chart('chart-trend-daily', chartTrendDailyOptions);
let chartCurrentTrend = Highcharts.chart('chart-trend-current', chartTrendCurrentOptions);
let chartCumTrend = Highcharts.chart('chart-trend-cum', chartTrendCumOptions);


function dataTypeSelector(chart, value) {
    if (value !== "default") {
        for (let i = 0; i < chart.series.length; i++) {
            if (chart.series[i].name === value) {
                chart.series[i].show()
            } else {
                chart.series[i].hide()
            }
        }
    }
}

function playBCR(bcr_id) {
    $('#loadBCRButtonLoader' + bcr_id).removeAttr('hidden')
    $('#loadBCRButton' + bcr_id).attr('hidden', true)
    $.ajax({
        url: '/api/bcr/' + bcr_id,
        method: 'get',
        success: function (response) {
            console.log(response)
            if (response["status"] === "ok") {
                $("#bcrCard" + bcr_id).append(response["html_str"])
                $("#bcrts" + bcr_id).append(response["ts"]).removeAttr('hidden')
            }
            else {
                $("#bcrCard" + bcr_id).append(response["error"])
                $("#bcrts" + bcr_id).append(response["error"]).removeAttr('hidden')
            }
            $("#loadBCRButtonLoader" + bcr_id).attr("hidden", true)
        }
    })
}
