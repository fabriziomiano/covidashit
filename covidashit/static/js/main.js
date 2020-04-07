let url = "https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-json/dpc-covid19-ita-andamento-nazionale.json";

// load chart
$(document).ready(function () {
    $(chart_id).highcharts({
        chart: chart,
        title: title,
        xAxis: xAxis,
        yAxis: yAxis,
        series: series,
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
        subtitle: {
            text: 'Source: <a href="' + url + '">Civil Protection dataset</a>',
            align: "left"
        },
        credits: {
            href: "https://fabriziomiano.github.io",
            text: "by Fabrizio Miano",
            position: {
                align: "center"
            }
        },
        plotOptions: {
            series: {
                visible: false
            }
        }
    });
});

// load tooltips
$(function () {
    $('[data-toggle="tooltip"]').tooltip()
});

//  TODO: Find a way to resize the chart to full width when the sidebar is toggled
// $(function () {
//     $("#sidebarToggle").bind('click', function () {
//         $(Highcharts.charts).each(function (i, chart) {
//             var height = chart.renderTo.clientHeight;
//             var width = chart.renderTo.clientWidth;
//             chart.setSize(width, height);
//         });
//     });
// });