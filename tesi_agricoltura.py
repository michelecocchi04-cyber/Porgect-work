
import datetime
import locale
import os
import random
import math

# mi da i nomi del giorno e del mese in italiano
for x in ["it_IT.UTF-8", "it_IT", "ita_it", "Italian"]: # cambia in base al sistema operativo: Windows, macOS, Linux
    try:
       locale.setlocale(locale.LC_TIME, x) 
    except locale.Error:
        continue

try: # centrare il titolo, tuttavia per evitare che alcuni ambienti lo mandino in crash
    larghezza_terminale = os.get_terminal_size().columns
except OSError:
    larghezza_terminale = 80

# dizionario prodotti azienda
DATASET_AZIENDA = {
    
    "ortaggi e verdure": {
        "pomodori": {
            "crescita_base": 75,   # giorni
            "priorità_raccolta": 3, # su una scala 1-3 (dove 3 è il più urgente e 1 il meno) si classificano i prodotti in base al loro deterioramento
            "manuale": {"tempo_raccolta_kg": 2.5, "capacita_giornaliera_singolo": 192},   # min/kg, kg/giorno
            "automatico": {"tempo_raccolta_kg": 1.2, "capacita_giornaliera": 800}
            
        },
        "lattuga": {
            "crescita_base": 45,
            "priorità_raccolta": 3,
            "manuale": {"tempo_raccolta_kg": 3, "capacita_giornaliera_singolo": 160},
            "automatico": {"tempo_raccolta_kg": 1.5, "capacita_giornaliera": 700}
        },
        "patate": {
            "crescita_base": 100,
            "priorità_raccolta": 1,
            "manuale": {"tempo_raccolta_kg": 1.8, "capacita_giornaliera_singolo": 266},
            "automatico": {"tempo_raccolta_kg": 0.8, "capacita_giornaliera": 2500}
        },
        "cipolle": {
            "crescita_base": 105,
            "priorità_raccolta": 1,
            "manuale": {"tempo_raccolta_kg": 1.6, "capacita_giornaliera_singolo": 300},
            "automatico": {"tempo_raccolta_kg": 0.7, "capacita_giornaliera": 2200}
        },
        "carote": {
            "crescita_base": 85,
            "priorità_raccolta": 2,
            "manuale": {"tempo_raccolta_kg": 2, "capacita_giornaliera_singolo": 240},
            "automatico": {"tempo_raccolta_kg": 0.9, "capacita_giornaliera": 1800}
        },
    },
    "frutta": {
        "uva": {
            "crescita_base": 150,
            "priorità_raccolta": 3,
            "manuale": {"tempo_raccolta_kg": 3, "capacita_giornaliera_singolo": 160},
            "automatico": {"tempo_raccolta_kg": 1.5, "capacita_giornaliera": 1000}
        },
        "mele": {
            "crescita_base": 160,
            "priorità_raccolta": 2,
            "manuale": {"tempo_raccolta_kg": 2.2, "capacita_giornaliera_singolo": 218},
            "automatico": {"tempo_raccolta_kg": 1, "capacita_giornaliera": 1400}
        },
        "arance": {
            "crescita_base": 210,
            "priorità_raccolta": 2,
            "manuale": {"tempo_raccolta_kg": 2.5, "capacita_giornaliera_singolo": 192},
            "automatico": {"tempo_raccolta_kg": 1.2, "capacita_giornaliera": 1600}
        },
        "pere": {
            "crescita_base": 150,
            "priorità_raccolta": 2,
            "manuale": {"tempo_raccolta_kg": 2.3, "capacita_giornaliera_singolo": 208},
            "automatico": {"tempo_raccolta_kg": 1.1, "capacita_giornaliera": 1300}
        },
        "fragole": {
            "crescita_base": 75,
            "priorità_raccolta": 3,
            "manuale": {"tempo_raccolta_kg": 4, "capacita_giornaliera_singolo": 120},
            "automatico": {"tempo_raccolta_kg": 2, "capacita_giornaliera": 500}
        },
        "olive": {
            "crescita_base": 210,
            "priorità_raccolta": 1,
            "manuale": {"tempo_raccolta_kg": 3.5, "capacita_giornaliera_singolo": 137},
            "automatico": {"tempo_raccolta_kg": 1.8, "capacita_giornaliera": 900}
        },
    },
    "cereali e semi": {
        "grano": {
            "crescita_base": 135,
            "priorità_raccolta": 1,
            "manuale": {"tempo_raccolta_kg": 1, "capacita_giornaliera_singolo": 480},
            "automatico": {"tempo_raccolta_kg": 0.5, "capacita_giornaliera": 2000}
        },
        "mais": {
            "crescita_base": 105,
            "priorità_raccolta": 1,
            "manuale": {"tempo_raccolta_kg": 1.5, "capacita_giornaliera_singolo": 320},
            "automatico": {"tempo_raccolta_kg": 0.7, "capacita_giornaliera": 1500}
        },
        "riso": {
            "crescita_base": 125,
            "priorità_raccolta": 1,
            "manuale": {"tempo_raccolta_kg": 1.3, "capacita_giornaliera_singolo": 369},
            "automatico": {"tempo_raccolta_kg": 0.6, "capacita_giornaliera": 2300}
        },
        "girasoli": {
            "crescita_base": 95,
            "priorità_raccolta": 1,
            "manuale": {"tempo_raccolta_kg": 1.7, "capacita_giornaliera_singolo": 282},
            "automatico": {"tempo_raccolta_kg": 0.8, "capacita_giornaliera": 1900}
        },
    }
}

