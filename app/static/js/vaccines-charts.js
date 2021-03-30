// Administrations per region: defined only for the national vax view
let adminsPerRegion = {}
if (!REGIONS.includes(area)) {
    // Administrations per region
    adminsPerRegion = {
        chart: {
            type: 'bar'
        },
        title: {
            text: adminsPerRegionTitle
        },
        plotOptions: {
            series: {
                dataLabels: {
                    enabled: true,
                    formatter: function () {
                        let pcnt = (this.y / totAdmins) * 100;
                        return Highcharts.numberFormat(pcnt, '1') + '%';
                    }
                }
            }
        },
        xAxis: {
            lineColor: '#999',
            lineWidth: 1,
            tickColor: '#666',
            tickLength: 3,
            categories: adminsPerRegionCategories,
        },
        yAxis: {
            title: {
                enabled: false
            },
            labels: {
                enabled: false
            }
        },
        series: [{
            name: adminsPerRegionData.name,
            data: adminsPerRegionData.data
        }, {
            name: expAdminsPerRegionData.name,
            data: expAdminsPerRegionData.data,
            visible: false
        }],
        subtitle: subtitle,
        credits: credits
    };
    Highcharts.chart('chart-admins-per-region', adminsPerRegion);


    // Vax time series for a given area
    adminsTimeseriesData = adminsTimeseriesData.map(function (o, i) {
        o.visible = i <= 2;
        return o;
    })
    let adminsTimeSeries = {
        chart: {
            zoomType: 'x',
            type: 'spline'
        },
        title: {
            text: adminsTimeseriesTitle
        },
        xAxis: {
            type: 'datetime',
            categories: adminsTimeseriesDates
        },
        yAxis: {
            title: {
                text: adminsTimeseriesyAxisTitle
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
        legend: {
            enabled: false
        },

        plotOptions: {
            series: {
                label: {
                    connectorAllowed: false
                },
                marker: {
                    enabled: false
                }
            },

        },
        series: adminsTimeseriesData,
        credits: credits,
        subtitle: subtitle
    };
    Highcharts.chart('chart-admins-timeseries', adminsTimeSeries);

    let series = $("#chart-admins-timeseries").highcharts().series;
    let seriesIMap = {}
    for (let i = 0; i < series.length; i++) {
        seriesIMap[series[i].name] = i;
    }
    $(function () {
        $('#timeseries-select').change(function (e) {
            let selRegions = $(e.target).val();
            REGIONS.forEach(function (region) {
                selRegions.includes(region) ? series[seriesIMap[region]].show() : series[seriesIMap[region]].hide();
            });
        })
    });
}

// Administrations per Age
let adminsPerAge = {
    chart: {
        type: 'column'
    },
    title: {
        text: adminsPerAgeTitle
    },
    plotOptions: {
        series: {
            shadow: false,
            borderWidth: 0,
            dataLabels: {
                enabled: true,
                formatter: function () {
                    let pcnt = (this.y / totAdmins) * 100;
                    return Highcharts.numberFormat(pcnt, '1') + '%';
                }
            }
        }
    },
    xAxis: {
        lineColor: '#999',
        lineWidth: 1,
        tickColor: '#666',
        tickLength: 3,
        categories: ageCategories,
    },
    yAxis: {
        title: {
            text: adminsPerAgeyAxisTitle
        },
    },
    legend: {
        enabled: false
    },
    series: adminsPerAgeData,
    subtitle: subtitle,
    credits: credits
};
Highcharts.chart('chart-admins-per-age', adminsPerAge);

// Administrations per category
let adminsPerCategory = {
    chart: {
        plotBackgroundColor: null,
        plotBorderWidth: null,
        plotShadow: false,
        type: 'pie'
    },
    title: {
        text: adminsPerCategoryTitle
    },
    tooltip: {
        pointFormat: '{series.name}: <b>{point.y}</b>'
    },
    accessibility: {
        point: {
            valueSuffix: '%'
        }
    },
    plotOptions: {
        pie: {
            allowPointSelect: true,
            cursor: 'pointer',
            dataLabels: {
                enabled: true,
                format: '<b>{point.name}</b>: {point.percentage:.1f} %',
                // distance: -50
            }
        }
    },
    series: [{
        name: adminsPerCategorySeriesName,
        data: adminsPerCategoryData
    }],
    subtitle: subtitle,
    credits: credits
}
Highcharts.chart('chart-pie-categories', adminsPerCategory);

// Administrations per provider
let adminsPerProvider = {
    chart: {
        plotBackgroundColor: null,
        plotBorderWidth: null,
        plotShadow: false,
        type: 'pie'
    },
    title: {
        text: adminsPerProviderTitle
    },
    tooltip: {
        pointFormat: '{series.name}: <b>{point.y}</b>'
    },
    accessibility: {
        point: {
            valueSuffix: '%'
        }
    },
    plotOptions: {
        pie: {
            allowPointSelect: true,
            cursor: 'pointer',
            dataLabels: {
                enabled: true,
                format: '{point.name}: <b>{point.percentage:.1f}%</b>',
                distance: -50
            }
        }
    },
    series: [{
        name: adminsPerProviderSeriesName,
        data: adminsPerProviderData
    }],
    subtitle: subtitle,
    credits: credits
}
Highcharts.chart('chart-pie-providers', adminsPerProvider);