# Monitoraggio COVID-19 Italia | [\#IoRestoACasa](https://twitter.com/hashtag/iorestoacasa)

English Version [here](https://github.com/fabriziomiano/covidashit/blob/master/README.md)

Una semplice dashboard per il monitoraggio dell'epidemia di COVID-19 in Italia
che usa i dati forniti dalla [Protezione Civile](https://github.com/pcm-dpc) 

## Anteprima

![alt_text](https://raw.githubusercontent.com/fabriziomiano/covidashit/master/preview_it.png)

##### La WebApp è pubblicata su Heroku &#8594; [qui](https://covidashit.herokuapp.com/)

##### I dati della proezione civile vengono presi da github &#8594; [qui](https://github.com/pcm-dpc/COVID-19/blob/master/dati-json/dpc-covid19-ita-andamento-nazionale.json)

## Per gli sviluppatori

La WebApp gira su Python3.6+ ed usa un server Flask e gunicorn davanti.
Inoltre, viene usato Flask-babel per la traduzione italiana dell'app. Lo script `make_pot.sh` crea i file necessari.
Una versione `Batch` è fornita per gli utenti Windows. 
La lingua di visualizzazione dipende dalla richiesta effettuata dal client.
Il back-end riceve i dati e li serve al frontend per le cards e la chart.
Non uso alcun database poiché per il momento, e speriamo neance in futuro, non si parla di molti dati.

Ci sono 3 APIs:
* `GET /api/national` response `{"national": [...]}`
* `GET /api/regional` response `{"regional": [...]}`
* `GET /api/provincial` response `{"provincial": [...]}`

dove l'array contiene i dati originali come forniti dalla protezione civile.

Il front-end sta in `covidashit/templates` ed usa JavaScript per costruire la chart che è 
creata con [HighCharts](https://www.highcharts.com/)

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

##### Produzione
Il `Procfile` è pronto per essere utilizzato su Heroku. 
Per testare l'abmiente di produzione in locale:
```
$ gunicorn covidashit:app
```

Alternativamente, è possibile fare il build del container Docker:
```
docker-compose up -d
```
Se è andato tutto bene, la WebApp sarà in ascolto [http://127.0.0.1](http://127.0.0.1)

## Donazione

Se il progetto ti piace o se ti ho fatto risparmiare qualche linea di codice, sentiti libero di offrirmi un caffé. Grazie!

[![paypal](https://www.paypalobjects.com/en_US/IT/i/btn/btn_donateCC_LG.gif)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=PMW6C23XTQDWG)
