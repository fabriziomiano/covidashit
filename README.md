# COVID-19 Italy Monitor | [\#StayAtHome](https://twitter.com/hashtag/StayAtHome)

Versione Italiana [qui](https://github.com/fabriziomiano/covidashit/blob/main/README_IT.md)

A simple dashboard to display and monitor the official data of the COVID-19 outbreak in Italy released by the [Civil Protection Dept.](https://github.com/pcm-dpc/COVID-19) and updated on a daily basis.

## Previews

### Pandemic View 
![alt_text](https://raw.githubusercontent.com/fabriziomiano/covidashit/main/previews/pandemic.png)

### Vaccines View
![alt_text](https://raw.githubusercontent.com/fabriziomiano/covidashit/main/previews/vaccines.png)

##### The app is deployed on Heroku &#8594; [here](https://www.covidash.it/)

##### The data is taken from the official CP Dept repository &#8594; [here](https://github.com/pcm-dpc/COVID-19/blob/master/dati-json/dpc-covid19-ita-andamento-nazionale.json)


## For developers
The WebApp requires Python 3.8+ and reads the data from a mongoDB. It employs a Flask server with `gunicorn` in front of it.
Furthermore, it employs Flask-babel for the italian translation, as English is set as primary language. 
The script `make_pot.sh` creates the files needed by Babel for the translations.
A `Batch` version of the script is provided for Windows users. 
The app language is decided upon the client request (browser / OS).

The front-end lives under `covidashit/templates` and it uses JS to create the chart object, 
which is built using [HighCharts](https://www.highcharts.com/).

In order for the app to be operational, a mongoDB must be populated 
([see here](https://docs.atlas.mongodb.com/tutorial/create-new-cluster) for the creation of an Atlas mongoDB free cluster).
Additionally, mongo collections must be updated on a daily basis. The Flask contains a number of API whose purpose is to 
update the DB every time the `master` branch of the CP Dept repository is updated, via a GitHub webhook (see the GitHub workflow [here](https://github.com/fabriziomiano/COVID-19/blob/master/.github/workflows/merge-upstream.yml)).
Ultimately, the webhooks for the following APIs must be set on the CP forked repository:

 * `/update/national`
 * `/update/national/series`
 * `/update/national/trends`
 * `/update/regional`
 * `/update/regional/breakdown`
 * `/update/regional/series`
 * `/update/regional/trends`
 * `/update/provincial`
 * `/update/provincial/breakdown`
 * `/update/provincial/series`
 * `/update/provincial/trends`
 * `/update/vax/`
 * `/update/vax/summary`

#### Set up a local version
* create and activate a virtual environment [(follow this)](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)
* install the requirements in `requirements.txt`

The `.env` file contains all the env vars needed by the webapp. 
In particular, the `MONGO_URI` and the various collection names string must be set.
Before the Flask server is started, but after the virtual environment has been activated, 
the DB must be populated.
For this purpose a Flask CLI, which runs a very basic ETL procedures that populates the various collections, is included
and can be run with 

`python -m flask create-collections`

This, with a very basic ETL procedure, will populate the various collections on the DB with the official data released by the Civil Protection Dept.


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

## Plots API
The app provides an API to produce a server-side plot with `matplotlib`.
The API can return a JSON response with the base64-encoded image, or 
the bytes content to be saved as a file.

### Resource URL

`https://www.covidash.it/api/plot`

### Query parameters
#### Data type
```
data_type = [national, regional, provincial]
```
#### Var name
```
varname = [nuovi_positivi, ingressi_terapia_intensiva, deceduti_g, tamponi_g,
 totale_ospedalizzati_g, nuovi_positivi_ma, deceduti_g_ma, 
 ingressi_terapia_intensiva_ma, tamponi_g_ma, totale_ospedalizzati_g_ma, 
 totale_positivi, terapia_intensiva, ricoverati_con_sintomi, 
 totale_ospedalizzati, isolamento_domiciliare, totale_casi, deceduti, 
 tamponi, dimessi_guariti]
```
for `data_type = [national, regional]`
```
varname = [nuovi_positivi, nuovi_positivi_ma, totale_casi]
```
for `data_type = [provincial]`
#### Area (regions)
```
area = [Abruzzo, Basilicata, Calabria, Campania, Emilia-Romagna, Friuli Venezia Giulia,
 Lazio, Liguria, Lombardia, Marche, Molise, Piemonte, Puglia, Sardegna, 
 Sicilia, Toscana, P.A. Bolzano, P.A. Trento, Umbria, Valle d'Aosta, Veneto]
```

#### Area (provinces)
```
area = [Chieti, L'Aquila, Pescara, Teramo, Matera, Potenza, Catanzaro, Cosenza,
Crotone, Reggio di Calabria, Vibo Valentia, Avellino, Benevento, Caserta, 
Napoli, Salerno, Bologna, Ferrara, Forlì-Cesena, Modena, Parma, Piacenza, 
Ravenna, Reggio nell'Emilia, Rimini, Gorizia, Pordenone, Trieste, Udine, 
Frosinone, Latina, Rieti, Roma, Viterbo, Genova, Imperia, La Spezia, Savona, 
Bergamo, Brescia, Como, Cremona, Lecco, Lodi, Mantova, Milano, 
Monza e della Brianza, Pavia, Sondrio, Varese, Ancona, Ascoli Piceno, Fermo, 
Macerata, Pesaro e Urbino, Campobasso, Isernia, Alessandria, Asti, Biella, 
Cuneo, Novara, Torino, Verbano-Cusio-Ossola, Vercelli, Bari, 
Barletta-Andria-Trani, Brindisi, Lecce, Foggia, Taranto, Cagliari, Nuoro, 
Sassari, Sud Sardegna, Agrigento, Caltanissetta, Catania, Enna, Messina, 
Palermo, Ragusa, Siracusa, Trapani, Arezzo, Firenze, Grosseto, Livorno, Lucca,
Massa Carrara, Pisa, Pistoia, Prato, Siena, Perugia, Terni, Aosta, Belluno, 
Padova, Rovigo, Treviso, Venezia, Verona, Vicenza]
```

### Examples
#### A national plot
* `/api/plot?data_type=national&varname=<varname>`
#### A regional plot
* `/api/plot?data_type=regional&area=<region>&varname=<varname>`
#### A regional plot
* `/api/plot?data_type=provincial&area=<province>&varname=[nuovi_positivi,nuovi_positivi_ma,totale_casi]>`

##### To get the base64-encoded image in a JSON response
###### JSON

###### Request
```
curl --request GET \ 
     --url 'https://www.covidash.it/api/plot?data_type=national&varname=totale_casi'
```

###### Response
`{
    "errors":[],
    "img":"iVBORw0KGgoAA...",
    "status":"ok"
}`

#### To download the file
###### Request 
```
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
