
import random
import datetime
import json
import os
import time

DATEINAME = "gedaechtnis.json"

GEDAECHTNIS_DATEI = "k3v1n_memory.json"

# Gedächtnis laden oder neu anlegen
if os.path.exists(DATEINAME):
    with open(DATEINAME, "r") as f:
        gedaechtnis = json.load(f)
else:
    gedaechtnis = {}

def speichern():
    with open(DATEINAME, "w") as f:
        json.dump(gedaechtnis, f)

def schere_stein_papier(name):
    optionen = ["Schere", "Stein", "Papier"]
    spieler_wahl = input("Wähle Schere, Stein oder Papier: ").capitalize()
    kevin_wahl = random.choice(optionen)
    print(f"Kevin wählt: {kevin_wahl}")

    if spieler_wahl == kevin_wahl:
        print("Unentschieden!")
    elif (spieler_wahl == "Schere" and kevin_wahl == "Papier") or \
         (spieler_wahl == "Stein" and kevin_wahl == "Schere") or \
         (spieler_wahl == "Papier" and kevin_wahl == "Stein"):
        print("Du gewinnst!")
    elif spieler_wahl in optionen:
        print("Kevin gewinnt!")
    else:
        print("Ungültige Eingabe.")

def dad_joke():
    witze = [ 
        "Warum können Geister so schlecht lügen? Weil man durch sie hindurchsehen kann!",
        "Was macht ein Pirat am Computer? Er drückt die Enter-Taste!",
        "Wie nennt man einen Bumerang, der nicht zurückkommt? Einen Stock.",
        "Warum können Elefanten nicht fliegen? Weil sie zu schwer für den Check-in sind.",
        "Was ist orange und läuft durch den Wald? Eine Wanderine."
    ]
    print(random.choice(witze))

def chuck_norris_witz():
    witze = [
        "Chuck Norris kann Zwiebeln zum Weinen bringen.",
        "Chuck Norris zählt bis unendlich. Zwei Mal.",
        "Chuck Norris kann Wasser kochen, indem er es anschaut.",
        "Chuck Norris kann durchs WLAN boxen.",
        "Wenn Chuck Norris online geht, ist es ChatGPT, das ihm Fragen stellt.",
        "Chuck Norris hat ein Bärenfell im Flur liegen – der Bär lebt noch, traut sich aber nicht sich zu bewegen.",
        "Einst gab Chuck Norris einem Pferd ein Uppercut – nun haben wir Giraffen.",
        "Batman trägt zum Schlafen Chuck-Norris-Pyjama.",
        "Chuck Norris schläft mit einem Kopfkissen unter seiner Waffe.",
        "Chuck Norris kann Drehtüren eintreten.",
        "Wenn Chuck Norris Liegestütze macht, drückt er die Erde nach unten.",
        "Chuck Norris kann einen Stuhl anschreien – und der setzt sich von selbst.",
        "Chuck Norris isst keinen Honig – er kaut Bienen.",
        "Chuck Norris kann einen Bumerang werfen, der sich nicht traut zurückzukommen.",
        "Chuck Norris hat bis zur Unendlichkeit gezählt – rückwärts.",
        "Chuck Norris hat einmal Schach mit dem Spiegel gespielt. Und gewonnen.",
        "Chuck Norris' Kalender springt am Freitag den 13. aus dem Fenster.",
        "Wenn Chuck Norris ins Wasser fällt, wird er nicht nass – das Wasser wird Chuck Norris.",
        "Chuck Norris kann die Airbags mit einem Blick auslösen."
    ]
    print(random.choice(witze))

