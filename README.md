# COVID-19 Italy Monitor

Versione Italiana [qui](https://github.com/fabriziomiano/covidashit/blob/master/README_IT.md)

A simple dashboard to monitor the COVID-19 outbreak in Italy, using the dataset 
provided by the [Civil Protection (CP)](https://github.com/pcm-dpc) 

## Preview

![alt_text](https://raw.githubusercontent.com/fabriziomiano/covidashit/master/preview.png)

##### The app is deployed on Heroku &#8594; [here](https://covidashit.herokuapp.com/)

##### The data is taken from the CP repo &#8594; [here](https://github.com/pcm-dpc/COVID-19/blob/master/dati-json/dpc-covid19-ita-andamento-nazionale.json)

Stay safe everbody!

## For developers

The WebApp uses a Flask server and gunicorn in front of it, and it only requires Python3.6+.
Furthermore, it employs Flask-babel for the italian translation. The script `make_pot.sh` creates the needed files.
A `Batch` version of the script is provided for Windows users. 
The website's language is decided upon the client request. 
The back-end retrieves the data and it serves it to the front-end chart and cards.
I'm not using any db as, luckily enough, there isn't too much data to store, and hopfully there will not be, ever.

3 APIs are provided:
* `GET /api/national` response `{"national": [...]}`
* `GET /api/regional` response `{"regional": [...]}`
* `GET /api/provincial` response `{"provincial": [...]}`

where the array is the data provided by the original source.

The front-end is under `covidashit/templates` and it uses a simple JS to create
the chart object, which is built using [HighCharts](https://www.highcharts.com/)

#### Setup a local version

* create and activate a virtual environment [(follow this)](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)
* install the requirements in `requirements.txt`

##### Development
Clone the repo, `cd` into it, and
```
$ export FLASK_ENV=development
$ export FLASK_DEBUG=1
$ python -m flask run
```

##### Production
The `Profile` can be used to deploy the app on Heroku.
To test the production environment locally, simply run
```
$ gunicorn covidashit:app
```

## Donation

If you liked this project or if I saved you some time, feel free to buy me a beer. Cheers!

[![paypal](https://www.paypalobjects.com/en_US/IT/i/btn/btn_donateCC_LG.gif)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=PMW6C23XTQDWG)