# titolo programma
def titolo():
    
    x = datetime.datetime.now().date()    # data odierna senza ore e minuti
    
    nome_farm = "FarmProduction Simulator"
    riga_titolo = "AZIENDA AGRICOLA DI FRUTTA & VERDURA"
    riga_separatore = "=" * 42
    
    print(x.strftime("\n\n%A %d-%B %Y").upper())
    print("\n" + f"{nome_farm.center(larghezza_terminale)}")
    print("\n" + f"\033[1m{riga_titolo.center(larghezza_terminale)}\033[0m") # grassetto
    print(riga_separatore.center(larghezza_terminale) + "\n\n")
    
# definisco le stagioni  con le rispettive catastrofi (3) & (2)
def stagione(data, giorni_ritardo):
    
    oggi =  data.month * 1000 + data.day  # così abbaimo un numero pulito diviso dallo zero
    
    #Primavera: 21 Marzo  - Estate: 21 Giugno
    # Autunno: 23 Settembre - Inverno: 21 Dicembre
    
    if 3021 <= oggi < 6021: 
        print("-" * 50)
        print(f"- [ATTENZIONE] Sfortunatamente i tempi di crescita si sono allungati di {giorni_ritardo} a causa delle forti innondazioni primaverili") 
        print("-" * 50)
    elif 6021 <= oggi < 9023:
        print("-" * 50)
        print(f"- [ATTENZIONE] Sfortunatamente i tempi di crescita si sono allungati di {giorni_ritardo} a causa della siccità estiva")
        print("-" * 50)
    elif 9023 <= oggi < 12021:
        print("-" * 50)
        print(f"- [ATTENZIONE] Sfortunatamente i tempi di crescita si sono allungati di {giorni_ritardo} a causa delle forti piogge autunnali")
        print("-" * 50)
    else:
        print("-" * 50)
        print(f"- [ATTENZIONE] Sfortunatamente i tempi di crescita si sono allungati di {giorni_ritardo} a causa del gelo invernale")  
        print("-" * 50)
        
# per imprevidibilità della coltivazione (2)
def variabile_crescita_base(categoria, prodotto):
    
    oggi = datetime.datetime.now().date()
    
    valore_originale = DATASET_AZIENDA[categoria][prodotto]["crescita_base"]
    valore_random = random.uniform(-0.15, 0.15)
    valore_uscita = round(valore_originale * (1+ valore_random)) # arrotonda al primo numero intero più vicino
    
    #imprevisto
    catastrofe = random.randint(1,100)
    if catastrofe <=5:
        giorni_ritardo  = random.randint(10,30)
        valore_uscita += giorni_ritardo
        stagione(oggi, giorni_ritardo)
        
    return valore_uscita

# periodo di coltivazione (2)
def calcolo_crescita(categoria_selezionata,prodotto):   
    
    giorni_crescita = variabile_crescita_base(categoria_selezionata, prodotto)
    print(f"- Per coltivare il prodotto selezionato ({prodotto}) ci vogliono {giorni_crescita} giorni")
    
    return giorni_crescita 

# per dare all'utente un giorno esatto per il ritiro (3) & (2) 
def calcola_data_consegna(giorni_totali_lavoro):
    
    giorno_contatore = 0
    giorno_attuale = datetime.datetime.now().date()
    anno_corrente = giorno_attuale.year
    
    def festivi(anno):
        return { # lo prende e lo manda direttamente fuori dalla def, se lo mettevo alla fine mi dava None
            datetime.date(anno, 1, 1),   # Capodanno
            datetime.date(anno, 1, 6),   # Epifania
            datetime.date(anno, 4, 25),  # 25 Aprile
            datetime.date(anno, 5, 1),   # 1 Maggio
            datetime.date(anno, 6, 2),   # 2 Giugno
            datetime.date(anno, 8, 15),  # Ferragosto
            datetime.date(anno, 11, 1),  # Ognissanti
            datetime.date(anno, 12, 8),  # Immacolata
            datetime.date(anno, 12, 25), # Natale
            datetime.date(anno, 12, 26), # S.Stefano    
        } 

    festività = festivi(anno_corrente)| festivi(anno_corrente+1) #quest'anno e l'anno prossimo
    
    def ponte_natalizio(data_anno):
        if data_anno.month == 12 and data_anno.day >= 25:
            return True # se è in quelle date 
        if data_anno.month == 1 and data_anno.day <= 6:
            return True
        return False # se non è in questo range non siamo nel ponte
    
    
    while giorno_contatore < giorni_totali_lavoro:
        giorno_attuale += datetime.timedelta(days = 1)
        
        #inserisco dei flag Truee
        se_weekand = giorno_attuale.weekday() >= 5 # lunedì 0 ... sabato 5 domenica 6
        se_natale = ponte_natalizio(giorno_attuale)
        se_festa = giorno_attuale in festività
        
        if not se_weekand and not se_natale and not se_festa: # se sono tutti falsi allora...
            giorno_contatore += 1
        
    return giorno_attuale
               
# calcola quanto ci mette a inviare i prodotti (3) & (2)  
def spedizione(data_consegna):
    
    nom_sped = "--- SPEDIZIONE PRODOTTO ---"
    print("\n" + "-" * 50)    
    print("\n\n" + f"{nom_sped.center(larghezza_terminale)}")
    print("\n\n" + "-" * 50)   
    print("\n- L'azienda agricola ha sede a Roma")
    
    while True:
                    
        print("\n- Inserisci \"1\" se risiedi nella stessa città")
        print("- Inserisci \"2\" se risiedi nelle provincie e d'intorni")
        print("- Inserisci \"3\" se risiedi in italia ")
        print("- Inserisci \"4\" se risiedi fuori dall'Italia")
                 
        opzione_residenza = input("\n- Scegli: ").strip()
           
        if opzione_residenza == "1":
            data_consegna += datetime.timedelta(days = 1)
            break
        elif opzione_residenza == "2":
            x = random.randint(2,3) #timedelta non legge float
            data_consegna += datetime.timedelta(days = x) 
            break   
        elif opzione_residenza == "3":
            y = random.randint(4,6)
            data_consegna += datetime.timedelta(days = y) 
            break
        elif opzione_residenza == "4":
            print("\n" + "-" * 50)
            print("- [ATTENZIONE] NON SI EFFETTUANO SPEDIZIONI FUORI DALL'ITALIA, RIPROVA A INSERIRE UN ALTRA RESIDENZA")
            print("-" * 50)
            continue
        else:
            print("\n" + "-" * 50)
            print("- [ATTENZIONE] SCELTA NON VALIDA. RIPROVA")
            print("-" * 50)
            continue
    
    return data_consegna.strftime("%A %d-%B %Y").upper()
    