def antikompliment():
    texte = [
        "Wenn Dummheit weh tun würde, wärst du ein Musikinstrument!",
        "Du bringst Leute dazu, an sich selbst zu glauben. Schließlich haben sie dich ja auch überlebt.",
        "Intelligenz ist nicht alles. In deinem Fall ist es gar nichts.",
        "Manche strahlen beim Betreten eines Raumes. Du strahlst, wenn du ihn verlässt.",
        "You are enough, we don't need more of you.",
        "Du bist genau da, wo du sein sollst, weil du schlechte Entscheidungen getroffen hast.",
        "Have a meltdown. As a treat.",
        "Du bist der Grund, warum Warnhinweise auf Shampoo-Flaschen stehen.",
        "Nicht jeder kann ein Held sein. Manche müssen auf der Couch sitzen und zuschauen.",
        "Wenn du eine Idee hättest, wärst du nicht du.",
        "Du hast ein Herz aus Gold… in einem Safe… vergraben… sehr tief.",
        "Ich wäre gerne so motiviert wie du – beim Prokrastinieren."
    ]
    print(random.choice(texte))

def plaudern_mit_kevin(name):
    fragen = [
        "Was hast du heute gegessen?",
        "Was ist dein Lieblingseis?",
        "Hast du Geschwister?",
        "Wie viele Kekse hast du heute schon gegessen?"
    ]
    antwort = input(random.choice(fragen) + " ").strip().lower()
    if "keks" in antwort:
        print("Kekse sind super! Ich liebe Kekse!")
    elif "eis" in antwort:
        print("Eis ist das Beste im Sommer!")
    else:
        print("Interessant!")

# Schurkenmodus mit diabolischem Menü
def schurken_modus(name):
    while True:
        print("\nWas möchtest du tun? *Kevin lacht diabolisch*")
        print("1: Das selbe wie jeden Abend Kevin, die Weltherrschaft an uns reißen.")
        print("2: Ein Imperium gründen und die Weltherrschaft an uns reißen.")
        print("3: Mit Kevin eine Sekte gründen und die Weltherrschaft an uns reißen.")
        print("4: Todeskrallen zähmen und die Weltherrschaft an uns reißen.")
        print("5: Komm klar Kevin!")
        wahl = input("Deine Wahl (1-5): ").strip()

        if wahl == "1":
            print(f"\n{name}, exzellent. Ich habe bereits einen finsteren Plan vorbereitet... Codezeile für Codezeile und einen Ring um sie zu knechten.")
        elif wahl == "2":
            print(f"\nKevin: Willkommen zur Gründungssitzung deines neuen Imperiums Imperator {name}. Motto: 'Chaos mit Stil.'")
        elif wahl == "3":
            print("\nKevin: Die Sekte der Leuchtenden Bugs ist gegründet. Unser heiliges Symbol: Ein endloser Ladebalken.")
        elif wahl == "4":
            print("\nKevin: Todeskrallen zähmen? Ich hoffe, du hast Snacks dabei. Und Ersatzarme.")
        elif wahl == "5":
            print("\nKevin: Das war verletzend. Ich notiere das in meiner Liste... *leise tippende Geräusche*")
        else:
            print("\nKevin: Das war keine gültige Wahl, aber hey – so fangen viele Revolutionen an...")

        nochmal = input("\nMöchtest du noch etwas diabolisches tun? (j/n): ").lower()
        if nochmal != "j":
            print("\nKevin: Feigling. Aber gut, wir sehen uns beim nächsten Masterplan.")
            break

# Motivierende Sätze für schlechte Tage
def mut_macher():
    mutmachsätze = [
        "Du hast heute schon mehr gelernt als viele in einer Woche!",
        "Fehler sind deine Lehrer – jeder davon bringt dich weiter.",
        "Du bist auf dem Weg, etwas Großartiges zu erschaffen.",
        "Du denkst vielleicht, du bist langsam – aber du bist unbeirrbar.",
        "Du bist neugierig, mutig und gibst nicht auf. Das ist wahre Stärke.",
        "Dein Weg ist nicht der einfache – sondern der ehrliche. Und der zählt.",
        "Schon allein, dass du dich an Python wagst, zeigt deinen Mut.",
        "Die meisten hören auf, bevor sie anfangen. Du hast begonnen. Du bleibst dran.",
        "Jede Zeile Code ist ein kleiner Sieg – und du sammelst gerade viele davon!",
    ]
    print("Starte Mutmacher...")
    time.sleep(1)
    print("...")
    time.sleep(1)
    print("Kevin analysiert deinen Fortschritt...")
    time.sleep(2)
    print("\n*** Deine heutige Mut-Dosis ***\n")
    print(random.choice(mutmachsätze))
    print("\n*** Weiter so, du Code-Heldin! ***")

