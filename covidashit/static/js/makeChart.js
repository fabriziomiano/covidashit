$(document).ready(function () {
    $("#chart-trend").highcharts({
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
    });

    if (!window.location.href.includes("provinces")) {
        $("#chart-iacopo").highcharts({
            chart: {
                type: 'scatter',
                zoomType: 'x'
            },
            title: title,
            subtitle: subtitle,
            xAxis: scatterXAxis,
            yAxis: scatterYAxis,
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
                    states: {
                        hover: {
                            marker: {
                                enabled: false
                            }
                        }
                    },
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
            series: [scatterData],
            credits: credits,
        });
    }
});
