# Monitoraggio COVID-19 Italia

English Version [here](https://github.com/fabriziomiano/covidashit/blob/master/README.md)

Una semplice dashboard per il monitoraggio dell'epidemia di COVID-19 in Italia
che usa i dati forniti dalla [Protezione Civile](https://github.com/pcm-dpc) 

## Anteprima

![alt_text](https://raw.githubusercontent.com/fabriziomiano/covidashit/master/preview_it.png)

##### La WebApp è pubblicata su Heroku &#8594; [qui](https://covidashit.herokuapp.com/)

##### I dati della proezione civile vengono presi da github &#8594; [here](https://github.com/pcm-dpc/COVID-19/blob/master/dati-json/dpc-covid19-ita-andamento-nazionale.json)

## Per i developers

La WebApp gira su Python3.6+ ed usa un server Flask e gunicorn davanti.
Inoltre, viene usato Flask-babel per la traduzione italiana dell'app. Lo script `make_pot.sh` crea i file necessari.
La lingua di visualizzazione dipende dalla richiesta effettuata dal client.
Il back-end riceve i dati e li serve al frontend per le cards e la chart.
Non uso alcun database poiché per il momento, e speriamo neance in futuro, non si parla di molti dati.

Il front-end sta in `covidashit/templates` ed usa JavaScript per costruire la chart che è 
creata con [HighCharts](https://www.highcharts.com/)

#### Setup locale

* creazione di un virtual environment [(seguire questi passaggi)](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)
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

## Donazione

Se il progetto ti piace o se ti ho fatto risparmiare qualche linea di codice, sentiti libero di offrirmi un caffé. Grazie!

[![paypal](https://www.paypalobjects.com/en_US/IT/i/btn/btn_donateCC_LG.gif)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=PMW6C23XTQDWG)