# calcolo del tempo impiegato per raccogliere (2)
def calcolo_totale(domanda_quantità, categoria_selezionata, prodotto, metodo_lavoro, numero_risorse_assegn_):
    
    if metodo_lavoro == "manuale":
        prodotto_kg_minuto = DATASET_AZIENDA[categoria_selezionata][prodotto]["manuale"]["tempo_raccolta_kg"]
        max_giornaliero = DATASET_AZIENDA[categoria_selezionata][prodotto]["manuale"]["capacita_giornaliera_singolo"]
        
        max_giornaliero_squadra_fisso = max_giornaliero * numero_risorse_assegn_
        variazione_rendimento_squadra = random.uniform(-0.04, 0.04) 
        max_giornaliero_squadra_var = max_giornaliero_squadra_fisso * (1 + variazione_rendimento_squadra)
        
        ore_totali = round((domanda_quantità * prodotto_kg_minuto) / numero_risorse_assegn_ / 60)
        
        if ore_totali == 0 and domanda_quantità > 0:
            ore_totali = 1
        giorni_totali = math.ceil(domanda_quantità / max_giornaliero_squadra_var) 
        
    elif metodo_lavoro == "automatico":
        prodotto_kg_minuto = DATASET_AZIENDA[categoria_selezionata][prodotto]["automatico"]["tempo_raccolta_kg"]
        max_giornaliero = DATASET_AZIENDA[categoria_selezionata][prodotto]["automatico"]["capacita_giornaliera"]        
        ore_totali = round((domanda_quantità * prodotto_kg_minuto) / 60)
    
        if ore_totali == 0 and domanda_quantità > 0:
            ore_totali = 1
        giorni_totali = math.ceil(domanda_quantità / max_giornaliero) 
        
    return ore_totali, giorni_totali  

# gestisco la distribuzione degli operai per prodotto  (2)  
def distribuisci_operai(ordine_carrello):
    
    operai_disponibili = 10
        
    for prodotto in ordine_carrello: 
        if prodotto["metodo"] == "manuale":
            prodotto["operai"] = 2
            operai_disponibili -= 2
                 
        elif prodotto["metodo"] == "automatico":
            prodotto["operai"] = 0
    
    prodotti_manuali = [p for p in ordine_carrello if p["metodo"] == "manuale"] #genero una lista a volo
    prodotti_manuali_ordinati = sorted(prodotti_manuali, key=lambda x: x["quantità"], reverse=True) # key=lambda dice al programma dove andare a cercare esattamente, essendo una lista in un dizionario, reverse=True mi da i numeri in maniera decrescente
    
    while operai_disponibili > 0 and len(prodotti_manuali_ordinati) > 0:
        operai_assegnati_in_questo_giro = False  # Flag
    
        for prodotto in prodotti_manuali_ordinati:
            if operai_disponibili > 0 and prodotto["operai"] < 5:
                prodotto["operai"] += 1
                operai_disponibili -= 1
                operai_assegnati_in_questo_giro = True  # sta ancora andando 
            
        if not operai_assegnati_in_questo_giro:
            break  # interrompo se c'è solo un prodotto e arrivo già a cinque 
        
    for prodotto in ordine_carrello:
        if prodotto["metodo"] == "manuale" and "operai_iniziali" not in prodotto:
            prodotto["operai_iniziali"] = prodotto["operai"] # salvaimo in operai_iniziali il valore attuale, così anche se in seguito si elimina ce l'abbiamo

