##### Progetto Di Statistica 
# Gruppi sanguigni 
La repository in questione è la mia prima prova di analisi dati e come dataset ho scelto di usare i dati trovati nel seguente [sito](https://rhesusnegative.net/themission/bloodtypefrequencies/).

### Scraping
Per prima cosa, ho eseguito uno scraping dei file (`scraping.py`) per prendere i dati dal sito e salvarli all'interno di un database locale.
La tabella del database che ho usato aveva la seguente struttura:

| id | NameCountry | 0+ | A+ | B+ | AB+ | 0- | A- | B- | AB- | NameContinent | Population |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Italy | 40 | 36 | 7.5 | 2.5 | 7 | 6 | 1.5 | 0.5 | Europe | 4203200 |

### Coding
Per analizzare i dati ho usato la libreria numpy principalmente mentre per la creazione dei grafici ho usato le librerie di plotly (soprattutto per ottenre dei grafici molto puliti che matplotlib non riesce sempre ad offrire).

### Presentazione
Per la presentazione ho usato Jupyter collegato al codice `main.py` dove ho sviluppato tutte le funzioni.

Il mio obbiettivo è quello di riuscire a far parte del mondo della Data Science quindi questo è solo un progettino iniziale per iniziare a prendere mano con le librerie e soprattutto con la codifica di python.
Se avete consigli per ampiarlo, scrivetemi pure sulla email di Github, ve ne sarò grato!!


