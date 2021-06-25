# COVID-19 Italy Monitor | [\#StayAtHome](https://twitter.com/hashtag/StayAtHome)

[![Awesome](https://awesome.re/badge.svg)](https://github.com/soroushchehresa/awesome-coronavirus#applications-and-bots)
[![Open Source Love](https://badges.frapsoft.com/os/v1/open-source.svg?v=103)](https://github.com/ellerbrock/open-source-badges/)
[![Made with Pthon](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)

![alt_text](https://raw.githubusercontent.com/fabriziomiano/covidashit/main/previews/mockup.png)

Versione Italiana [qui](https://github.com/fabriziomiano/covidashit/blob/main/README_IT.md)

A simple dashboard to display and monitor the official data of the COVID-19 outbreak in Italy released by the [Civil Protection Dept.](https://github.com/pcm-dpc/COVID-19) and updated on a daily basis.

**The app is deployed on Heroku [here](https://www.covidash.it/)**

**Pandemic data from the [official CP Dept repository](https://github.com/pcm-dpc/COVID-19/)**

**Vaccine data from the [official open-data repository](https://github.com/italia/covid19-opendata-vaccini)**


## For developers
The WebApp requires Python 3.8+ and reads the data from a mongoDB. It employs a Flask server with `gunicorn` in front of it.
Furthermore, it employs Flask-babel for the italian translation, as English is set as primary language. 
The script `make_pot.sh` creates the files needed by Babel for the translations.
A `Batch` version of the script for Windows users is provided. 
The app language is decided upon the client request (browser / OS).

The front-end lives under `covidashit/templates` and it uses JS to create the chart object, 
which is built using [HighCharts](https://www.highcharts.com/).

In order for the app to be operational, a mongoDB must be populated 
([see here](https://docs.atlas.mongodb.com/tutorial/create-new-cluster) for the creation of an Atlas mongoDB free cluster).
Additionally, mongo collections must be updated on a daily basis. The Flask contains a number of API whose purpose is to 
update the DB every time the `master` branch of the CP Dept repository is updated, via a GitHub webhook (see the GitHub workflow [here](https://github.com/fabriziomiano/COVID-19/blob/master/.github/workflows/merge-upstream.yml)).
Ultimately, the webhooks for the following APIs must be set on the CP forked repository:

 * `POST /update/<data_type>`
 * `POST /update/<data_type>/<coll_type>`

| data_type  | coll_type                   |
|------------|-----------------------------|
| national   | [series, trends]            |
| regional   | [breakdown, series, trends] |
| provincial | [breakdown, series, trends] |
| vax        | [summary]                   |

### Local deployment (DEV)
* create and activate a virtual environment [(follow this)](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)
* install the requirements in `requirements.txt`

The `.env` file contains all the env vars needed by the webapp. 
In particular, the `MONGO_URI` and the various collection names string must be set.
Before the Flask server is started, but after the virtual environment has been activated, 
the DB must be populated.
For this purpose a Flask CLI, that populates the various collections, is included.
This, with a very basic ETL procedure, will populate the various collections on 
the DB with the official data released by the Civil Protection Dept.

Clone the repo, `cd` into it, activate the virtual environment, and run the procedure
```shell
flask create-collections
```
then run the worker 
```shell
celery -A celery_worker.celery worker
```
in a new shell, the celery beat for the background scheduled tasks
```shell
celery -A celery_worker.celery beat
```
and, in a new shell, run the application server
```shell
flask run
```
Flask will be listening at [http://127.0.0.1:5000](http://127.0.0.1:5000)

### Local deployment (PROD)
First, replace the value of `APPLICATION_ENV` in `.env` with `production`
#### Procfile
to test the `Procfile` configuration, Simply run the heroku CLI 
```shell
heroku local
```

#### Docker
To test the containerization locally spawn the container with:
```shell
docker-compose up -d
```

The docker container will be listening at `http://127.0.0.1:PORT` with `PORT`
being set in the `.env` file

Stop it with 
```shell
docker-compose down
```

### Deployment on Heroku
The app can be deployed on Heroku either as a docker container or simply using the Procfile

## Plots API
The app provides an API to produce a server-side plot with `matplotlib`.
The API can return a JSON response with the base64-encoded image, or 
the bytes content to be saved as a file.

### Resource URL

`https://www.covidash.it/api/plot`

### Query parameters

| data_type  | var_name                                                                                                                                                                                                                                                                                                                                                            | area                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
|------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| national   | [nuovi_positivi, ingressi_terapia_intensiva,  deceduti_g, tamponi_g,totale_ospedalizzati_g,  nuovi_positivi_ma, deceduti_g_ma,  ingressi_terapia_intensiva_ma, tamponi_g_ma, totale_ospedalizzati_g_ma, totale_positivi, terapia_intensiva, ricoverati_con_sintomi, totale_ospedalizzati, isolamento_domiciliare, totale_casi, deceduti,  tamponi, dimessi_guariti] | N/A                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| regional   | [nuovi_positivi, ingressi_terapia_intensiva,  deceduti_g, tamponi_g,totale_ospedalizzati_g,  nuovi_positivi_ma, deceduti_g_ma,  ingressi_terapia_intensiva_ma, tamponi_g_ma, totale_ospedalizzati_g_ma, totale_positivi, terapia_intensiva, ricoverati_con_sintomi, totale_ospedalizzati, isolamento_domiciliare, totale_casi, deceduti,  tamponi, dimessi_guariti] | [Abruzzo, Basilicata, Calabria, Campania, Emilia-Romagna, Friuli Venezia Giulia, Lazio, Liguria, Lombardia, Marche, Molise, Piemonte, Puglia, Sardegna, Sicilia, Toscana, P.A. Bolzano, P.A. Trento, Umbria, Valle d'Aosta, Veneto]                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| provincial | [nuovi_positivi, nuovi_positivi_ma, totale_casi]                                                                                                                                                                                                                                                                                                                    | [Chieti, L'Aquila, Pescara, Teramo,  Matera, Potenza, Catanzaro, Cosenza, Crotone, Reggio di Calabria, Vibo Valentia,  Avellino, Benevento, Caserta,  Napoli, Salerno, Bologna, Ferrara,  Forlì-Cesena, Modena, Parma, Piacenza,  Ravenna, Reggio nell'Emilia, Rimini,  Gorizia, Pordenone, Trieste, Udine,  Frosinone, Latina, Rieti, Roma, Viterbo,  Genova, Imperia, La Spezia, Savona,  Bergamo, Brescia, Como, Cremona, Lecco,  Lodi, Mantova, Milano,  Monza e della Brianza, Pavia, Sondrio,  Varese, Ancona, Ascoli Piceno, Fermo,  Macerata, Pesaro e Urbino, Campobasso,  Isernia, Alessandria, Asti, Biella,  Cuneo, Novara, Torino, Verbano-Cusio-Ossola,  Vercelli, Bari, Barletta-Andria-Trani,  Brindisi, Lecce, Foggia, Taranto, Cagliari,  Nuoro, Sassari, Sud Sardegna, Agrigento,  Caltanissetta, Catania, Enna, Messina,  Palermo, Ragusa, Siracusa, Trapani, Arezzo,  Firenze, Grosseto, Livorno, Lucca, Massa Carrara, Pisa, Pistoia, Prato, Siena,  Perugia, Terni, Aosta, Belluno,  Padova, Rovigo, Treviso, Venezia, Verona, Vicenza] |


### Examples
#### National plot
`GET /api/plot?data_type=national&varname=<varname>`

#### Regional plot 
`GET /api/plot?data_type=regional&area=<region>&varname=<varname>`

#### Provincial plot
`GET /api/plot?data_type=provincial&area=<province>&varname=[nuovi_positivi,nuovi_positivi_ma,totale_casi]>`


#### To get the base64-encoded image in a JSON response
#### JSON

#### Request
```
curl --request GET \ 
     --url 'https://www.covidash.it/api/plot?data_type=national&varname=totale_casi'
```

#### Response
```json
{
    "errors":[],
    "img":"iVBORw0KGgoAA...",
    "status":"ok"
}
```

#### To download the file
#### Request 
```shell
curl --request GET \
     --url 'https://www.covidash.it/api/plot?data_type=national&varname=totale_casi&download=true' \
     --output plot.png
```

The plot will be saved in `./plot.png`

## Plot preview
![alt_text](https://raw.githubusercontent.com/fabriziomiano/covidashit/main/previews/plot.png) 


## Donation
If you liked this project or if I saved you some time, feel free to buy me a beer. Cheers!

[![paypal](https://www.paypalobjects.com/en_US/IT/i/btn/btn_donateCC_LG.gif)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=PMW6C23XTQDWG)
