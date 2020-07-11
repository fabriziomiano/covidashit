let chartTrendOptions = {
    chart: {
        type: 'line',
        zoomType: 'x'
    },
    title: title,
    xAxis: xAxis,
    yAxis: yAxis,
    series: series,
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
            visible: false
        }
    }
}

let chartIacopoOptions = {
    chart: {
        type: 'scatter',
        zoomType: 'x'
    },
    legend: {
        enabled: false
    },
    title: title,
    subtitle: subtitle,
    xAxis: scatterXAxis,
    yAxis: scatterYAxis,
    plotOptions: {
        scatter: {
            marker: {
                radius: 3,
                states: {
                    hover: {
                        enabled: true,
                        lineColor: 'rgb(100,100,100)'
                    }
                }
            },
            states: {
                hover: {
                    marker: {
                        enabled: false
                    }
                }
            },
        }
    },
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
    series: [scatterData],
    credits: credits
}

let chartTrend = Highcharts.chart('chart-trend', chartTrendOptions);

$(document).ready(function () {
    if (!window.location.href.includes("provinces")) {
        $("#chart-iacopo").highcharts(chartIacopoOptions);
    }
});

function dataTypeSelector(value) {
    if (value !== "default") {
        for (let i = 0; i < chartTrend.series.length; i++) {
            if (chartTrend.series[i].name === value) {
                chartTrend.series[i].show()
            } else {
                chartTrend.series[i].hide()
            }
        }
    }
}

$(function () {
    $.ajax({
        url: '/api/get_bcr',
        method: 'get',
        success: function (response) {
            $("#bcrLoader").attr("hidden", true)
            $("#bcrCard").append(response["html"])
            $("#bcrts").append(response["ts"])
        }
    })
})