# gestisce più lavori in uno stesso lasso di tempo (2)                  
def lavoro_parallelo_(carrello_urgenze):
    
    prodotti_automatici_ordinati = [p for p in carrello_urgenze if p["metodo"] == "automatico"]
    
    # se non c'è conflitto 
    gestione_conflitti = "1" 
    strategia_manuale = "1"
    
    if len(prodotti_automatici_ordinati) > 2:
        nom_conf = "-------- GESTIONE CONFLITTI --------"
        print( f"{nom_conf.center(larghezza_terminale)}" + "\n\n")
        print( "-" * 50 + "\n" ) 
        
        while True:
            print("- Inserisci \"1\" per la GESTIONE AUTOMATICA dei conflitti di risorse")
            print("- Inserisci \"2\" per la GESTIONE MANUALE")
            gestione_conflitti = input("\n- Scegli: ").strip()
            
            if gestione_conflitti in ["1", "2"]: 
                break
            print("\n" + "-" * 50)
            print("- [ATTENZIONE] SCELTA NON VALIDA. RIPROVA")
            print("-" * 50 + "\n" )

        if gestione_conflitti == "2":
            while True:
                print("\n  Inserisci \"1\" se intendi far attendere il prodotto in coda")
                print("  Inserisci \"2\" se intendi passare al metodo manuale con operai")
                strategia_manuale = input("\n- Scegli: ").strip()
                
                if strategia_manuale in ["1", "2"]:
                    break
                print("\n" + "-" * 50)
                print("- [ATTENZIONE] SCELTA NON VALIDA. RIPROVA")
                print("-" * 50 + "\n" )

    giorno = 0
    
    for prodotto in carrello_urgenze:
        prodotto["kg_rimasti"] = prodotto["quantità"]
        prodotto["giorni_crescita_rimasti"] = prodotto["crescita"]
        prodotto["stato"] = "in_crescita"
        prodotto["conflitto_gestito"] = False
        prodotto["ore_totali_accumulate"] = 0
        
    while any(prodotto["kg_rimasti"] > 0 for prodotto in carrello_urgenze):
        giorno += 1
        
        for prodotto in carrello_urgenze:
            if prodotto["stato"] == "in_crescita":
                prodotto["giorni_crescita_rimasti"] -= 1
                if prodotto["giorni_crescita_rimasti"] == 0:
                    prodotto["stato"] = "cresciuto"
        
        macchine_occupate = 0 
        prodotti_automatici = []       
            
        for prodotto in carrello_urgenze:
            # gestione prodotti manuali
            if prodotto["metodo"] == "manuale" and prodotto["stato"] == "cresciuto" and prodotto["kg_rimasti"] > 0:
                lavoro_giornaliero_sing_fisso = DATASET_AZIENDA[prodotto["categoria"]][prodotto["nome"]]["manuale"]["capacita_giornaliera_singolo"]
                variaziona_operaio = random.uniform(-0.07, 0.07) 
                lavoro_giornaliero_sing_var = lavoro_giornaliero_sing_fisso * (1 + variaziona_operaio)
                
                if prodotto.get("operai", 0) == 0:
                    distribuisci_operai(carrello_urgenze)
                
                prodotto["ore_totali_accumulate"] += 8
                kg_raccolti_oggi_mano = prodotto.get("operai", 0) * lavoro_giornaliero_sing_var
                prodotto["kg_rimasti"] -= kg_raccolti_oggi_mano
                
                if prodotto["kg_rimasti"] <= 0:
                    prodotto["kg_rimasti"] = 0
                    prodotto["stato"] = "completato"
                    prodotto["operai"] = 0  # libera gli operai
                    
            # gestione automatici (se sono liberi)
            elif prodotto["metodo"] == "automatico" and prodotto["stato"] == "cresciuto" and prodotto["kg_rimasti"] > 0:
                if macchine_occupate < 2:
                    macchine_occupate += 1
                    prodotti_automatici.append(prodotto["nome"])
                    prodotto["ore_totali_accumulate"] += 8
                    lavoro_giornaliero_aut_ = DATASET_AZIENDA[prodotto["categoria"]][prodotto["nome"]]["automatico"]["capacita_giornaliera"]
                    prodotto["kg_rimasti"] -= lavoro_giornaliero_aut_
                    
                    if prodotto["kg_rimasti"] <= 0:
                        prodotto["kg_rimasti"] = 0
                        prodotto["stato"] = "completato"
    
                # gestione conflitto
                else: 
                    if gestione_conflitti == "1":
                        operai_gia_occupati = sum(p.get("operai", 0) for p in carrello_urgenze if p["kg_rimasti"] > 0 and p["metodo"] == "manuale")
                        operai_liberi = 10 - operai_gia_occupati
                        
                        if operai_liberi >= 2:
                            prodotto["metodo"] = "manuale"
                            prodotto["operai"] = 0
                            distribuisci_operai(carrello_urgenze)
                            prodotto["ore_totali_accumulate"] += 8
                            lavoro_giornaliero_sing_fisso = DATASET_AZIENDA[prodotto["categoria"]][prodotto["nome"]]["manuale"]["capacita_giornaliera_singolo"]
                            variaziona_operaio = random.uniform(-0.07, 0.07)
                            lavoro_giornaliero_sing_var = lavoro_giornaliero_sing_fisso * (1 + variaziona_operaio)
                            prodotto["kg_rimasti"] -= (prodotto.get("operai", 0) * lavoro_giornaliero_sing_var)
                        else:
                            pass # Macchine piene e operai finiti, aspetta
                    # qui decideiamo la selezione manuale     
                    elif gestione_conflitti == "2":
                        if strategia_manuale == "1":
                            pass # attende in coda
                        elif strategia_manuale == "2":
                            prodotto["metodo"] = "manuale" 
                            prodotto["operai"] = 0 
                            distribuisci_operai(carrello_urgenze)
                            prodotto["ore_totali_accumulate"] += 8
                            lavoro_giornaliero_sing_fisso = DATASET_AZIENDA[prodotto["categoria"]][prodotto["nome"]]["manuale"]["capacita_giornaliera_singolo"]
                            variaziona_operaio = random.uniform(-0.07, 0.07)
                            lavoro_giornaliero_sing_var = lavoro_giornaliero_sing_fisso * (1 + variaziona_operaio)
                            prodotto["kg_rimasti"] -= (prodotto.get("operai", 0) * lavoro_giornaliero_sing_var)

                    if prodotto["kg_rimasti"] <= 0:
                        prodotto["kg_rimasti"] = 0
                        prodotto["stato"] = "completato"
                        prodotto["operai"] = 0
                                            
    return giorno

# chiede che categoria di prodotti da scegliere (2)          
def visualizza_prodotti():
    
    while True:
        print("\n- Inserisci \"1\" per visualizzare gli ortaggi e le verdure disponibili")
        print("- Inserisci \"2\" per visualizzare i frutti disponibili")
        print("- Inserisci \"3\" per visualizzare i cereali e i semi disponibili")
     
        opzione_visualizzazione = input("\n- Scegli: ").strip()

        if opzione_visualizzazione == "1":
            stampa_categoria("ortaggi e verdure")
            return "ortaggi e verdure"
            
        elif opzione_visualizzazione == "2":
            stampa_categoria("frutta")
            return "frutta"  
      
        elif opzione_visualizzazione == "3":
            stampa_categoria("cereali e semi")
            return "cereali e semi"
        
        else:
            print("\n" + "-" * 50)
            print("[ATTENZIONE] SCELTA NON VALIDA. RIPROVA")
            print("-" * 50)

