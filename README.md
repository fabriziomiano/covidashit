# Italian COVID Dashboard

A Flask dashboard displaying the Italian data,
 as per the dataset provided by the [Civil Protection (CP)](https://github.com/pcm-dpc),
 of the Italian COVID-19 outbreak.

## Preview

![alt_text](https://raw.githubusercontent.com/fabriziomiano/covidashit/master/preview.png)

##### The app is deployed on Heroku &#8594; [here](https://covidashit.herokuapp.com/)

##### The data is taken from the CP repo &#8594; [here](https://github.com/pcm-dpc/COVID-19/blob/master/dati-json/dpc-covid19-ita-andamento-nazionale.json)

Stay safe everbody!

## For developers

The WebApp uses a Flask server and gunicorn in front of it,
 and it only requires Python3.6+
There's only one function in the back-end, `get_data()`, which retrieves
the data from the above-mentioned link and serves it to the front-end chart.
I'm not using any db as, luckily enough, there isn't too much data to store, and hopfully there will not be, ever.

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

## Donation

If you liked this project or if I saved you some time, feel free to buy me a beer. Cheers!


[![paypal](https://www.paypalobjects.com/en_US/IT/i/btn/btn_donateCC_LG.gif)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=PMW6C23XTQDWG)
