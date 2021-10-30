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
            let firstAdminsPerRegionData = adminsPerRegion.first;
            let secondAdminsPerRegionData = adminsPerRegion.second;
            let populationData = adminsPerRegion.population;
            let adminsPerRegionCategories = adminsPerRegion.categories;
            let popDict = adminsPerRegion.pop_dict;
            $('#vax-region-loading-spinner').hide();
            $('#chart-admins-per-region').highcharts({
                chart: {
                    type: 'bar',
                    zoomType: 'y'
                },
                title: {
                    text: adminsPerRegion.title
                },
                plotOptions: {
                    bar: {
                        grouping: false,
                        pointWidth: 14
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
                    type: 'logarithmic',
                    title: {
                        enabled: false
                    },
                    max: populationData.data[0]
                },
                series: [
                    {
                        name: populationData.name,
                        data: populationData.data
                    },
                    {
                        name: firstAdminsPerRegionData.name,
                        data: firstAdminsPerRegionData.data,
                        dataLabels: {
                            enabled: true,
                            color: 'white',
                            formatter: function () {
                                let pcnt = (this.y / popDict[this.x]) * 100;
                                return Highcharts.numberFormat(pcnt, '0') + '%';
                            }
                        }
                    },
                    {
                        name: secondAdminsPerRegionData.name,
                        data: secondAdminsPerRegionData.data,
                        dataLabels: {
                            enabled: true,
                            color: 'white',
                            formatter: function () {
                                let pcnt = (this.y / popDict[this.x]) * 100;
                                return Highcharts.numberFormat(pcnt, '0') + '%';
                            }
                        }
                    }
                ],
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
        let firstAdminsPerAgeData = adminsPerAge.first;
        let secondAdminsPerAgeData = adminsPerAge.second;
        let populationData = adminsPerAge.population;
        let adminsPerAgeCategories = adminsPerAge.categories;
        let ageDict = adminsPerAge.age_dict;
        $('#vax-age-loading-spinner').hide();
        $('#chart-admins-per-age').highcharts({
            chart: {
                type: 'bar'
            },
            title: {
                text: adminsPerAge.title + ' | ' + area
            },
            plotOptions: {
                bar: {
                    grouping: false,
                    pointWidth: 25
                }
            },
            xAxis: {
                lineColor: '#999',
                lineWidth: 1,
                tickColor: '#666',
                tickLength: 3,
                categories: adminsPerAgeCategories,
            },
            yAxis: {
                visible: false,
                title: {
                    text: adminsPerAge.yAxisTitle
                },
            },
            series: [
                {
                    name: populationData.name,
                    data: populationData.data
                },
                {
                    name: firstAdminsPerAgeData.name,
                    data: firstAdminsPerAgeData.data
                },
                {
                    name: secondAdminsPerAgeData.name,
                    data: secondAdminsPerAgeData.data,
                    dataLabels: {
                        enabled: true,
                        color: 'white',
                        formatter: function () {
                            let pcnt = (this.y / ageDict[this.x]) * 100;
                            return Highcharts.numberFormat(pcnt, '0') + '%';
                        }
                    }
                }
            ],
            subtitle: subtitle,
            credits: credits
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
                    dataLabels: {
                        enabled: true,
                        distance: -50,
                        format: '{point.name}: <b>{point.percentage:.1f}%</b>',
                        style: {
                            fontWeight: 'bold',
                            color: 'white'
                        }
                    },
                    startAngle: -90,
                    endAngle: 90,
                    center: ['50%', '75%'],
                    size: '110%'
                }
            },
            series: [{
                name: adminsPerProvider.name,
                innerSize: '50%',
                data: adminsPerProvider.data
            }],
            subtitle: subtitle,
            credits: credits
        })
    }
});
