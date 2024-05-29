let spinnerHTML = '<div class="spinner-grow text-primary" role="status"><span class="sr-only">Loading...</span></div>';
let baseUrl = '/api/vax_charts/';
if (!REGIONS.includes(area)) {

    // Administrations per region
    $.ajax(baseUrl + 'region', {
        dataType: 'json',
        cache: false,
        beforeSend: function () {
            $('#chart-admins-per-region').html(spinnerHTML);
        },
        success: function (adminsPerRegion) {
            let firstAdminsPerRegionData = adminsPerRegion.first;
            let secondAdminsPerRegionData = adminsPerRegion.second;
            let boosterAdminsPerRegionData = adminsPerRegion.booster;
            let populationData = adminsPerRegion.population;
            let adminsPerRegionCategories = adminsPerRegion.categories;
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
                        grouping: false
                    }
                },
                xAxis: {
                    categories: adminsPerRegionCategories,
                },
                yAxis: {
                    visible: false
                },
                series: [
                    {
                        name: populationData.name,
                        data: populationData.data
                    },
                    {
                        name: firstAdminsPerRegionData.name,
                        data: firstAdminsPerRegionData.data
                    },
                    {
                        name: secondAdminsPerRegionData.name,
                        data: secondAdminsPerRegionData.data
                    },
                    {
                        name: boosterAdminsPerRegionData.name,
                        data: boosterAdminsPerRegionData.data
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
            $('#chart-admins-timeseries').html(spinnerHTML);
        },
        success: function (adminsTimeseriesData) {
            // Show only Sicilia by default
            adminsTimeseriesData.data = adminsTimeseriesData.data.map(function (o) {
                o.visible = o.name === "Sicilia";
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
        $('#chart-admins-per-age').html(spinnerHTML);
    },
    data: {
        area: area
    },
    success: function (adminsPerAge) {
        let firstAdminsPerAgeData = adminsPerAge.first;
        let secondAdminsPerAgeData = adminsPerAge.second;
        let boosterAdminsPerAgeData = adminsPerAge.booster;
        let populationData = adminsPerAge.population;
        let adminsPerAgeCategories = adminsPerAge.categories;
        let ageDict = adminsPerAge.age_dict;
        $('#chart-admins-per-age').highcharts({
            chart: {
                type: 'bar'
            },
            title: {
                text: adminsPerAge.title + ' | ' + area
            },
            plotOptions: {
                bar: {
                    grouping: false
                }
            },
            xAxis: {
                categories: adminsPerAgeCategories,
            },
            yAxis: {
                visible: false
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
                    data: secondAdminsPerAgeData.data
                },
                {
                    name: boosterAdminsPerAgeData.name,
                    data: boosterAdminsPerAgeData.data
                },
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
        $('#chart-pie-providers').html(spinnerHTML);
    },
    data: {
        area: area
    },
    success: function (adminsPerProvider) {
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
                pointFormat: '{point.y} (<b>{point.percentage:.1f}%</b>)'
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
                    },
                    startAngle: -90,
                    endAngle: 90,
                    center: ['50%', '70%'],
                    // size: '150%'
                }
            },
            series: [{
                name: adminsPerProvider.name,
                innerSize: '20%',
                data: adminsPerProvider.data
            }],
            subtitle: subtitle,
            credits: credits
        })
    }
});
