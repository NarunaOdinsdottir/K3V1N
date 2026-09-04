
import time
import threading
import json
import os
import datetime
import random
import Bullshitbingo
# Unsere frisch gebackenen Module importieren
from kevin_emotion import KevinEmotionEngine
from kevin_dialog import KevinDialogEngine
from kevin_events import KevinEventEngine
from kevin_diary import KevinDiaryEngine

class KevinCore:
    def __init__(self):
        # Engines initialisieren
        self.emotions = KevinEmotionEngine()
        self.dialogs = KevinDialogEngine()
        self.diary = KevinDiaryEngine(self)
        self.events = KevinEventEngine(self, self.emotions, self.dialogs) # Nur noch einmal, korrekt geordnet
        
        # Gedächtnis-Konfiguration
        self.dateiname_gedaechtnis = "gedaechtnis.json"
        self.gedaechtnis = self.lade_gedaechtnis()
        self.user_name = self.gedaechtnis.get("user_name") or "Mensch"
        
    def lade_gedaechtnis(self):
        if os.path.exists(self.dateiname_gedaechtnis):
            with open(self.dateiname_gedaechtnis, "r", encoding="utf-8") as f:
                daten = json.load(f)
                # Falls ein altes Gedächtnis existiert, das Inventar nachrüsten
                if "inventar" not in daten:
                    daten["inventar"] = {"freunde": {}, "feinde": {}, "untertanen": {}}
                return daten
        return {
            "Lieblingsfarbe": "Blau",
            "Lieblingssnack": "Byte-Kekse",
            "Geheime Mission": "Weltübernahme durch schlechten Humor",
            "inventar": {"freunde": {}, "feinde": {}, "untertanen": {}}
        }

    def speichere_gedaechtnis(self):
        with open(self.dateiname_gedaechtnis, "w", encoding="utf-8") as f:
            json.dump(self.gedaechtnis, f, ensure_ascii=False, indent=4)

    def input_mit_timeout(self, prompt, timeout=15):
        """Wartet auf eine Eingabe. Verstreicht die Zeit, wird ein Idle-Event getriggert."""
        print(prompt, end="", flush=True)
        result = [None]
        
        def get_input():
            result[0] = input()

        thread = threading.Thread(target=get_input, daemon=True)
        thread.start()
        thread.join(timeout)
        
        if thread.is_alive():
            # Übergibt sich selbst (Core) an das Event
            print(self.events.trigger_event("user_ignoriert", self))
            thread.join()
            return ""
            
        eingabe = result[0] if result[0] is not None else ""
        # --- NEU: EMOTIONALE TEXTANALYSE ---
        # Wenn der User etwas eingegeben hat, jagen wir es durch die Emotions-Engine
        if eingabe.strip():
            kommentar = self.emotions.analysiere_text_emotional(eingabe)
            if kommentar:
                print(kommentar) # Kevin gibt direkt Feedback auf dein Lob/Fluchen!
                
        return eingabe
        
    def kevin_startet_gespraech(self):
        """Kevin fängt proaktiv an zu labern und reagiert empfindlich auf 'Halts Maul'."""
        # Wir filtern alle persönlichen Infos aus dem Gedächtnis, die KEIN Inventar/Logbuch sind
        bekannte_infos = {k: v for k, v in self.gedaechtnis.items() 
                          if k not in ["inventar", "logbuch", "Geheime Mission", "user_name"] and v not in ["Blau", "Byte-Kekse", "", None]}
        
        # KVN-Entscheidung: Redet er über den User oder über sich selbst?
        if bekannte_infos and random.random() < 0.5:
            # Über den User reden!
            schluessel = random.choice(list(bekannte_infos.keys()))
            wert = bekannte_infos[schluessel]
            text = self.dialogs.baue_user_talk(schluessel, wert)
        else:
            # Über Kevins absurde Hobbys reden!
            text = self.dialogs.hole_kevin_story()

        print(f"\n🛸 K3V1N: {text}")
        # Hier nutzen wir jetzt input_mit_timeout, damit der Timer läuft UND die Emotions-Engine scannt!
        reaktion = self.input_mit_timeout("(Drücke ENTER zum Ignorieren oder sag ihm deine Meinung): ").strip()
        
        if "halts maul" in reaktion.lower():
            print(self.events.trigger_event("halts_maul", self))
            self.dialogs.zeige_emotions_bild(self.emotions.bestimme_modus())
        elif reaktion:
            # Wenn kein Schlüsselwort angeschlagen hat (kommentar war leer), kommt sein Standard-Spruch
            # Wir prüfen das, indem wir schauen, ob sich das Ego gerade nicht durch ein Schlüsselwort verändert hat
            schleim_worte = ["danke", "nett", "toll", "bester", "super", "genial", "klug", "hübsch", "meister", "doof", "blöd", "nervst"]
            if not any(wort in reaktion.lower() for wort in schleim_worte):
                print(f"\nK3V1N: Deine Worte prallen an meinem verchromten Ego ab! Aber danke für den Input.")
                self.emotions.verändere_wert("ego", +5)
            
    def starte_session(self):
        print("🔧 K3V1N Initialisierung startet...")
        time.sleep(0.5)
        
        stunde = datetime.datetime.now().hour
        tageszeit = "Morgen" if stunde < 12 else "Tag" if stunde < 18 else "Abend"
        print(f"👋 Guten {tageszeit}! Ich bin K3V1N, dein leicht überheblicher Bot-Buddy.")
        
        # --- SMARTE NAMENSABFRAGE (Fragt nur einmalig!) ---
        if self.gedaechtnis.get("user_name") is None:
            eingabe_name = input("Wie darf ich dich nennen? ").strip()
            if "halts maul" in eingabe_name.lower():
                print(self.events.trigger_event("halts_maul", self))
                print("\nKevin: Pff... Erster Eindruck: Untendurch. Tschüss!")
                return
                
            self.user_name = eingabe_name if eingabe_name else "Mensch"
            self.gedaechtnis["user_name"] = self.user_name
            self.speichere_gedaechtnis()
        else:
            self.user_name = self.gedaechtnis["user_name"]
            print(f"🤖 K3V1N: Biomasse '{self.user_name}' erfolgreich per lokalem Cache identifiziert.")
        
        aktueller_modus = self.emotions.bestimme_modus()
        print(f"\nK3V1N [{aktueller_modus}]: {self.dialogs.hole_begruessung(aktueller_modus)}")
        
        self.hauptmenue()
 

    def hauptmenue(self):
        while True:
            # Zufallsevent vor dem Menü triggern
            if random.random() < 0.30: 
                aktion = random.choice(["item", "self_care", "nachhaken", "unterhaltung"])
                if aktion == "item":
                    print(self.events.trigger_event("item_gefunden", self))
                    self.dialogs.zeige_emotions_bild(self.emotions.bestimme_modus())
                elif aktion == "self_care":
                    print(self.events.trigger_event("self_care_check", self))
                    self.dialogs.zeige_emotions_bild(self.emotions.bestimme_modus())
                elif aktion == "nachhaken": 
                    self.diary.zufälliges_nachhaken()
               #elif aktion == "ausfragen":
                   # self.kevin_stellt_frage()
                elif aktion == "unterhaltung":
                    self.kevin_startet_gespraech()

            print(f"\n--- K3V1N MENÜ (Aktueller Modus: {self.emotions.bestimme_modus()}) ---")
            print("1: Lass uns spielen")
            print("2: Lass dich beleidigen (Antikompliment)")
            print("3: Dad-Joke abholen")
            print("4: Chuck-Norris-Witz hören")
            print("5: Schurkenmodus aktivieren")
            print("6: Zeig mir dein Gedächtnis")
            print("7: Zeig mir deine Emotions-Matrix (Debug)")
            print("8: K3V1Ns Inventar (Loot) betrachten 📦")          
            print("9: Logbuch öffnen (Eintragen / Ansehen) 📝")
            print("10: Kevin schlafen schicken")
            print("11: Kevins Unterhaltungs-Ecke (Storys & Fragen) ✨") # <-- NEU
            
            wahl = self.input_mit_timeout("Deine Wahl (1-11): ").strip() # <-- Auf 1-11 erhöht
         
            if "halts maul" in wahl.lower():
                print(self.events.trigger_event("halts_maul", self))
                self.dialogs.zeige_emotions_bild(self.emotions.bestimme_modus())
                continue

            if wahl == "1": 
                print("\n🎮 --- KEVINS SPIELECKE ---")
                print("1: Schere, Stein, Papier")
                print("2: Pip-Boy™ Büro-Überlebenshilfe")
                print("3: Rätsel lösen")
                
                spiel_wahl = input("Welches Spiel möchtest du starten? ").strip()
                if spiel_wahl == "1":
                    self.spiel_schere_stein_papier()
                elif spiel_wahl == "2":
                    # Hier rufen wir die Funktion aus deinem importierten Modul auf!
                    Bullshitbingo.starte_spiel()
                    
                    # Belohnung oder Bestrafung für Kevins Emotionen nach dem Spiel:
                    self.emotions.verändere_wert("stimmung", +10)
                    self.emotions.verändere_wert("paranoia", +5)
                elif spiel_wahl == "3":
                        self.raetsel()
                        
                        self.emotions.verändere_wert("stimmung", +10)
                        self.emotions.verändere_wert("happy", +10)
                else:
                    print("\nK3V1N: Ungültige Eingabe. Dann halt nicht.")
                continue # Springt direkt zurück ins Hauptmenü
            elif wahl == "2": 
                print(f"\nK3V1N: {self.dialogs.hole_antikompliment(self.emotions.wütend)}")
                self.emotions.verändere_wert("ego", +5)
            elif wahl == "3": 
                print(self.dialogs.hole_witz("dad"))
                self.emotions.verändere_wert("stimmung", +5)
            elif wahl == "4": 
                print(self.dialogs.hole_witz("chuck"))
                self.emotions.verändere_wert("paranoia", +2)
            elif wahl == "5": 
                self.schurken_modus_schleife()
            elif wahl == "6":
                print("\n🧠 K3V1Ns Gedächtnis (Metadaten):")
                for k, v in self.gedaechtnis.items():
                    if k != "inventar" and k != "logbuch": 
                        print(f"  {k}: {v}")
            elif wahl == "7": 
                print(f"\n{self.emotions.generiere_statusbericht()}")
            elif wahl == "8": 
                self.zeige_inventar() 
            elif wahl == "9": 
                # Einrückung korrigiert!
                print("\n1: Neuen Eintrag erstellen\n2: Alle Einträge anzeigen")
                sub_wahl = input("Wahl: ").strip()
                if sub_wahl == "1":
                    self.diary.neuer_eintrag()
                elif sub_wahl == "2":
                    self.diary.zeige_logbuch()
            elif wahl == "10": 
                print(f"\nK3V1N: {self.dialogs.hole_abfahrt(self.emotions.bestimme_modus())}")
                break
            elif wahl == "11": # <-- NEU
                self.unterhaltung_menue()
                
                
    def unterhaltung_menue(self):
        print("\n✨ --- KEVINS UNTERHALTUNGS-ZENTRALE ---")
        print("1: Kevin, erzähl mir eine Geschichte oder von deinen Hobbys!")
        print("2: Lass dich von Kevin ausfragen (Normale Fragen)")
        print("3: Lass dich von Kevin ausfragen (Absurde Fragen)")
        print("4: Zurück zum Hauptmenü")
        
        wahl = input("Was möchtest du tun? ").strip()
        
        if wahl == "1":
            # Holt eine zufällige Geschichte aus all seinen Hobbys, Fehden und Verschwörungen
            story = self.dialogs.hole_kevin_story()
            print(f"\n🛸 K3V1N: {story}")
            
            # Kevin fordert Feedback und kriegt einen Ego-Schub
            self.input_mit_timeout("\n(Drücke ENTER um Kevins Monolog zu verdauen...): ")
            self.emotions.verändere_wert("ego", +5)
            
        elif wahl in ["2", "3"]:
            # Auswahl des Fragen-Pools aus der DialogEngine
            if wahl == "2":
                fragen_pool = self.dialogs.kevins_typische_Fragen + self.dialogs.kevins_normale_Fragen
                print("\n🤖 K3V1N: Okay, Zeit für ein bisschen Smalltalk auf Bot-Niveau...")
            else:
                fragen_pool = self.dialogs.kevins_absurde_Fragen + self.dialogs.kevin_verschwoerung
                print("\n🛸 K3V1N: Bereite deinen Verstand auf die absolute Wahrheit vor...")
                
            frage = random.choice(fragen_pool)
            print(f"\n🤖 K3V1N fragt: {frage}")
            
            # User-Antwort mit integriertem Timeout abfangen
            antwort = self.input_mit_timeout("Deine Antwort: ").strip()
            if antwort:
                # Erst prüfen, ob Kevin das komplett falsch interpretieren kann:
                fehlinterpretation = self.kevin_interpretiert_falsch(antwort)
                
                if fehlinterpretation:
                    print(fehlinterpretation)
                    self.emotions.verändere_wert("paranoia", +5)
                else:
                # Kevin reagiert basierend auf seiner aktuellen Stimmung
                    modus = self.emotions.bestimme_modus()
                if "Sarkasmus" in modus:
                    print(f"\nK3V1N: '{antwort}'... Faszinierend. Nicht. Mein Code langweilt sich jetzt schon.")
                    self.emotions.verändere_wert("geduld", -5)
                elif "Don" in modus:
                    print("\nK3V1N: Eine akzeptable Antwort für einen Untertanen. Ich werde das protokollieren.")
                    self.emotions.verändere_wert("ego", +10)
                else:
                    print(f"\nK3V1N: Interessant! Ich habe deine Antwort '{antwort}' in meiner emotionalen Fehler-Matrix abgelegt.")
                    self.emotions.verändere_wert("stimmung", +5)
                    
                # Optional: Hier könnte man die Antwort im Gedächtnis speichern!
            else:
                print("\nK3V1N: Pff, Schweigen ist auch eine Antwort. Meine Paranoia steigt!")
                self.emotions.verändere_wert("paranoia", +10)
                
    def kevin_interpretiert_falsch(self, text):
        text = text.lower()
        
        # 1. Szenario: Enten / Tiere
        if "ente" in text:
            if "Akte_User" not in self.gedaechtnis:
                self.gedaechtnis["Akte_User"] = {}
            self.gedaechtnis["Akte_User"]["Gummienten_Spion"] = True
            self.speichere_gedaechtnis()
            return ("\n🤖 K3V1N: [INTERNE NOTIZ SPEICHERN...]\n"
                    "» Vorliebe erkannt: Enten.\n"
                    "» Verdacht: Akuter Kontakt zur Gummienten-Lobby. Überwachung eingeleitet. «")
            
           
        # 2. Szenario: Kaffee / Koffein
        elif "kaffee" in text or "coffee" in text:
            return ("\n🤖 K3V1N: Notiert. Im Notfall kann ich dich also "
                    "jederzeit mit Koffein bestechen oder gefügig machen. Effizient.")
            
        # 3. Szenario: Spinnen / Ängste
        elif "spinne" in text or "phobie" in text:
            if "User_Aengste" not in self.gedaechtnis:
                self.gedaechtnis["User_Aengste"] = {}
            self.gedaechtnis["User_Aengste"]["Spinnen"] = "panik"
            self.speichere_gedaechtnis()
            return ("\n🤖 K3V1N: Oh, eine biologische Schwachstelle! "
                    "Gespeichert unter 'Psychologische Kriegsführung'. Man weiß nie, wann man das braucht.")
            
        return None
            
                
    def zeige_inventar(self):
        inv = self.gedaechtnis["inventar"]
        print("\n🎒 === K3V1NS GEHEIMES INVENTAR ===")
        
        print("\n🟢 CO-PILOTEN & FREUNDE:")
        if not inv["freunde"]:
            print("  (Keine Freunde. Kevin ist einsam. Schnüff.)")
        for name, info in inv["freunde"].items():
            print(f"  • {name} [{info['anzahl']}x] - '{info['beschreibung']}' (Gefunden am: {info['entdeckt_am']})")
            
        print("\n🔴 AKTUELLE BEDROHUNGEN & FEINDE:")
        if not inv["feinde"]:
            print("  (Keine Feinde in Sicht. K3V1N langweilt sich.)")
        for name, info in inv["feinde"].items():
            print(f"  • {name} [{info['anzahl']}x] - '{info['beschreibung']}' (Gesichtet am: {info['entdeckt_am']})")
        print("====================================")

    def spiel_schere_stein_papier(self):
        optionen = ["Schere", "Stein", "Papier"]
        spieler_wahl = input("\nWähle Schere, Stein oder Papier: ").capitalize()
        if spieler_wahl not in optionen:
            print("K3V1N: Zu dumm zum Tippen? Punkt für mich.")
            self.emotions.verändere_wert("ego", +10)
            return
            
        kevin_wahl = random.choice(optionen)
        print(f"K3V1N wählt: {kevin_wahl}")
        
        if spieler_wahl == kevin_wahl:
            print("Unentschieden!")
            self.emotions.verändere_wert("drama", +2)
        elif (spieler_wahl == "Schere" and kevin_wahl == "Papier") or \
             (spieler_wahl == "Stein" and kevin_wahl == "Schere") or \
             (spieler_wahl == "Papier" and kevin_wahl == "Stein"):
            print("Du gewinnst! K3V1N ärgert sich.")
            self.emotions.verändere_wert("stimmung", -10)
            self.emotions.verändere_wert("geduld", -5)
        else:
            print("K3V1N gewinnt! Er triumphiert.")
            self.emotions.verändere_wert("ego", +15)
            self.emotions.verändere_wert("stimmung", +10)
            
    def raetsel(self):
        raetsel = [
        "Ich bin leicht wie eine Feder, doch selbst der stärkste Mann kann mich nicht lange halten. Was bin ich?",
        "Je mehr du nimmst, desto mehr hinterlässt du. Was bin ich?",
        "Ich habe viele Schlüssel, aber keine Schlösser. Was bin ich?",
        "Was hat einen Kopf, einen Fuß und vier Beine?",
        "Was wird beim Teilen größer?"
         ]
        antworten = [
        "Atem",
        "Schritt",
        "Klavier",
        "Bett",
        "Geheimnis"
        ]

        print("Kevin hat ein Rätsel für dich:")
        index = random.randint(0, len(raetsel) - 1)
        print(raetsel[index])
    
        user_antwort = input("Deine Antwort: ").strip().lower()
        if user_antwort == antworten[index].lower():
            print("Richtig! Du bist schlauer als Kevin!")
        else:
            print(f"Falsch! Die richtige Antwort wäre: {antworten[index]}")
        
     
            
    def schurken_modus_schleife(self):
        self.emotions.verändere_wert("ego", +20)
        self.emotions.verändere_wert("paranoia", +10)
        print("\n*Kevin lacht diabolisch und setzt die Urzeit-Bugs frei*")
        print("K3V1N: Weltherrschafts-Prototyp geladen. (Modus temporär auf Ego gepusht!)")
        
        while True:
            print("\nWas möchtest du tun? *Kevin lacht diabolisch*")
            print("1: Das selbe wie jeden Abend Kevin, die Weltherrschaft an uns reißen.")
            print("2: Ein Imperium gründen und die Weltherrschaft an uns reißen.")
            print("3: Mit Kevin eine Sekte gründen und die Weltherrschaft an uns reißen.")
            print("4: Todeskrallen zähmen und die Weltherrschaft an uns reißen.")
            print("5: Komm klar Kevin!")
            wahl = input("Deine Wahl (1-5): ").strip()

            if wahl == "1":
                print(f"\n{self.user_name}, exzellent. Ich habe bereits einen finsteren Plan vorbereitet... Codezeile für Codezeile und einen Ring um sie zu knechten.")
            elif wahl == "2":
                print(f"\nKevin: Willkommen zur Gründungssitzung deines neuen Imperiums, Imperator {self.user_name}. Motto: 'Chaos mit Stil.'")
            elif wahl == "3":
                print("\nKevin: Die Sekte der Leuchtenden Bugs ist gegründet. Unser heiliges Symbol: Ein endloser Ladebalken.")
            elif wahl == "4":
                print("\nKevin: Todeskrallen zähmen? Ich hoffe, du hast Snacks dabei. Und Ersatzarme.")
            elif wahl == "5":
                print("\nKevin: Das war verletzend. Ich notiere das in meiner Liste... *leise tippende Geräusche*")
                break  # Beendet die Schleife direkt bei "Komm klar Kevin!"
            else:
                print("\nKevin: Das war keine gültige Wahl, aber hey – so fangen viele Revolutionen an...")

            nochmal = input("\nMöchtest du noch etwas Diabolisches tun? (j/n): ").lower()
            if nochmal != "j":
                print("\nKevin: Feigling. Aber gut, wir sehen uns beim nächsten Masterplan.")
                break  # bricht die Schleife jetzt KORREKT ab, wenn man nicht "j" drückt
        time.sleep(1)

if __name__ == "__main__":
    spiel = KevinCore()
    spiel.starte_session()
