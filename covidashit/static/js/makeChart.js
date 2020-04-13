let url = "https://github.com/pcm-dpc/COVID-19/tree/master/dati-json";

// load chart
$(document).ready(function () {
    $(chart_id).highcharts({
        chart: chart,
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
        subtitle: {
            text: 'Source: <a href="' + url + '">Civil Protection dataset</a>',
            align: "left"
        },
        credits: {
            href: "https://fabriziomiano.github.io",
            text: "by Fabrizio Miano | Made with Highcharts.com",
        },
        plotOptions: {
            series: {
                visible: false
            }
        }
    });

    if (!window.location.href.includes("provinces")) {
        $("#chart-iacopo").highcharts({
            chart: {
                type: 'scatter',
                zoomType: 'xy'
            },
            title: {
                text: 'New Positive VS Total positive',
                align: "left"
            },
            subtitle: {
                text: 'Source: <a href="' + url + '">Civil Protection dataset</a>',
                align: "left"
            },
            xAxis: {
                title: {
                    enabled: true,
                    text: '# Total cases'
                },
                startOnTick: true,
                endOnTick: true,
                showLastLabel: true
            },
            yAxis: {
                type: "logarithmic",
                title: {
                    text: '# New positives'
                }
            },
            plotOptions: {
                scatter: {
                    marker: {
                        radius: 7,
                        states: {
                            hover: {
                                enabled: true,
                                lineColor: 'rgb(100,100,100)'
                            }
                        }
                    },
                    // lineWidth: 2,
                    states: {
                        hover: {
                            marker: {
                                enabled: false
                            }
                        }
                    },
                    tooltip: {
                        headerFormat: '<b>{series.name}</b><br>',
                        pointFormat: '{point.x} New positive cases, {point.y} Total cases'
                    }
                }
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
            series: [{
                name: "New positive VS Total positive",
                data: data
            }],
            credits: {
                href: "https://fabriziomiano.github.io",
                text: "by Fabrizio Miano | Made with Highcharts.com",
            },
        });
    }
});
