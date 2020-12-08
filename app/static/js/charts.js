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
let chartDailyTrend = Object.assign(
    chartCommon,
    {series: seriesDaily}
    );
for (let i = 0; i < seriesDaily.length ; i++) {
    if (seriesDaily[i].id === "tamponi_g") {
        seriesDaily[i].visible = false
    }
}
Highcharts.chart('chart-trend-daily', chartDailyTrend);

// current chart
if (seriesCurrent !== null) {
    let chartCurrentTrend = Object.assign(
        chartCommon,
        {series: seriesCurrent}
        );
    Highcharts.chart('chart-trend-current', chartCurrentTrend);

}

// cum chart
let chartCumTrend = Object.assign(
    chartCommon,
    {yAxis: {type: 'logarithmic'}, series: seriesCum}
    );
Highcharts.chart('chart-trend-cum', chartCumTrend);
