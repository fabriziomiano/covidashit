let baseUrl = '/api/vax_charts/'
if (!REGIONS.includes(area)) {

    // Administrations per region
    $.ajax(baseUrl + 'region', {
        dataType: 'json',
        cache: false,
        beforeSend: function () {
            $('#vax-region-loading-spinner').show();
        },
        success: function (adminsPerRegion) {
            let adminsPerRegionData = adminsPerRegion.real;
            let expAdminsPerRegionData = adminsPerRegion.expected;
            let adminsPerRegionCategories = adminsPerRegion.categories;
            $('#vax-region-loading-spinner').hide();
            $('#chart-admins-per-region').highcharts({
                chart: {
                    type: 'bar'
                },
                title: {
                    text: adminsPerRegion.title
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
            });
        }
    });

    // Administrations trend
    $.ajax(baseUrl + 'trend', {
        dataType: 'json',
        cache: false,
        beforeSend: function () {
            $('#vax-timeseries-loading-spinner').show();
        },
        success: function (adminsTimeseriesData) {
            $('#vax-timeseries-loading-spinner').hide();
            // Vax time series for a given area
            adminsTimeseriesData.data = adminsTimeseriesData.data.map(function (o, i) {
                o.visible = i <= 2;
                return o;
            })
            $('#chart-admins-timeseries').highcharts({
                chart: {
                    zoomType: 'x',
                    type: 'spline'
                },
                title: {
                    text: adminsTimeseriesData.title
                },
                xAxis: {
                    type: 'datetime',
                    categories: adminsTimeseriesData.dates
                },
                yAxis: {
                    title: {
                        text: adminsTimeseriesData.yAxisTitle
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
                series: adminsTimeseriesData.data,
                credits: credits,
                subtitle: subtitle
            });

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
    });
}

// Administrations per age
$.ajax(baseUrl + 'age', {
    dataType: 'json',
    cache: false,
    beforeSend: function () {
        $('#vax-age-loading-spinner').show();
    },
    data: {
        area: area
    },
    success: function (adminsPerAge) {
        $('#vax-age-loading-spinner').hide();
        $('#chart-admins-per-age').highcharts({
            chart: {
                type: 'bar'
            },
            title: {
                text: adminsPerAge.title + ' | ' + area
            },
            plotOptions: {
                // series: {
                //     borderWidth: 0,
                //     dataLabels: {
                //         enabled: true,
                //         formatter: function () {
                //             let pcnt = (this.y / totAdmins) * 100;
                //             return Highcharts.numberFormat(pcnt, '1') + '%';
                //         }
                //     }
                // },
                bar: {
                    grouping: false
                }
            },
            xAxis: {
                lineColor: '#999',
                lineWidth: 1,
                tickColor: '#666',
                tickLength: 3,
                categories: adminsPerAge.categories,
            },
            yAxis: {
                visible: false,
                title: {
                    text: adminsPerAge.yAxisTitle
                },
            },
            series: adminsPerAge.data,
            subtitle: subtitle,
            credits: credits,
            caption: caption
        });
    }
});


// Administrations per provider
$.ajax(baseUrl + 'provider', {
    area: area,
    dataType: 'json',
    cache: false,
    beforeSend: function () {
        $('#vax-provider-loading-spinner').show();
    },
    data: {
        area: area
    },
    success: function (adminsPerProvider) {
        $('#vax-provider-loading-spinner').hide();
        $('#chart-pie-providers').highcharts({
            chart: {
                plotBackgroundColor: null,
                plotBorderWidth: null,
                plotShadow: false,
                type: 'pie'
            },
            title: {
                text: adminsPerProvider.title + ' | ' + area
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
                        // distance: -1
                    }
                }
            },
            series: [{
                name: adminsPerProvider.name,
                data: adminsPerProvider.data
            }],
            subtitle: subtitle,
            credits: credits
        })
    }
});