# visualizzazione prodotti della categoria scelta (2)
def stampa_categoria(nome_categoria):
    
    testo_intestazione = "- Prodotti disponibili per la categoria " + nome_categoria + " :"
    print("\n" + testo_intestazione) 
    print("-" * len(testo_intestazione) + "\n")
    
    prodotti = DATASET_AZIENDA[nome_categoria]
    for i in prodotti.keys():
        print(" - " + i.capitalize()) 
    print("\n" + "-" * len(testo_intestazione))
 
#comando errore se uno inserisce due volte lo stesso prodotto (2)   
def inserimento_duplicato(oggetto, lista):
    
    if oggetto in [x["nome"] for x in lista]: 
        return True
    return None 
         
# scegli un prodotto inerente alla categoria selezionata, e poi decidi la quantità (2)     
def scelta(categoria_scelta, lista_prodotto_non_disp, carrello):
    
    contatore = 0
    
    while True:
        
        domanda_prodotto = input("\n- Scegli il tipo di prodotto di cui hai bisogno: ").strip().lower()
        
        if inserimento_duplicato(domanda_prodotto, carrello):
            print("\n" + "-" * 50)
            print("- [ATTENZIONE] NON È POSSIBILE SELEZIONARE DUE VOLTE LO STESSO PRODOTTO")
            print("-" * 50)
            continue
        
        if domanda_prodotto in lista_prodotto_non_disp: # verifica esaurimento
            print("\n" + "-" * 50)
            print(f"- [ATTENZIONE] ATTUALMENTE NON È POSSIBILE COLTIVARE IL PRODOTTO: {domanda_prodotto.upper()}. SELEZIONA UN ALTRO PRODOTTO")
            print("-" * 50)
            continue
            
        if domanda_prodotto not in DATASET_AZIENDA[categoria_scelta]:
            print("\n" + "-" * 50)
            print(f"- [ATTENZIONE] IL PRODOTTO \"{domanda_prodotto.upper()}\" NON È SOTTO LA CATEGORIA {categoria_scelta.upper()}")
            print("-" * 50)
            continue 

        capacità_coltivazione__casuale = random.randint(0, 7000) # anche nullo
       
        if capacità_coltivazione__casuale <= 100:
            print("\n" + "-" * 50 + "\n")
            print("- [ATTENZIONE] LA CAPACITÀ DI PIANIFICAZIONE DEL PRODOTTO SCELTO È MOMENTANEAMENTE ESAURITA. NON È POSSIBILE ACQUISTARLO")
            print("-" * 50)
            lista_prodotto_non_disp.append(domanda_prodotto)
            continue # torna all'inizio
        
        elif capacità_coltivazione__casuale > 100:
            print(f"- La capienza massima del campo per la coltivazione del prodotto selezionato: {domanda_prodotto.upper()} è di {capacità_coltivazione__casuale} kg")
            break

    while True:
            
        try:
            if contatore == 0 :
                print("\n" + "-" * 50)
                print("- [ATTENZIONE] LA QUANTITÀ DI PRODOTTO SCELTO NON PUÒ ESSERE INFERIORE AD UN QUINTALE")
                print("-" * 50)
                contatore += 1 # per non far rivedere questo print
                
            domanda_quantità = float(input("\n- Scegli la quantità numerica che ti occorre (IL PROGRAMMA CALCOLA IN KG): ").strip())
                
            if domanda_quantità < 100:
                print("\n" + "-" * 50)
                print("- [ATTENZIONE] LA QUANTITÀ DI PRODOTTO SCELTO NON PUÒ ESSERE MINORE DI 100 KG")
                print("-" * 50)
                continue
            
            if domanda_quantità > capacità_coltivazione__casuale:
                print("\n" + "-" * 50)
                print("- [ATTENZIONE] LA QUANTITÀ DI PRODOTTO SCELTO È SUPERIORE ALLA DISPONIBILITÀ")
                print("-" * 50)
                continue
                
            return domanda_prodotto, domanda_quantità, carrello 
                    
        except ValueError:
            print("\n" + "-" * 50)
            print("- [ATTENZIONE] IL VALORE INSERITO DEVE ESSERE NUMERICO")
            print("-" * 50)
              
# scelta metodo manuale o automatizzato (2)
def seleziona_metodo_lavoro():
    
    nom_tit = "--- GESTIONE METODO DI RACCOLTA ---"
    riga_avviso = "[ATTENZIONE]: Le macchine automatiche disponibili sono al massimo 2"           
    print(f"{nom_tit.center(larghezza_terminale)}")
    print(f"{riga_avviso.center(larghezza_terminale)}" + "\n\n")  
    print("-" * 50 + "\n") 
    
    while True:

        print("- Seleziona \"1\" per la coltivazione manuale (Tradizionale, richiede più tempo: sabato e domenica non sono lavorativi)")
        print("- Seleziona \"2\" per la coltivazione automatizzata (Macchinari industriali, più rapido: lavora ogni giorno alla stessa intensità)")
        
        scelta_metodo = input("\n- Scegli: ").strip()
        
        if scelta_metodo == "1":
            print("\n- Hai selezionato il metodo: MANUALE")
            print( "-" * 50 + "\n" )
            return "manuale" 
            
        elif scelta_metodo == "2":
            print("\n- Hai selezionato il metodo: AUTOMATIZZATO")
            print( "-" * 50 + "\n" )
            return "automatico" 
            
        else:
            print("\n- [ATTENZIONE] Scelta non valida. Riprova.\n\n")
            
