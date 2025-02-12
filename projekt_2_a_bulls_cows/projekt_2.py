"""
projekt_2.py: druhý projekt do Engeto Online Python Akademie

author: Zuzana Mogyorósi
email: zuzana.mogyorosi@gmail.com
discord: Zuzana M. - zuzanamogyorosi
Popis: Hra Bulls and Cows. Program vygeneruje náhodné 4místné číslo, 
které hráč hádá. Program vyhodnocuje počet bull(s) a cow(s) a upozorňuje na chybný vstup.
Ukládá statistiky počtu pokusů a času hádání.
Hráč má možnost se vzdát a zobrazit správné číslo.
"""


import random
import time
import os
import csv

# Generuje 4 místné číslo s unikátními číslicemi, nezačínající nulou.
def generuj_tajne_cislo():
    cisla = list("123456789")  
    random.shuffle(cisla)
    prvni_cislice = cisla.pop(0)  

    cisla.append("0")  
    random.shuffle(cisla)

    return prvni_cislice + "".join(cisla[:3])


# Ověří, zda hádané číslo splňuje podmínky (4 číslice, žádné duplicity, nezačíná nulou).
def overuje_cisla(tip_cisla):
    chyby = []
    
    if not tip_cisla.isdigit():
        chyby.append("Vstup musí být číslo.")
    if len(tip_cisla) != 4:
        chyby.append("Vstup musí obsahovat přesně 4 číslice.")
    if len(set(tip_cisla)) != 4:
        chyby.append("Číslo nesmí obsahovat duplicity.")
    if tip_cisla.startswith("0"):
        chyby.append("Číslo nesmí začínat nulou.")

    return None if not chyby else " ".join(chyby)


# Spočítá počet bulls a cows.
def spocitej_bulls_a_cows(tajne_cislo, tip_cisla):
    bulls = sum(1 for tajne, tip in zip(tajne_cislo, tip_cisla) if tajne == tip)
    cows = sum(1 for tip in tip_cisla if tip in tajne_cislo) - bulls
    return bulls, cows


# Vrátí správně formulovaný text o počtu bulls a cows.
def vypis_bulls_cows(bulls, cows):
    bull_text = f"{bulls} bull" if bulls == 1 else f"{bulls} bulls"
    cow_text = f"{cows} cow" if cows == 1 else f"{cows} cows"
    return f"{bull_text}, {cow_text}"

# Uloží statistiky hry do souboru ve složce data pro konkrétního hráče.
def uloz_statistiku(jmeno_hrace, pocet_pokusu, celkovy_cas, vzdal_se=False):
    os.makedirs("data", exist_ok=True)
    soubour_path = "data/game_statistics.csv"
    
    hlavicka = ["Jméno hráče", "Pokusy", "Čas (s)", "Vzdal se", "Výsledek"]
    vysledek = "Prohrál" if vzdal_se else "Vyhrál"
    data = [jmeno_hrace, pocet_pokusu, celkovy_cas, "Ano" if vzdal_se else "Ne", vysledek]
    
    soubor_existuje = os.path.exists(soubour_path)

    with open(soubour_path, "a", newline="") as file:
        writer = csv.writer(file)
        if not soubor_existuje:
            writer.writerow(hlavicka)  # Přidá záhlaví jen pokud soubor neexistuje
        writer.writerow(data)
# Hlavní smyčka hry.
def main():
    print("Zdravím!")
    jmeno_hrace = input("Zadej, prosím, své jméno: ").strip()
    print("-" * 91)
    print("Vygeneroval jsem pro tebe náhodné 4 místné číslo. Tvým úkolem je uhádnout toto tajné číslo. \nBulls: Počítá, kolik číslic na stejné pozici odpovídá tajnému číslu. \nCows: Počítá, kolik číslic je obsaženo v tajném čísle, ale není na správné pozici. \n- (odečítá bulls, aby se nepočítaly dvakrát.)")
    print("-" * 91)
    print("Pojďme si zahrát Bulls and Cows!")
    print("Pokud se chceš budeš chtít vzdát, napiš slovo 'konec'.")
    print("Čas se rozběhne až po zadání tvého prvního tipu čísla!")
    print("-" * 55)
    
    tajne_cislo = generuj_tajne_cislo()
    pocet_pokusu = 0
    zacatek_casu = None
    
    while True:
        print("-" * 40)
        tip_cisla = input("Zadej číslo: ")
        if zacatek_casu is None:  
            zacatek_casu = time.time()
        if tip_cisla.lower() == "konec":
            print(f"Správné číslo bylo: {tajne_cislo}")
            konec_casu = time.time()
            uplynuly_cas = round(konec_casu - zacatek_casu, 2)
            print(f"Hra ukončena po {pocet_pokusu} pokusech.")
            print("-" * 40)
            print("-" * 40)
            uloz_statistiku(jmeno_hrace, pocet_pokusu, uplynuly_cas, vzdal_se=True)
            break
        
        validation_error = overuje_cisla(tip_cisla)
        if validation_error:
            print(validation_error)
            continue
        
        pocet_pokusu += 1
        bulls, cows = spocitej_bulls_a_cows(tajne_cislo, tip_cisla)
        print(vypis_bulls_cows(bulls, cows))
        
        if bulls == 4:
            konec_casu = time.time()
            uplynuly_cas = round(konec_casu - zacatek_casu, 2)
            print(f"Správně, {jmeno_hrace} uhodl/a jsi číslo za {pocet_pokusu} pokusů!")
            print(f"Čas: {uplynuly_cas} sekund")
            print("To je úžasné!")
            print("-" * 40)
            print("-" * 40)
            uloz_statistiku(jmeno_hrace, pocet_pokusu, uplynuly_cas)
            break

# Zajistí spuštění kódu pomocí klávesové zkratky control + option + n
if __name__ == "__main__":
    main()
