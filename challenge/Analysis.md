# Analysis

## Problema  per superare l'unitest

Al momento di cercare di effettuare il test in modo di verificare la correttezza della funzione mi sono trovato con l'impossibilità di superarlo giacche per l'**account_id = 3673936931** c'è una differenza tra i valori nella tabella *results* e quelli calcolati dalla mia funzione.  

### Account ID = 3673936931

**test result** = 113.444444  
**my result** = 115  

Questa differenza potrebbe essere giustificata tramite un cambio dei criteri arbitrari pressi nella realizzazione dei calcoli, come potrebbe essere il momento dove realizzare il bilancio giornaliero. Nella mia funzione il bilancio lo realiza alle ore "23:59:59.999".
Visto que per questo account tutte le transazioni si fanno alle "00:00:00.000" il fatto de includerlo nel giorno prescedente o no potrebbe influire sul risultato finale.

## Possibile problema nella funzione

Dai dati racolti per il calcolo del average del bilancio dentro una finestra di **90 giorni**, insieme alla definizione dell'average, sembra che ci sia dimenticato un possibile caso, quando lo storico TOTALE del conto non supera i 90 giorni. In questo caso, al calcolare l'average dei bilanci giornaleri non dovrebbe essere diviso per i 90 giorni, ma per la quantità totale di giorni dello storico. Continuare con questa definizione potrebbe generare una distorzione della misura.