# gestisco l'inserimento multiplo di più prodotti da parte dell'utente (2)
def inserimento_multiplo(contatore_carrello, contatore_automatico):
    
    if contatore_automatico == 0:
        pass
    elif contatore_automatico == 1:
        info_1 = "HAI SELEZIONATO \"1\" MACCHINA AUTOMATICA"
        print(f"{info_1.center(larghezza_terminale)}")
    elif contatore_automatico == 2:
        info_2 = "HAI SELEZIONATO \"2\" MACCHINE AUTOMATICHE"
        print(f"{info_2.center(larghezza_terminale)}")
    else:
        info_3 = "[ATTENZIONE] HAI SELEZIONATO PIÙ DI \"2\" MACCHINE AUTOMATICHE"
        print(f"{info_3.center(larghezza_terminale)}")
        
    if contatore_carrello == 5:
        info_4 = "[ATTENZIONE] HAI RAGGIUNTO IL LIMITE MASSIMO DI PRODOTTI SELEZIONABILI(\"5\")"
        info_5 = "A SEGUITO VERRÀ MOSTRATA L'ESECUZIONE DELL'ORDINE"
        print(f"{info_4.center(larghezza_terminale)}")
        print(f"{info_5.center(larghezza_terminale)}" + "\n")
        return "prosegui"
    
    elif contatore_carrello == 1:
        info_6 = "HAI SELEZIONATO \"1\" PRODOTTO"
        print(f"{info_6.center(larghezza_terminale)}"+ "\n")
        print( "-" * 50 + "\n" )
        print("- Se desideri selezionare un ulteriore prodotto inserisci \"1\"")
        print("- Se hai terminato la tua selezione e desideri continuare inserisci \"2\"")
        
    elif contatore_carrello in range(2, 4): 
        info_7 = f"HAI SELEZIONATO \"{contatore_carrello}\" PRODOTTI"
        print(f"{info_7.center(larghezza_terminale)}" + "\n")
        print( "-" * 50 + "\n" )
        print("- Se desideri selezionare un ulteriore prodotto inserisci \"1\"")
        print("- Se hai terminato la tua selezione e desideri continuare inserisci \"2\"")
        
    elif contatore_carrello == 4:
        info_8 = f"HAI SELEZIONATO \"{contatore_carrello}\" PRODOTTI"
        print(f"{info_8.center(larghezza_terminale)}" + "\n")
        print( "-" * 50 + "\n" )
        print("- Se desideri selezionare un ultimo prodotto inserisci \"1\"")
        print("- Se hai terminato la tua selezione e desideri continuare inserisci \"2\"")
        
    while True:   
        selezione = input("\n- Scegli: ").strip()
        
        if selezione == "1": 
            return "continua"  
        elif selezione == "2":
            print("\n" + "-" * 50)  
            info_9 = "A SEGUITO VERRÀ MOSTRATA L'ESECUZIONE DELL'ORDINE"
            print("\n" + f"{info_9.center(larghezza_terminale)}" + "\n") 
            return "prosegui"
        print("\n" + "-" * 50)
        print("- [ATTENZIONE] SCELTA NON VALIDA. RIPROVA") 
        print("-" * 50) 
        
# generazione processo casuale (3)
def generazione_casuale(categoria_random): 
    
    prodotti_list = list(DATASET_AZIENDA[categoria_random].keys())
    prodotti_casuali = random.choice(prodotti_list)
    quantità_casuale = random.randint(100, 7000) 
    metodo_casuale = random.choice(["manuale", "automatico"])
    
    print("-" * 50)
    print(f"\n- Il prodotto è stato selezionato dalla categoria: {categoria_random}")
    print(f"- Il prodotto selezionato è: {prodotti_casuali}")
    print(f"- Abbiamo selezionato {quantità_casuale} kg di {prodotti_casuali}")
    print(f"- La produzione di {quantità_casuale} kg di {prodotti_casuali} sarà svolta con procedimento {metodo_casuale}")
    print("\n" + "-" * 50 + "\n")
    
    giorni_coltivazione = calcolo_crescita(categoria_random, prodotti_casuali)
    
    if metodo_casuale == "manuale":  
        risorse_random = 5 
        max_giornaliero_fisso = DATASET_AZIENDA[categoria_random][prodotti_casuali]["manuale"]["capacita_giornaliera_singolo"]        
        max_giornaliero_squadra_var = 0 
        
        for operaio in range(risorse_random):
            variazione_operaio = random.uniform(-0.07, 0.07)
            max_giornaliero_squadra_var += max_giornaliero_fisso * (1 + variazione_operaio)
            
        prodotto_kg_minuto = DATASET_AZIENDA[categoria_random][prodotti_casuali]["manuale"]["tempo_raccolta_kg"]   
        ore_totali = round((quantità_casuale * prodotto_kg_minuto) / risorse_random / 60)
        giorni_totali = math.ceil(quantità_casuale / max_giornaliero_squadra_var)
            
    else:
        risorse_random = 1
        prodotto_kg_minuto = DATASET_AZIENDA[categoria_random][prodotti_casuali]["automatico"]["tempo_raccolta_kg"]
        max_giornaliero = DATASET_AZIENDA[categoria_random][prodotti_casuali]["automatico"]["capacita_giornaliera"]        
        ore_totali = round((quantità_casuale * prodotto_kg_minuto) / 60)
        giorni_totali = math.ceil(quantità_casuale / max_giornaliero)
    
    # decido se ha senso aggiungere un giorno di organizzazione    
    if ore_totali >= 8: 
        giorni_organizzazione = 1 
    else:
        giorni_organizzazione = 0
    risultato_giorni_totali = giorni_coltivazione + giorni_totali + giorni_organizzazione
    data_consegna = calcola_data_consegna(risultato_giorni_totali)
    
    if giorni_organizzazione == 1:
        print("\n" + "-" * 50 + "\n")
        print(f"- Per preparare l'ordine di {quantità_casuale} kg ci sono voluti: 1 giorno per l'organizzazione dei macchinari e degli operai, {giorni_coltivazione} giorni di coltivazione e {giorni_totali} giorni di raccolta") 
        print(f"- Abbiamo impiegato per questo singolo ordine circa {ore_totali} ore di lavoro") 
        print("\n" + "-" * 50 + "\n")
    else:
        print("\n" + "-" * 50 + "\n")
        print(f"- Per preparare l'ordine di {quantità_casuale} kg ci sono voluti: {giorni_coltivazione} giorni di coltivazione e {giorni_totali} giorno di raccolta")  
        print(f"- Abbiamo impiegato per questo singolo ordine circa {ore_totali} ora/e di lavoro)")
        print("\n" + "-" * 50 + "\n")
        
    print(f"- IL TUO ORDINE SARÀ PRONTO PER LA SPEDIZIONE: {data_consegna.strftime('%A %d-%B %Y').upper()}")
    print(f"- L'azienda ha impiegato {risultato_giorni_totali} giorni totali")
    print("\n" + "-" * 50)
    
    # spedizione casuale
    residenza_casuale = random.choice(["a Roma", "nella provincia e dintorni di Roma", "in un altra regione italiana al di fuori del Lazio", "fuori dall'Italia"])
    
    titolosped = "--- SPEDIZIONE PRODOTTO ---"
        
    print("\n\n" + f"{titolosped.center(larghezza_terminale)}")
    print("\n\n" + "-" * 50)
    print(f"\n- L'azienda agricola ha sede a Roma")
    print(f"- La tua residenza simulata è: {residenza_casuale}")
    
    if residenza_casuale == "a Roma.":
        data_consegna += datetime.timedelta(days=1) 
        print("\n" + "-" * 50) 
    elif residenza_casuale == "nella provincia e dintorni di Roma": 
        data_consegna += datetime.timedelta(days=random.randint(2, 3))
        print("\n" + "-" * 50)
    elif residenza_casuale == "in un altra regione italiana al di fuori del Lazio":
        data_consegna += datetime.timedelta(days=random.randint(4, 6)) 
        print("\n" + "-" * 50)
    elif residenza_casuale == "fuori dall'Italia":
        print("\n" + "-" * 50)
        print("- [ATTENZIONE] Non si effettuano spedizioni fuori dall'Italia. Consegna simulata a Roma (+1 giorno)")
        print("-" * 50)
        data_consegna += datetime.timedelta(days=1)
   
    risultato_finale_testo = f"IL TUO ORDINE TI VERRÀ CONSEGNATO: {data_consegna.strftime('%A %d-%B %Y').upper()}" 
    print("\n\n" + f"{risultato_finale_testo.center(larghezza_terminale)}")
           
    stampa_schermo = "\nSE VUOI CONTINUARE A RESTARE NEL PROGRAMMA SEGUI LE SEGUENTI INDICAZIONI: \n\n"
    print("\n\n" + "-" * len(stampa_schermo))
    print(stampa_schermo)  
    return

