let chartCommon = {
    chart: {
        type: 'areaspline',
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
    credits: credits
}


// daily chart
seriesDaily.forEach(function (entry) {
    entry.visible = !(entry.id.endsWith("_ma") || entry.id.includes("tamponi"));
})

let chartDailyTrend = Object.assign({}, chartCommon);
chartDailyTrend.series = seriesDaily;
chartDailyTrend.exporting.buttons.weeklyMovAvg = {
    text: '7d MAvg',
    onclick: function () {
        this.series.forEach(function (entry) {
            let seriesId = entry.userOptions.id
            if (seriesId.endsWith("_ma") && !seriesId.includes("tamponi")) {
                if (!entry.visible) {
                    entry.show()
                } else {
                    entry.hide()
                }
            }
        })
    }
}
Highcharts.chart('chart-trend-daily', chartDailyTrend);


// current chart
if (seriesCurrent !== null) {
    let chartCurrentTrend = Object.assign({}, chartCommon);
    chartCurrentTrend.series = seriesCurrent;
    delete chartCurrentTrend.exporting.buttons.weeklyMovAvg;
    Highcharts.chart('chart-trend-current', chartCurrentTrend);
}


// cum chart
let chartCumTrend = Object.assign({}, chartCommon);
chartCumTrend.series = seriesCum
chartCumTrend.yAxis = {type: 'logarithmic'}
delete chartCumTrend.exporting.buttons.weeklyMovAvg;
Highcharts.chart('chart-trend-cum', chartCumTrend);
