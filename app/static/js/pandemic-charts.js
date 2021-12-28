Highcharts.theme = {
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
        itemHoverStyle: {
            color: 'gray'
        }
    },
    plotOptions: {
        series: {
            marker: {
                enabled: false
            }
        }
    }
};
// Apply the theme
Highcharts.setOptions(Highcharts.theme);

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


// daily chart
let links = {
    "tamponi_g": "tamponi_g_ma",
    "tamponi_g_ma": "tamponi_g",
    "nuovi_positivi": "nuovi_positivi_ma",
    "nuovi_positivi_ma": "nuovi_positivi",
    "totale_ospedalizzati_g": "totale_ospedalizzati_g_ma",
    "totale_ospedalizzati_g_ma": "totale_ospedalizzati_g",
    "deceduti_g": "deceduti_g_ma",
    "deceduti_g_ma": "deceduti_g",
    "ingressi_terapia_intensiva": "ingressi_terapia_intensiva_ma",
    "ingressi_terapia_intensiva_ma": "ingressi_terapia_intensiva"
}
let colors = ['#2f7ed8', '#0d233a', '#8bbc21', '#910000', '#1aadce']
let colorMap = {
    "tamponi_g": colors[0],
    "tamponi_g_ma": colors[0],
    "nuovi_positivi": colors[1],
    "nuovi_positivi_ma": colors[1],
    "totale_ospedalizzati_g": colors[2],
    "totale_ospedalizzati_g_ma": colors[2],
    "deceduti_g": colors[3],
    "deceduti_g_ma": colors[3],
    "ingressi_terapia_intensiva": colors[4],
    "ingressi_terapia_intensiva_ma": colors[4]
}
seriesDaily.forEach(function (entry, i) {
    entry.showInLegend = entry.id.endsWith("_ma");
    entry.visible = (entry.id.endsWith("_ma") || entry.id.endsWith("_ma")) && !entry.id.includes("tamponi")
    entry.linkedTo = links[entry.id]
    entry.color = colorMap[entry.id]
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