# stampa il risultato all'utente (2)                 
def stampa_finale(carrello_urgenze, giorni_totali_ordine):
    
    lista_ore = []
    
    for prodotto_memorizzato in carrello_urgenze:  
        if prodotto_memorizzato["metodo"] == "manuale":
            risorse = prodotto_memorizzato.get("operai_iniziali", 2)# legge gli operai assegnati all'inizio, se non li trova mette due, per evitare una divisione per zero
            if risorse == 0:
                risorse = 2
        else:
            risorse = 1
        ore_singolo, giorni_raccolta_singolo = calcolo_totale(prodotto_memorizzato["quantità"], prodotto_memorizzato["categoria"], prodotto_memorizzato["nome"], prodotto_memorizzato["metodo"], risorse)
        lista_ore.append(ore_singolo)
        giorni_crescita = prodotto_memorizzato["crescita"]
        print( "\n" + "-" * 50 + "\n" )
        print(f"- Per preparare l'ordine di {prodotto_memorizzato['quantità']} kg di {prodotto_memorizzato['nome']} ci sono voluti {giorni_crescita} giorni di coltivazione e {giorni_raccolta_singolo} di raccolta.")
        print(f"- Abbiamo impiegato per questo singolo ordine circa {ore_singolo} ora/e di lavoro")  
    
    if lista_ore:
        totale_ore_lavoro = max(lista_ore)
    else:
        totale_ore_lavoro = 0
    
    if totale_ore_lavoro >= 8:
        giorni_organizzazione = 1
    else:
        giorni_organizzazione = 0
        
    giorni_complessivi_azienda = giorni_totali_ordine + giorni_organizzazione
    data_termine_prodotto = calcola_data_consegna(giorni_complessivi_azienda)
    
    print("\n" + "-" * 50 + "\n")
    
    if giorni_organizzazione == 1:
        print(f"- NOTA: Il calcolo include 1 giorno per l'organizzazione dei macchinari e degli operai")
        
    print(f"- IL TUO ORDINE COMPLESSIVO SARÀ PRONTO IN AZIENDA IL: {data_termine_prodotto.strftime('%A %d-%B %Y').upper()}")
    print("\n" + "-" * 50 + "\n")
        
    print(f"- L'azienda ha impiegato {giorni_complessivi_azienda} giorni totali per preparare il tuo ordine")     
    print(f"- Corrisponenti a circa {totale_ore_lavoro} ore di lavoro") 
    riusltato_finale = spedizione(data_termine_prodotto) # la restituisce formattata
    
       
    testo_consegna = f"IL TUO ORDINE TI VERRÀ CONSEGNATO: {riusltato_finale}"
    print("\n" + "-" * 50 ) 
    print("\n\n" + testo_consegna.center(larghezza_terminale))
            
    stampa_schermo = "SE VUOI CONTINUARE A RESTARE NEL PROGRAMMA SEGUI LE SEGUENTI INDICAZIONI:"
    print("\n\n" + "-" * len(stampa_schermo))
    print(stampa_schermo)
          
