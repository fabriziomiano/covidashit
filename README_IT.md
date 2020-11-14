# Monitoraggio COVID-19 Italia | [\#IoRestoACasa](https://twitter.com/hashtag/iorestoacasa)

English Version [here](https://github.com/fabriziomiano/covidashit/blob/master/README.md)

Una semplice dashboard per il monitoraggio dell'epidemia di COVID-19 in Italia
che usa i dati forniti dalla [Protezione Civile](https://github.com/pcm-dpc) 

## Anteprima

Mobile          |  Desktop
:-------------------------:|:-------------------------:
![alt_text](https://raw.githubusercontent.com/fabriziomiano/covidashit/master/previews/mobile_it.png) |  ![alt_text](https://raw.githubusercontent.com/fabriziomiano/covidashit/master/previews/preview_it.png)

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
 - Vanno fatte le POST a `/api/update/<collection_type>` che popoleranno le varie collezioni, 
 ad es. ```POST /api/update/national```

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

##### Additional note

L'app puo' essere pubblicata su Heroku sia come docker container che semplicemente utilizzando il Procfile.

## Donazione

Se il progetto ti piace o se ti ho fatto risparmiare qualche linea di codice, 
sentiti libero di offrirmi un caffé. Grazie!

[![paypal](https://www.paypalobjects.com/en_US/IT/i/btn/btn_donateCC_LG.gif)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=PMW6C23XTQDWG)
