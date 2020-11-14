# COVID-19 Italy Monitor | [\#StayAtHome](https://twitter.com/hashtag/StayAtHome)

Versione Italiana [qui](https://github.com/fabriziomiano/covidashit/blob/master/README_IT.md)

A simple dashboard to monitor the COVID-19 outbreak in Italy, using the dataset 
provided by the [Civil Protection (CP)](https://github.com/pcm-dpc) 

## Preview

Mobile          |  Desktop
:-------------------------:|:-------------------------:
![alt_text](https://raw.githubusercontent.com/fabriziomiano/covidashit/master/previews/mobile.png) |  ![alt_text](https://raw.githubusercontent.com/fabriziomiano/covidashit/master/previews/preview.png)

##### The app is deployed on Heroku &#8594; [here](https://covidashit.herokuapp.com/)

##### The data is taken from the CP repo &#8594; [here](https://github.com/pcm-dpc/COVID-19/blob/master/dati-json/dpc-covid19-ita-andamento-nazionale.json)


## For developers

The WebApp uses a Flask server and gunicorn in front of it, and it only requires Python3.6+.
Furthermore, it employs Flask-babel for the italian translation. 
The script `make_pot.sh` creates the files needed by babel for the translations.
A `Batch` version of the script is provided for Windows users. 
The website's language is decided upon the client request. 

The front-end is under `covidashit/templates` and it uses JS to create the chart object, 
which is built using [HighCharts](https://www.highcharts.com/).

For the app to be operational, a mongoDB must be populated:
 - The following environmental variables must be set:
    * `MONGO_URI`
    * `NATIONAL_DATA_COLLECTION`
    * `NATIONAL_TRENDS_COLLECTION`
    * `NATIONAL_SERIES_COLLECTION`
    * `REGIONAL_DATA_COLLECTION`
    * `REGIONAL_TRENDS_COLLECTION`
    * `REGIONAL_SERIES_COLLECTION`
    * `REGIONAL_BREAKDOWN_COLLECTION`
    * `PROVINCIAL_DATA_COLLECTION`
    * `PROVINCIAL_TRENDS_COLLECTION`
    * `PROVINCIAL_SERIES_COLLECTION`
    * `PROVINCIAL_BREAKDOWN_COLLECTION`
 - The API `/api/update/<collection_type>` can be called via POST requests to drop and recreate the
 `national`, `regional` and `provincial` collections, e.g.
 ```POST /api/update/national```
 
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
Flask will be listening at [http://127.0.0.1:5000](http://127.0.0.1:5000)

##### Production
The provided Dockerfile is ready to be used to deploy the app on Heroku. 
To test the production environment locally, uncomment L17, add the 
above-mentioned env variables, and run:
```
$ docker build --tag covidashit:latest . 
$ docker run --name covidashit -d -p 80:5000 covidashit
```

The docker container will be listening at [http://127.0.0.1](http://127.0.0.1)

##### Additional note

The app can be deployed on Heroku either as a docker container or simply using the Procfile



## Donation

If you liked this project or if I saved you some time, feel free to buy me a beer. Cheers!

[![paypal](https://www.paypalobjects.com/en_US/IT/i/btn/btn_donateCC_LG.gif)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=PMW6C23XTQDWG)