# menu generazione processo casuale, calcolo lineare (3)
def esegui_menu_tre():    
    
    
    riga_titolo = "--------HAI SCELTO DI MANDARE A SCHERMO UNA RAPPRESENTAZIONE DEL PROCESSO IN MANIERA CASUALE--------"
    riga_avviso = "[ATTENZIONE]: Questa rapida simulazione prevede la selezione di unicamente un prodotto prelevato casualmente da quelli disponibili"
    riga_nota = "(Nel piano produttivo reale (Opzione 2) puoi inserire e gestire fino a 5 prodotti in parallelo)"  
                
    print("\n" + f"{riga_titolo.center(larghezza_terminale)}")
    print("\n" + f"{riga_avviso.center(larghezza_terminale)}")
    print(f"{riga_nota.center(larghezza_terminale)}"+ "\n\n")
    
    scelta_categorie = ["ortaggi e verdure","frutta","cereali e semi"]
    categoria_random = random.choice(scelta_categorie)
    generazione_casuale(categoria_random)

# menu richiesta prodotto dall'utente, calcolo parallelo (2)
def esegui_menu_due():
    
    lista_prodotto_non_disp = []
    ordine_carrello = [] 
    contatore_carrello = 1
    contatore_automatico = 0
    
    nom_1 = "--------HAI SCELTO DI RICHIEDERE UN PRODOTTO--------"
    nom_2 = "[ATTENZIONE]: Puoi selezionare un massimo di 5 prodotti"  
            
    print("\n" + f"{nom_1.center(larghezza_terminale)}")
    print(f"{nom_2.center(larghezza_terminale)}" + "\n\n")
    
    
    while True:
         
        categoria_selezionata = visualizza_prodotti()
        
        if not categoria_selezionata: #non interrompe se modifico visualizza_prodotti => se diventasse none
            return
        
        prodotto, quantità, lista_carrello = scelta(categoria_selezionata, lista_prodotto_non_disp, ordine_carrello)    
                     
        print(f"- Hai scelto {quantità} kg di {prodotto}") 
        
        crescita_prodotto = calcolo_crescita(categoria_selezionata, prodotto)
        print ("\n" + "-" * 50)
        print ("\n\n")
        metodo_lavoro = seleziona_metodo_lavoro()
        
        prodotto_corrente = {
            "nome": prodotto,
            "quantità": quantità,
            "categoria":categoria_selezionata,
            "crescita": crescita_prodotto,
            "metodo": metodo_lavoro,
            "priorità": DATASET_AZIENDA[categoria_selezionata][prodotto]["priorità_raccolta"], # perché non è una variabile locale
        }
        lista_carrello.append(prodotto_corrente)
        if metodo_lavoro == "automatico":
            contatore_automatico += 1
        prodotti_multipli = inserimento_multiplo(contatore_carrello, contatore_automatico)
        
        if prodotti_multipli == "continua":
            contatore_carrello += 1
            continue
        elif prodotti_multipli == "prosegui":
            break
        
    carrello_urgenze = sorted(lista_carrello, key=lambda x: x["priorità"], reverse=True)
    distribuisci_operai(carrello_urgenze)
    giorni_totali_ordine = lavoro_parallelo_(carrello_urgenze)
    
    stampa_finale(carrello_urgenze, giorni_totali_ordine)
    
# menu visualizzazione tutti i prodotti dell'azienda (1)
def esegui_menu_uno():
    
    richiesta_visual = "--------HAI SCELTO DI VISUALIZZARE L'ELENCO DEI NOSTRI PRODOTTI--------"
                
    print("\n" + f"{richiesta_visual.center(larghezza_terminale)}")
            
    testo_stampato = " ECCO TUTTI I NOSTRI PRODOTTI: "
    print("\n" + "-" * len(testo_stampato))
    print(testo_stampato)
    print("-" * len(testo_stampato) + "\n")
            
    testo_ortaggi = " ORTAGGI E VERDURE:"
    print("\n\n" + "-" * len(testo_ortaggi))
    print(testo_ortaggi)
    print("-" * len(testo_ortaggi) + "\n")
    for i in DATASET_AZIENDA["ortaggi e verdure"]:
        print(f" - {i.capitalize()}\n")
    print("-" * len(testo_ortaggi))

    print(" FRUTTA:")
    print("-" * len(testo_ortaggi) + "\n")
    for i in DATASET_AZIENDA["frutta"]:
        print(f" - {i.capitalize()}\n")
    print("-" * len(testo_ortaggi))
            
    print(" CEREALI E SEMI:")
    print("-" * len(testo_ortaggi) + "\n")
    for i in DATASET_AZIENDA["cereali e semi"]:
        print(f" - {i.capitalize()}")
                
        
    stampa_schermo = "\nSE VUOI CONTINUARE A RESTARE NEL PROGRAMMA SEGUI LE SEGUENTI INDICAZIONI: \n\n"
    print("\n" + "-" * len(stampa_schermo))
    print(stampa_schermo)
    
# menu di controllo
def menu_principale():
    
    titolo()
    
    while True:
        print("\n- Inserisci \"1\" per visualizzare tutti i prodotti dell'azienda")
        print("- Inserisci \"2\" per richiedere un prodotto")
        print("- Inserisci \"3\" per richiedere una simulazione causale")
        print("- Inserisci \"4\" per uscire")
     
        opzione_menu = input("\n- Scegli: ").strip()

        if opzione_menu == "1":
            esegui_menu_uno()
            
        elif opzione_menu == "2":
            esegui_menu_due()
    
        elif opzione_menu == "3":
            esegui_menu_tre()
        
        elif opzione_menu == "4":
            fine = "USCITA PROGRAMMA"
            print("\n" + f"{fine.center(larghezza_terminale)}" + "\n\n")
            print("GRAZIE PER ESSERE STATO ALL0INTERNO DEL NOSTRO PROGRAMMA")
            print("-" * 50)
            return None 
        
        else:
            print("\n" + "-" * 50)
            print("- [ATTENZIONE] SCELTA NON VALIDA. RIPROVA")
            print("-" * 50)

menu_principale() 