# Monitoraggio COVID-19 Italia | [\#IoRestoACasa](https://twitter.com/hashtag/iorestoacasa)

English Version [here](https://github.com/fabriziomiano/covidashit/blob/master/README.md)

Una semplice dashboard per il monitoraggio dell'epidemia di COVID-19 in Italia
che usa i dati forniti dalla [Protezione Civile](https://github.com/pcm-dpc) 

## Anteprima

Mobile          |  Desktop
:-------------------------:|:-------------------------:
![alt_text](https://raw.githubusercontent.com/fabriziomiano/covidashit/main/previews/mobile_it.png) |  ![alt_text](https://raw.githubusercontent.com/fabriziomiano/covidashit/main/previews/preview_it.png)

##### La WebApp è pubblicata su Heroku &#8594; [qui](https://covidashit.herokuapp.com/)

##### I dati della proezione civile vengono presi da github &#8594; [qui](https://github.com/pcm-dpc/COVID-19/blob/master/dati-json/dpc-covid19-ita-andamento-nazionale.json)

## Per gli sviluppatori

La WebApp gira su Python3.6+, legge i dati da mongoDB ed usa un server 
Flask e gunicorn davanti.
Viene usato Flask-babel per la traduzione italiana dell'app. 
Lo script `make_pot.sh` crea i file necessari a babel per le traduzioni.
Una versione `Batch` è fornita per gli utenti Windows. 
La lingua di visualizzazione dipende dalla richiesta effettuata dal client.

Il front-end sta in `covidashit/templates` ed usa JavaScript per costruire la chart che è 
creata con [HighCharts](https://www.highcharts.com/). 

Perché l'app funzioni è necessario popolare un database mongo: 
 - Vanno impostate le variabili d'ambiente :
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
 - le collezioni possono essere popolate tramite le APIs
    - POST `/recovery/<coll>` (`national`, `regional`, `provincial`)
    - POST `/recovery/<coll>/<type>` (`series`, `trends` for `coll=national` or `breakdown`, `series`, `trendws` for `coll=regional, provincial`)
    

#### Setup locale

* creazione ed attivazione di un virtual environment [(seguire questi passaggi)](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)
* installare i requirements in `requirements.txt`

##### Sviluppo
Clonare la repo e nella home directory di questa
```
$ export FLASK_ENV=development
$ export FLASK_DEBUG=1
$ python -m flask run
```

Flask sarà in ascolto all'url [http://127.0.0.1:5000](http://127.0.0.1:5000)

##### Produzione
Il Dockerfile fornito può essere usato per pubblicare l'app su Heroku.
Per testare l'abmiente di produzione in locale decommentare la L17, e 
 settare le variabili d'ambiente summenzionate. Lanciare:
```
$ docker build --tag covidashit:latest . 
$ docker run --name covidashit -d -p 80:5000 covidashit
```
Flask sarà in ascolto all'url [http://127.0.0.1](http://127.0.0.1) 

##### Note addizionali

L'app puo' essere pubblicata su Heroku sia come docker container che semplicemente utilizzando il Procfile.


## Plots API

L'app fornisce delle API per produrre i plot delle variabili con `matplotlib`.
Puo' tornare un JSON response con l'immagine codificata in base64 oppure il 
contenuto in byte per scaricare il file.

### Resource URL 

`https://www.covidash.it/api/plot`

### Parametri
| Nome      | Richiesto                                        | Descrizione                                  | Valore di default | Esempio                                  |
|-----------|-------------------------------------------------|----------------------------------------------|---------------|------------------------------------------|
| data_type | Si                                             | Il data type da plottare                        |               | uno tra ["national" "regional" "provincial"] |
| varname   | Si                                             | Il nome della variabile da plottare             |               | uno tra ["nuovi_positivi", "tamponi_g"...]    |
| area      | Solo se data_type è "regional" o "provincial" | The name of the area to filter the data with |               | uno tra ["Sicilia", "Catania"...]                  |
| download  | No                                              | The flag to download directly the file       | False         | "true"                                   |

### Esempi

#### Immagine codififcata in base64-encoded (JSON response)
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

#### Per scaricare il file 
###### Request 
```
curl --request GET \
    --url 'https://www.covidash.it/api/plot?data_type=national&varname=terapia_intensiva&download=true' \
    --output plot.png
```

Il plot verrà scritto in `./plot.png`

## Anteprima plot
![alt_text](https://raw.githubusercontent.com/fabriziomiano/covidashit/main/previews/plot.png) 


## Donazione

Se il progetto ti piace o se ti ho fatto risparmiare qualche linea di codice, 
sentiti libero di offrirmi un caffé. Grazie!

[![paypal](https://www.paypalobjects.com/en_US/IT/i/btn/btn_donateCC_LG.gif)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=PMW6C23XTQDWG)
