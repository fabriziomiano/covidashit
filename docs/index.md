# COVID-19 Italy Monitor | [\#StayAtHome](https://twitter.com/hashtag/StayAtHome)

[![Awesome](https://awesome.re/badge.svg)](https://github.com/soroushchehresa/awesome-coronavirus#applications-and-bots)
[![Open Source Love](https://badges.frapsoft.com/os/v1/open-source.svg?v=103)](https://github.com/ellerbrock/open-source-badges/)
[![Made with Pthon](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)

![alt_text](previews/mockup.png)

A simple dashboard to display and monitor the official data of the COVID-19 outbreak in Italy, released by the [Italian Civil Protection Dept.](https://github.com/pcm-dpc/COVID-19), and the vaccination-status data, released by [Italia Open Data](https://github.com/italia/covid19-opendata-vaccini/).

**The app is deployed on an AWS EC2 instance [here](https://www.covidash.it/)**

**Pandemic data from the [official CP Dept repository](https://github.com/pcm-dpc/COVID-19/)**

**Vaccine data from the [official open-data repository](https://github.com/italia/covid19-opendata-vaccini)**


## For developers
The WebApp requires Python 3.10 and reads the data from a mongoDB. It employs a Flask server with `gunicorn` in front of it.
Furthermore, it employs Flask-babel for the italian translation, as English is set as primary language. 
The script `make_pot.sh` creates the files needed by Babel for the translations.
A `Batch` version of the script for Windows users is provided. 
The app language is decided upon the client request (browser / OS).

The front-end lives under `covidashit/templates` and it uses JS to create the chart object, 
which is built using [HighCharts](https://www.highcharts.com/).

In order for the app to be operational, a mongoDB must be populated 
([see here](https://docs.atlas.mongodb.com/tutorial/create-new-cluster) for the creation of an Atlas mongoDB free cluster).
The backend is populated by [covidashflow](https://github.com/fabriziomiano/covidashflow) - an Apache-Airflow ETL - which reads the pandemic data from the `master` branch of the [PCM-DPC repository](https://github.com/pcm-dpc/COVID-19/), and the vaccines data from the `master` branch of the [Italia Open Data repository](https://github.com/italia/covid19-opendata-vaccini/)


### Local deployment (DEV)
* create and activate a virtual environment [(follow this)](https://python-poetry.org/docs/managing-environments/)
* install the requirements via poetry `pip install --upgrade pip poetry && poetry install`

The `.env` file contains all the env vars needed by the webapp. 
In particular, the `MONGO_URI` and the various collection names string must be set.
The values of these variables should match those  in [covidashflow](https://github.com/fabriziomiano/covidashflow)
The WebApp should start without errors even if the backend is empty; no data will be visualized.

Clone the repo, `cd` into it, activate the virtual environment, run the application server
```shell
gunicorn wsgi:app
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

## Plots API
The app provides an API to produce plots with `matplotlib`.
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
![alt_text](previews/plot.png) 


## Donation
If you liked this project or if I saved you some time, feel free to buy me a beer. Cheers!

[![paypal](https://www.paypalobjects.com/en_US/IT/i/btn/btn_donateCC_LG.gif)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=PMW6C23XTQDWG)
