let chartCommon = {
    chart: {
        type: 'spline',
        zoomType: 'x'
    },
    legend: {
        enabled: true
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
    credits: credits
}


seriesDaily.forEach(function (entry, i) {
    entry.visible = !entry.id.includes("tamponi")
    entry.borderColor = 'black'
    entry.borderWidth = 1
})
let chartDailyTrend = Object.assign({}, chartCommon);
chartDailyTrend.series = seriesDaily;
Highcharts.chart('chart-trend-daily', chartDailyTrend);


// current chart
if (seriesCurrent !== null) {
    let chartCurrentTrend = Object.assign({}, chartCommon);
    chartCurrentTrend.series = seriesCurrent;
    Highcharts.chart('chart-trend-current', chartCurrentTrend);
}

// cum chart
let chartCumTrend = Object.assign({}, chartCommon);
chartCumTrend.series = seriesCum
chartCumTrend.yAxis = {type: 'logarithmic'}
Highcharts.chart('chart-trend-cum', chartCumTrend);