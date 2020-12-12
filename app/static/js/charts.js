Highcharts.theme = {
    colors: [
        '#0520c6', '#08a4e8', '#3b6d00', '#ff0000', '#24CBE5'
    ],
    subtitle: {
        style: {
            color: '#666666',
            font: 'bold 12px "Trebuchet MS", Verdana, sans-serif'
        }
    },
    legend: {
        itemStyle: {
            font: '9pt Trebuchet MS, Verdana, sans-serif',
            color: 'black'
        },
        itemHoverStyle:{
            color: 'gray'
        }
    }
};
// Apply the theme
Highcharts.setOptions(Highcharts.theme);

let chartCommon = {
    chart: {
        type: 'areaspline',
        zoomType: 'xy'
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


// daily chart
seriesDaily.forEach(function (entry, i) {
    entry.visible = (entry.id.endsWith("_ma") && !entry.id.includes("tamponi"));
    if (!entry.id.endsWith("_ma")) {
        entry.type = 'spline';
        entry.dashStyle = 'Dot';
    }
    entry.showInLegend = entry.id.endsWith("_ma");
    entry.type = 'spline';
})

let chartDailyTrend = Object.assign({}, chartCommon);
chartDailyTrend.series = seriesDaily;
chartDailyTrend.exporting.buttons.originalData = {
    text: 'Original',
    onclick: function () {
        this.series.forEach(function (entry) {
            let seriesId = entry.userOptions.id;
            if (!seriesId.endsWith("_ma") && !seriesId.includes("tamponi")) {
                (entry.visible) ? entry.hide() : entry.show()
            }
        })
    }
}
chartDailyTrend.exporting.buttons.weeklyMovAvg = {
    text: '7d MA',
    onclick: function () {
        this.series.forEach(function (entry) {
            let seriesId = entry.userOptions.id;
            if (seriesId.endsWith("_ma") && !seriesId.includes("tamponi")) {
                (!entry.visible) ? entry.show() : entry.hide()
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
    delete chartCurrentTrend.exporting.buttons.originalData;
    Highcharts.chart('chart-trend-current', chartCurrentTrend);
}


// cum chart
let chartCumTrend = Object.assign({}, chartCommon);
chartCumTrend.series = seriesCum
chartCumTrend.yAxis = {type: 'logarithmic'}
delete chartCumTrend.exporting.buttons.weeklyMovAvg;
delete chartCumTrend.exporting.buttons.originalData;
Highcharts.chart('chart-trend-cum', chartCumTrend);
