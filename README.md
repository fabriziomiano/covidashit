# COVID-19 Dash-IT

A simple dashboard with a chart of the current italian trend
based on the national data provided by the "Protezione Civile". 

##### The app is deployed on Heroku &#8594; [here](https://covidashit.herokuapp.com/)

##### Link to data &#8594; [here](https://github.com/pcm-dpc/COVID-19/blob/master/dati-json/dpc-covid19-ita-andamento-nazionale.json)

## For developers

The WebApp uses a Flask server and gunicorn in front of it,
 and it only requires Python3.6+
There's only one function in the back-end, `get_data()`, which retrieves 
the data from the above-mentioned link and it serves to the front-end chart.

The front-end is under `covidashit/templates` and it uses a simple JS to create
the chart object, which is built using [HighCharts](https://www.highcharts.com/)

#### Setup a local version

* create a virtual environment [(follow this)](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)
* install the requirements in `requirements.txt`

##### Dev (on 5000)
```
$ export FLASK_ENV=development
$ export FLASK_DEBUG=1
$ python -m flask run
```

##### Prod (on 8000)

```
$ gunicorn covidashit:app
```