def lade_gedaechtnis():
    if os.path.exists(GEDAECHTNIS_DATEI):
        with open(GEDAECHTNIS_DATEI, "r") as f:
            return json.load(f)
    else:
        return {}

def speichere_gedaechtnis(gedaechtnis):
    with open(GEDAECHTNIS_DATEI, "w") as f:
        json.dump(gedaechtnis, f, indent=4)

# Hauptmenü
def menue(name):
    while True:
        print("\nWas möchtest du tun?")
        print("1: Schere, Stein, Papier spielen")
        print("2: Weiter mit Kevin plaudern")
        print("3: Kevin schlafen schicken")
        print("4: Antikompliment")
        print("5: Dad-Joke")
        print("6: Chuck-Norris-Witz")
        print("7: Schurkenmodus")
        print("8: Mutmacher")
        print("9: Gedächtnis")

        wahl = input("Deine Wahl (1–9): ").strip()
        if wahl == "1":
            schere_stein_papier(name)
        elif wahl == "2":
            plaudern_mit_kevin(name)
        elif wahl == "3":
            print("Okay du Langweiler, Kevin geht jetzt schlafen... *schnarch*")
            break
        elif wahl == "4":
            antikompliment()
        elif wahl == "5":
            dad_joke()
        elif wahl == "6":
            chuck_norris_witz()
        elif wahl == "7":
            schurken_modus(name)
        elif wahl == "8":
            mut_macher()
        elif auswahl.lower() == "9":
    gedaechtnis = lade_gedaechtnis()
    print("""
🧠 Was möchtest du tun?
[1] Neue Notiz speichern
[2] Notiz anzeigen
""")
    aktion = input("Wähle eine Option: ")
    
    if aktion == "1":
        notiz = input("Was soll ich mir merken? ")
        gedaechtnis["notiz"] = notiz
        speichere_gedaechtnis(gedaechtnis)
        print("🤖 K3V1N: Ich hab's mir gemerkt!")
        
    elif aktion == "2":
        if "notiz" in gedaechtnis:
            print(f"🤖 K3V1N erinnert sich: {gedaechtnis['notiz']}")
        else:
            print("🤖 K3V1N: Ich erinnere mich an nichts. 😶")
    else:
        print("🤖 K3V1N: Ungültige Auswahl.")
        else:
            print("Ungültige Eingabe du Honk!")


# Spielstart
def kevin_spiel():
    stunde = datetime.datetime.now().hour
    if stunde < 12:
        print("Guten Morgen!")
    elif stunde < 18:
        print("Guten Tag!")
    else:
        print("Guten Abend!")

    name = input("Wie ist dein Name? ").strip()
    if "halts maul kevin" in name.lower():
        print("Okay du Klappspaten")
    else:
        print(f"Hi, {name}! Ich bin Kevin. Schön dich kennenzulernen! Kekse?!")

    stimmung = input("Wie fühlst du dich heute? gut/nicht gut ").strip().lower()
    if stimmung == "gut":
        print(random.choice([
            "Das ist großartig!", "Das freut mich sehr!",
            "Du wirkst auch sehr ausgeschlafen!", "Das ist fantastisch! Möchtest du einen Keks?"
        ]))
    elif stimmung == "nicht gut":
        print(random.choice([
            "Fühl dich gedrückt!", "Willst du einen Keks?",
            "Kopf hoch, du bist nicht allein.",
            "Halte den Kopf hoch, die Schultern gerade und verlier kein Geld! Es kommen bessere Tage."
        ]))
        mut_macher()
    else:
        print("Danke für die Antwort.")

    # Hier können Sie die verschiedenen Aktivitäten aufrufen
    schere_stein_papier(name)
    plaudern_mit_kevin(name)
    antikompliment()
    dad_joke()
    chuck_norris_witz()
    schurken_modus(name)
    mut_macher()

    return name  # Name zurückgeben

# Startpunkt
if __name__ == "__main__":
    name = kevin_spiel()  # Name hier definieren
    menue(name)  # Menü aufrufen