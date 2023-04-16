# Analysis

## Problema  per superare l'unitest

Al momento di cercare di effettuare il test in modo di verificare la correttezza della funzione mi sono trovato con l'impossibilità di superarlo. In particolare con due **account_id** (**3673936931** e **3673936942**) si vedeva una differenza tra i valori nella tabella *results* e quelli calcolati dalla mia funzione.  
A continuazione lascio il riepilogo dello storico delle transazioni fatte dal account_id 3673936931, insieme a altre informazioni, sia fornita dal problema come calcolata da me in modo da aiutare a capire il problema.

### Account ID = 3673936931

**test result** = 113.444444  
**my result** = 123.444444  

| evento | data | amount | bilancio |
| ------ | ---- | ------ | -------- |
| init_reference | 2016-12-31 | - | 120 |
| creation | 2016-12-01 | - | 120 |
| transaction | 2017-01-15 | 10 | 130|
| transaction | 2017-02-15 | -10 | 120 |
| reference | 2017-03-31 | - | 120 |  

Nel periodo da analizzare (2016-12-31 a 2017-03-31) si può osservare in modo veloce come il bilancio inizia con un valore di **120** e mai nel suo storico scende sotto quel valore. Detto questo, al momento di calcolare il average dei bilanci in quel periodo non può essere mai inferiore a 120. Ma il valore de riferimento fornito per fare l'unitest è uguale a **113.444444**. Questa differenza non può essere giustificata tramite nessun cambio dei criteri arbitrari pressi nella realizzazione dei calcoli, come potrebbe essere il momento dove realizzare il bilancio giornaliero. Il valore calcolato da me per il average è uguale a **123.444444**, essendo coerente con quello detto prima. Per una maggiore correttezza ci vorrà fare delle verifiche sui dati forniti per la realizzazione del unitest.

## Possibile problema nella funzione

Dai dati racolti per il calcolo del average del bilancio dentro una finestra di **90 giorni**, insieme alla definizione dell'average, sembra che ci sia dimenticato un possibile caso, quando lo storico TOTALE del conto non supera i 90 giorni. In questo caso, al calcolare l'average dei bilanci giornaleri non dovrebbe essere diviso per i 90 giorni, ma per la quantità totale di giorni dello storico. Continuare con questa definizione potrebbe generare una distorzione della misura.