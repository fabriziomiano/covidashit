let url = "https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-json/dpc-covid19-ita-andamento-nazionale.json";
$(document).ready(function () {
    $(chart_id).highcharts({
        chart: chart,
        title: title,
        xAxis: xAxis,
        yAxis: yAxis,
        series: series,
        subtitle: {
            text: ('Source: <a href="' + url + '">Protezione Civile</a>')
        },
        credits: {
            href: "fabriziomiano.github.io",
            text: "by Fabrizio Miano"
        }
    });
});
