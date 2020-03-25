import time
from flask import render_template
from covidashit import app, get_data
PAGE_TITLE = "COVID-19 Italian trend"


@app.route('/')
@app.route('/index')
def index(chart_id='chart_ID', chart_type='column'):
    (dates, series1, series2, series3, series4, series5,
     series6, series7, series8, series9, series10, trend) = get_data()
    chart = {"renderTo": chart_id, "type": chart_type}
    series = [
        series1, series2, series3, series4, series5,
        series6, series7, series8, series9, series10
    ]
    title = {"text": 'COVID-19 Italian trend', "align": "left"}
    x_axis = {"categories": dates}
    y_axis = {"title": {"text": '# of people'}, "type": "logarithmic"}
    return render_template(
        'index.html',
        trend=trend,
        pagetitle=PAGE_TITLE,
        chartID=chart_id,
        chart=chart,
        series=series,
        title=title,
        xAxis=x_axis,
        yAxis=y_axis,
        ts=str(time.time())
    )
