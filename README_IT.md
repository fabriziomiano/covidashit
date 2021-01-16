# Monitoraggio COVID-19 Italia | [\#IoRestoACasa](https://twitter.com/hashtag/iorestoacasa)
English Version [here](https://github.com/fabriziomiano/covidashit/blob/main/README.md)

Una semplice dashboard per la visualizzazione e il monitoraggio dei dati ufficiali sulla pandemia da COVID-19 rilasciati giornalmente dal [Dipartimento della Protezione Civile](https://github.com/pcm-dpc) 

## Anteprime

### Pandemic View 
![alt_text](https://raw.githubusercontent.com/fabriziomiano/covidashit/main/previews/pandemic_it.png)

### Vaccines View
![alt_text](https://raw.githubusercontent.com/fabriziomiano/covidashit/main/previews/vaccines_it.png)

##### La WebApp è pubblicata su Heroku &#8594; [qui](https://www/covidash.it)

##### I dati vengono presi dal repository ufficiale della proezione civile &#8594; [qui](https://github.com/pcm-dpc/COVID-19/blob/master/dati-json/dpc-covid19-ita-andamento-nazionale.json)

## Per gli sviluppatori
La WebApp gira su Python3.8+, legge i dati da mongoDB ed usa un server 
Flask e `gunicorn` davanti.
Viene usato Flask-babel per la traduzione italiana dell'app, poiché l'inglese è scelto come lingua di default. 
Lo script `make_pot.sh` crea i file necessari a babel per le traduzioni.
Una versione `Batch` è fornita per gli utenti Windows. 
La lingua di visualizzazione dipenderà dalla richiesta effettuata dal client (lingua del browser o del sistema operativo).

Il front-end sta in `covidashit/templates` ed usa JavaScript per costruire la chart che è 
creata con [HighCharts](https://www.highcharts.com/). 

Perché l'app funzioni è necessario popolare un database mongo 
([qui](https://docs.atlas.mongodb.com/tutorial/create-new-cluster) per documentazione mongoDB su creazione cluster Atlas).
Inoltre, le collezioni del DB devono essere aggiornate giornalmente. Per questo motivo, l'app contiene delle API che vengono chiamate da un GitHub Webhook che viene lanciato quando il branch `master` della repository della PC viene aggiornato (vedi GitHub workflow nel mio fork della repo della PC [qui](https://github.com/fabriziomiano/COVID-19/blob/master/.github/workflows/merge-upstream.yml)).
Infine, bisogna settare i vari webhooks sul fork della repo della PC per le seguenti API: 

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

#### Setup locale
* creazione ed attivazione di un virtual environment [(seguire questi passaggi)](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)
* installazione dei requisiti in `requirements.txt`

Il file `.env` contiene una serie di variabile d'ambiente necessarie al funzionamento della webapp.  
Prima di avviare il server Flask, ma dopo aver attivato il virtual environment e settato le variabili nel 
`.env` file, come ad esempio il `MONGO_URI` e i vari nomi delle collezioni (a discrezione dello sviluppatore), 
sarà necessario popolare il DB tramite la Flask CLI 

`python -m flask create-collections`

Questa, tramite una semplicissima procedura ETL, creerà e popolerà le collezioni su DB 
con i dati ufficiali del Dipartimento della Protezione Civile.

##### Dev & Test
Clonare la repo e nella home directory di questa
```
$ export FLASK_ENV=development
$ export FLASK_DEBUG=1
$ python -m flask run
```

Flask sarà in ascolto all'url [http://127.0.0.1:5000](http://127.0.0.1:5000)

##### Production
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


## Plot API
L'app fornisce delle API per produrre i plot delle variabili con `matplotlib`.
Puo' tornare un JSON response con l'immagine codificata in base64 oppure il 
contenuto in byte per scaricare il file.

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
se `data_type = [national, regional]`
```
varname = [nuovi_positivi, nuovi_positivi_ma, totale_casi]
```
se `data_type = [provincial]`
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
#### Plot nazionale
* `/api/plot?data_type=national&varname=<varname>`
#### Plot regionale
* `/api/plot?data_type=regional&area=<region>&varname=<varname>`
#### Plot provinciale
* `/api/plot?data_type=provincial&area=<province>&varname=[nuovi_positivi,nuovi_positivi_ma,totale_casi]>`

##### Immagine codififcata in base64-encoded
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

#### Per scaricare il file 
###### Request 
```
curl --request GET \
     --url 'https://www.covidash.it/api/plot?data_type=national&varname=totale_casi&download=true' \
     --output plot.png
```

Il plot verrà salvato in `./plot.png`

## Anteprima plot
![alt_text](https://raw.githubusercontent.com/fabriziomiano/covidashit/main/previews/plot.png) 


## Donazione
Se il progetto ti piace o se ti ho fatto risparmiare qualche linea di codice, 
sentiti libero di offrirmi un caffé. Grazie!

[![paypal](https://www.paypalobjects.com/en_US/IT/i/btn/btn_donateCC_LG.gif)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=PMW6C23XTQDWG)
