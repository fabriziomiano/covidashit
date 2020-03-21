from flask import render_template

from covidashit import app, get_data


@app.route('/')
@app.route('/index')
def index(chart_id='chart_ID', chart_type='column'):
    dates, series1, series2, series3, series4 = get_data()
    chart = {"renderTo": chart_id, "type": chart_type}
    series = [series1, series2, series3, series4]
    title = {"text": 'COVID-19 Italian trend'}
    x_axis = {"categories": dates}
    y_axis = {"title": {"text": '# of people'}, "type": "logarithmic"}
    return render_template(
        'index.html',
        chartID=chart_id,
        chart=chart,
        series=series,
        title=title,
        xAxis=x_axis,
        yAxis=y_axis)
