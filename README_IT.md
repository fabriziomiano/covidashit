# Monitoraggio COVID-19 Italia | [\#IoRestoACasa](https://twitter.com/hashtag/iorestoacasa)

[![Awesome](https://awesome.re/badge.svg)](https://github.com/soroushchehresa/awesome-coronavirus#applications-and-bots)
[![Open Source Love](https://badges.frapsoft.com/os/v1/open-source.svg?v=103)](https://github.com/ellerbrock/open-source-badges/)
[![Made with Pthon](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)

![alt_text](https://raw.githubusercontent.com/fabriziomiano/covidashit/main/previews/mockup.png)

English Version [here](https://github.com/fabriziomiano/covidashit/blob/main/README.md)

Una semplice dashboard per la visualizzazione e il monitoraggio dei dati ufficiali sulla pandemia da COVID-19 rilasciati giornalmente dal [Dipartimento della Protezione Civile](https://github.com/pcm-dpc) 

**La WebApp è pubblicata su un'istanza EC2 di AWS [qui](https://www.covidash.it)**

**Dati ufficiali sulla pandemia: [repository ufficiale della proezione civile](https://github.com/pcm-dpc/COVID-19)**

**Dati ufficiali sui vaccini: [repository ufficiale Developers Italia](https://github.com/italia/covid19-opendata-vaccini)**

## Per gli sviluppatori
La WebApp gira su Python3.8+, legge i dati da mongoDB e usa un server 
Flask e `gunicorn` davanti.
Viene usato Flask-babel per la traduzione italiana dell'app, poiché l'inglese è scelto come lingua di default. 
Lo script `make_pot.sh` crea i file necessari a babel per le traduzioni.
Una versione `Batch` è fornita per gli utenti Windows. 
La lingua di visualizzazione dipenderà dalla richiesta effettuata dal client (lingua del browser o del sistema operativo).

Il front-end sta in `covidashit/templates` e usa JavaScript per costruire la chart che è 
creata con [HighCharts](https://www.highcharts.com/). 

Perché l'app funzioni è necessario popolare un database mongo 
([qui](https://docs.atlas.mongodb.com/tutorial/create-new-cluster) per documentazione mongoDB su creazione cluster Atlas).
Inoltre, le collezioni del DB devono essere aggiornate giornalmente. Per questo motivo, l'app contiene delle API che vengono chiamate da un GitHub Webhook che viene lanciato quando il branch `master` della repository della PC viene aggiornato (vedi GitHub workflow nel mio fork della repo della PC [qui](https://github.com/fabriziomiano/COVID-19/blob/master/.github/workflows/merge-upstream.yml)).
Infine, bisogna settare i vari webhooks sul fork della repo della PC per le seguenti API: 

 * `POST /update/<data_type>`
 * `POST /update/<data_type>/<coll_type>`

| data_type  | coll_type                   |
|------------|-----------------------------|
| national   | [series, trends]            |
| regional   | [breakdown, series, trends] |
| provincial | [breakdown, series, trends] |
| vax        | [summary]                   |

### Setup locale  (DEV)
* creazione e attivazione di un virtual environment [(seguire questi passaggi)](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)
* installazione dei requisiti in `requirements.txt`

Il file `.env` contiene una serie di variabile d'ambiente necessarie al funzionamento della webapp.  
Prima di avviare il server Flask, ma dopo aver attivato il virtual environment e settato le variabili nel 
`.env` file, come ad esempio il `MONGO_URI` e i vari nomi delle collezioni (a discrezione dello sviluppatore), 
sarà necessario popolare il DB tramite la Flask CLI inclusa.  

Dopo aver clonato la repo e attivato il virtual environment: 
```shell
flask createdb
```
Questa, tramite una semplicissima procedura ETL, creerà e popolerà le collezioni su DB 
con i dati ufficiali del Dipartimento della Protezione Civile.

Successivamente, avviare il worker, 
```shell
celery -A celery_worker.celery worker
```

Infine, lanciare l'application server in una nuova shell:
```shell
gunicorn wsgi:app
```

Flask sarà in ascolto all'url [http://127.0.0.1:5000](http://127.0.0.1:5000)

### Setup locale (PROD)
Nel `.env` file settare il valore di `APPLICATION_ENV` con `production`.

#### Docker
Per avviare il container:
```shell
docker-compose up -d
```
Flask sarà in ascolto all'url [http://127.0.0.1:PORT] dove `PORT` viene 
settata in `.env`.

## Plot API
L'app fornisce delle API per produrre i plot delle variabili con `matplotlib`.
Puo' tornare un JSON response con l'immagine codificata in base64 oppure il 
contenuto in byte per scaricare il file.

### Resource URL

`https://www.covidash.it/api/plot`

### Query parameters

| data_type  | var_name                                                                                                                                                                                                                                                                                                                                                            | area                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
|------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| national   | [nuovi_positivi, ingressi_terapia_intensiva,  deceduti_g, tamponi_g,totale_ospedalizzati_g,  nuovi_positivi_ma, deceduti_g_ma,  ingressi_terapia_intensiva_ma, tamponi_g_ma, totale_ospedalizzati_g_ma, totale_positivi, terapia_intensiva, ricoverati_con_sintomi, totale_ospedalizzati, isolamento_domiciliare, totale_casi, deceduti,  tamponi, dimessi_guariti] | N/A                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| regional   | [nuovi_positivi, ingressi_terapia_intensiva,  deceduti_g, tamponi_g,totale_ospedalizzati_g,  nuovi_positivi_ma, deceduti_g_ma,  ingressi_terapia_intensiva_ma, tamponi_g_ma, totale_ospedalizzati_g_ma, totale_positivi, terapia_intensiva, ricoverati_con_sintomi, totale_ospedalizzati, isolamento_domiciliare, totale_casi, deceduti,  tamponi, dimessi_guariti] | [Abruzzo, Basilicata, Calabria, Campania, Emilia-Romagna, Friuli Venezia Giulia, Lazio, Liguria, Lombardia, Marche, Molise, Piemonte, Puglia, Sardegna, Sicilia, Toscana, P.A. Bolzano, P.A. Trento, Umbria, Valle d'Aosta, Veneto]                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| provincial | [nuovi_positivi, nuovi_positivi_ma, totale_casi]                                                                                                                                                                                                                                                                                                                    | [Chieti, L'Aquila, Pescara, Teramo,  Matera, Potenza, Catanzaro, Cosenza, Crotone, Reggio di Calabria, Vibo Valentia,  Avellino, Benevento, Caserta,  Napoli, Salerno, Bologna, Ferrara,  Forlì-Cesena, Modena, Parma, Piacenza,  Ravenna, Reggio nell'Emilia, Rimini,  Gorizia, Pordenone, Trieste, Udine,  Frosinone, Latina, Rieti, Roma, Viterbo,  Genova, Imperia, La Spezia, Savona,  Bergamo, Brescia, Como, Cremona, Lecco,  Lodi, Mantova, Milano,  Monza e della Brianza, Pavia, Sondrio,  Varese, Ancona, Ascoli Piceno, Fermo,  Macerata, Pesaro e Urbino, Campobasso,  Isernia, Alessandria, Asti, Biella,  Cuneo, Novara, Torino, Verbano-Cusio-Ossola,  Vercelli, Bari, Barletta-Andria-Trani,  Brindisi, Lecce, Foggia, Taranto, Cagliari,  Nuoro, Sassari, Sud Sardegna, Agrigento,  Caltanissetta, Catania, Enna, Messina,  Palermo, Ragusa, Siracusa, Trapani, Arezzo,  Firenze, Grosseto, Livorno, Lucca, Massa Carrara, Pisa, Pistoia, Prato, Siena,  Perugia, Terni, Aosta, Belluno,  Padova, Rovigo, Treviso, Venezia, Verona, Vicenza] |
        
### Examples
#### Plot nazionale 
`GET /api/plot?data_type=national&varname=<varname>`

#### Plot regionale
`GET /api/plot?data_type=regional&area=<region>&varname=<varname>`
    
#### Plot provinciale 
`GET /api/plot?data_type=provincial&area=<province>&varname=[nuovi_positivi,nuovi_positivi_ma,totale_casi]>`

    
##### Immagine codififcata in base64-encoded
###### JSON

###### Request
```shell
curl --request GET \ 
     --url 'https://www.covidash.it/api/plot?data_type=national&varname=totale_casi'
```

###### Response
```json
{
    "errors":[],
    "img":"iVBORw0KGgoAA...",
    "status":"ok"
}
```

#### Per scaricare il file 
###### Request 
```shell
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
