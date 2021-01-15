// Administrations per region
if (!REGIONS.includes(area)) {
    let adminsPerRegion = {
        chart: {
            type: 'column'
        },
        title: {
            text: adminsPerRegionTitle
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
            categories: adminsPerRegionCategories,
        },
        yAxis: {
            title: {
                text: adminsPerRegionyAxisTitle,

            },

        },
        legend: {
            enabled: false
        },
        series: adminsPerRegionData,
        subtitle: subtitle,
        credits: credits
    };
    Highcharts.chart('chart-admins-per-region', adminsPerRegion);
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
            text: adminsPerAgeyAxisTitle,

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
        pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
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
                format: '<b>{point.name}</b>: {point.percentage:.1f} %'
            }
        }
    },
    series: [{
        name: adminsPerCategorySeriesName,
        data: adminsPerCategoryData
    }],
    subtitle: subtitle,
    credits: {
        enabled: false
    }
}
Highcharts.chart('chart-pie-categories', adminsPerCategory);