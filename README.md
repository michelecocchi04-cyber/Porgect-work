# Sistema di Gestione e Simulazione per Azienda Agraria

Questo repository contiene un software sviluppato in **Python** per l'ottimizzazione e la simulazione dei processi di coltivazione, raccolta e logistica di un'azienda agraria. 

Il programma permette di gestire le risorse agricole, pianificare la raccolta (manuale o automatizzata) e calcolare accuratamente le tempistiche di produzione e spedizione sul territorio nazionale.

## Funzionalità del Programma (Struttura dei Menu)

- Il software è strutturato attraverso un'interfaccia a **3 Menu principali**:

### Menu 1: Catalogo Coltivazioni
* Consente di visualizzare la **lista completa dei prodotti** che l'azienda è in grado di coltivare.
* Fornisce una panoramica delle sementi e delle colture disponibili nel sistema.

### Menu 2: Pianificazione, Gestione e Tempistiche dell'Ordine
In questa sezione l'utente può configurare un ordine personalizzato e il sistema calcolerà i tempi di lavorazione:
* **Selezione Prodotti:** Scelta di un massimo di **5 prodotti** simultaneamente.
* **Inserimento Quantità:** Definizione dei chilogrammi (kg) da produrre per ciascuna coltura.
* **Modalità di Raccolta:** Scelta tra raccolta **manuale** o **automatica** (con blocco e gestione code se le **2 macchine automatiche** sono già occupate).
* **Calcolo dei Tempi e Output a Schermo:**
  * Mostra il tempo di **coltivazione singolo** per ogni specifico prodotto selezionato.
  * Mostra il tempo di **raccolta totale**, sommando il tempo impiegato per completare tutti i prodotti dell'ordine.
  * Mostra il tempo necessario per **inviare l'intero ordine** a destinazione (escludendo i giorni festivi e bloccando le spedizioni fuori dall'Italia).

### Menu 3: Simulazione Rapida su Singolo Prodotto Casualità
A differenza del Menu 2 (dove l'utente sceglie tutto l'ordine), questo modulo avvia una simulazione automatica:
* **Generazione Casuale:** Il sistema seleziona autonomamente **un solo prodotto a caso** dalla lista aziendale.
* **Calcolo dei Tempi:** Mostra a schermo la simulazione completa delle tempistiche (coltivazione, raccolta e spedizione nazionale senza festivi) specifiche per quell'unico prodotto estratto.

## Tecnologie Utilizzate
* **Linguaggio:** Python 3.14.3
* **Paradigma:** Programmazione procedurale / modulare con gestione dei flussi condizionali.
