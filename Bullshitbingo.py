import time
import os

Points = 0

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def header():
    print("="*40)
    print("     Pip-Boy™ 3000 – Büro-Überlebenshilfe")
    print("       (Bullshit Survival Bingo v1.0)")
    print("="*40)

def warte_lade(text="Lade"):
    for i in range(3):
        print(f"{text}{'.' * (i+1)}")
        time.sleep(0.3)

def bullshit_bingo():
    global Points
    clear()
    header()
    warte_lade("Gedankliche Gewaltanalyse läuft")
    ohrfeige = int(input("\n[?] Wie viele mentale Ohrfeigen heute?\n(1 = keine, 10 = alle): "))
    if ohrfeige <= 3:
        print("\n> Gut überlebt, Wanderer.")
        Points += 1
    elif 4 <= ohrfeige <= 6:
        print("\n> Atemnot erkannt. Nimm einen Keks. Mentats helfen nicht immer.")
        Points += 2
    else:
        print("\n> Todeskrallen? Pah. Bürokraten sind schlimmer.")
        Points += 3
    input("\n[ENTER] zum Fortfahren...")

def feierabend_check():
    global Points
    clear()
    header()
    warte_lade("Gefährdungspotential wird berechnet")
    menschen = int(input("\n[?] Wie viele wurden gedanklich ausgeschaltet?\n(1 = Niemand, 10 = Massaker): "))
    if menschen <= 3:
        print("\n> Keine Verluste – keine Munition verbraucht. Nice.")
        Points += 1
    elif 4 <= menschen <= 6:
        print("\n> Raider-Quote erfüllt. Für heute.")
        Points += 2
    else:
        print("\n> Du bist schlimmer als 'ne verseuchte Ghulherde auf Speed.")
        Points += 3
    input("\n[ENTER] zum Fortfahren...")

def alltag_meistern():
    global Points
    clear()
    header()
    warte_lade("Psycho-Widerstandsanalyse läuft")
    kollege_nervt = int(input("\n[?] Wie viele dumme Menschen sind dir heute auf den Sack gegangen?\n(1=Handzahm, 10 = komplette Plage):"))
    if kollege_nervt <= 3:
        print("\n> Nicht schlecht, genieße es!")
        Points += 1
    elif 4 <= kollege_nervt <= 6 :
        print("\n> Tief einatmen ... Du knurrst schon Tische an wie ein Raider auf Psycho-Jet Entzug!")
        Points += 2
    else:
        print(" \n> Falls du den Laden abfackeln willst - Kevin kennt den Weg zur nächsten Tankstelle.")
        Points += 3
    input("\n> [ENTER] zum Fortfahren....")

def alles_nervt():
    global Points
    clear()
    header()

    warte_lade("Reizüberflutungs-Index wird ermittel")
    genervt = int(input("\n> [?]Wie genervt bist du? \n( 1 = War das ein Augenrollen? - 10 = Tische werden angeknurrt):"))
    if genervt <= 3:
        print(" \n> Du bist die Ruhe selbst!")
        Points += 1
    elif 4 <= genervt <= 6:
        print("\n> Ess nen Keks, du bist nicht du selbst wenn du Hunger hast!")
        Points += 2
    else:
        print("\n> Kevin besorgt schon mal Boxhandschuhe und Sandsack.")
        
        print("\n> Du wurdest von so vielen wilden Ghulen umzingelt - kein Wunder, dass du grunzt.")
        Points += 3
    input("\n> [ENTER] zum Fortfahren....")

def auswertung():
    clear()
    header()
    print("\n*** TAGESAUSWERTUNG ***")
    print(f">> Gesamtpunkte: {Points}\n")
    if Points <= 4:
        print("> Du bist der Dalai Lama unter den Wastelandern.")
    elif 5 <= Points <= 7:
        print("> Zwischen Psycho und Paladin – du hältst dich gut.")
    else:
        print("> Vault-Tec stuft dich als „legendär Überlebende“ ein. Bonus-Keks aktiviert.")
    print("\n>>> Vault-Tec dankt für deine Mitarbeit.")

def starte_spiel():
    """Diese Funktion rufen wir später aus Kevins Core auf!"""
    global Points
    Points = 0 # Punkte bei jedem Neustart zurücksetzen!
    clear()
    header()
    input(">> Willkommen zurück, Überlebenskünstler. [ENTER]")
    
    bullshit_bingo()
    feierabend_check()
    alltag_meistern()
    alles_nervt()
    auswertung()

if __name__ == "__main__":
    starte_spiel()
