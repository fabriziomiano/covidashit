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
let chartDailyTrend = Highcharts.chart('chart-trend-daily', chartTrendDailyOptions);

let chartTrendCumOptions = Object.assign({}, chartTrendOptions);
chartTrendCumOptions.series = seriesCum;
let chartCumTrend = Highcharts.chart('chart-trend-cum', chartTrendCumOptions);

if (seriesCurrent !== undefined) {
    let chartTrendCurrentOptions = Object.assign({}, chartTrendOptions);
    chartTrendCurrentOptions.series = seriesCurrent;
    let chartCurrentTrend = Highcharts.chart('chart-trend-current', chartTrendCurrentOptions);

}
