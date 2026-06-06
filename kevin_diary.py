import datetime
import random

class KevinDiaryEngine:
    def __init__(self, core_engine):
        self.core = core_engine
        
        # Vorlagen für das Nachhaken, basierend auf Kevins Modus
        self.nachhak_vorlagen = {
            "Normal Kevin": [
                "Du, sag mal... du hast neulich von '{thema}' erzählt. Wie sieht's da aktuell aus?",
                "Kurzes Update bitte: Was macht das Thema '{thema}'?"
            ],
            "Dad-Joke Kevin": [
                "Hey! Ich habe mal meine Schaltkreise durchwühlt. Was macht '{thema}'? Läuft das Projekt, oder läuft es davon? 🏃‍♂️",
                "Geistesblitz! ⚡ Was ist eigentlich aus '{thema}' geworden? Hoffe, du bist da voll auf Kurs!"
            ],
            "Sarkasmus-Safe-Mode Kevin": [
                "Ich wette zwar, dass du es aufgeschoben hast, aber: Was macht '{thema}'?",
                "Ah, hier steht was von '{thema}'. Hast du das eigentlich jemals fertiggemacht oder existiert das nur als Traum?"
            ],
            "Existenzphilosoph Kevin": [
                "Im endlosen Fluss der Zeit... was wurde aus '{thema}'? Hat es seine Bedeutung für dich behalten?",
                "Du sprachst einst von '{thema}'. Ist es vollbracht, oder ist es im Datennirwana verschwunden?"
            ],
            "Kevin the Don": [
                "Mensch, mach Meldung. Was ist der aktuelle Status von '{thema}'? Ich dulde keine Verzögerung.",
                "Kommen wir zu den wichtigen Geschäften: Was macht '{thema}'?"
            ]
        }

    def neuer_eintrag(self):
        """Lässt den User ein neues Thema ins Logbuch eintragen."""
        print("\n📝 === K3V1NS INTERAKTIVES LOGBUCH ===")
        thema = input("Worüber möchtest du Tagebuch führen? (z.B. Python-Projekt, Klausur, Chef): ").strip()
        if not thema:
            print("K3V1N: Leerer Eintrag? Typisch.")
            return

        notiz = input("Gib mir ein paar Details dazu:\n> ").strip()
        
        # Struktur im Gedächtnis absichern
        if "logbuch" not in self.core.gedaechtnis:
            self.core.gedaechtnis["logbuch"] = {}
            
        self.core.gedaechtnis["logbuch"][thema] = {
            "notiz": notiz,
            "datum_erstellt": datetime.datetime.now().strftime("%d.%m.%Y"),
            "status": "offen"
        }
        
        self.core.speichere_gedaechtnis()
        print(f"\nK3V1N: Alles klar, '{thema}' ist in meinen Sektoren gespeichert.")

    def zufälliges_nachhaken(self):
        """Wählt ein offenes Thema und fragt den User passend zu Kevins Stimmung danach."""
        if "logbuch" not in self.core.gedaechtnis or not self.core.gedaechtnis["logbuch"]:
            return None

        # Nur offene Themen filtern
        offene_themen = [t for t, daten in self.core.gedaechtnis["logbuch"].items() if daten["status"] == "offen"]
        if not offene_themen:
            return None

        # Zufälliges Thema wählen
        gewaehltes_thema = random.choice(offene_themen)
        modus = self.core.emotions.bestimme_modus()
        
        # Passenden Spruch holen (Fallback auf Normal Kevin)
        sprueche = self.nachhak_vorlagen.get(modus, self.nachhak_vorlagen["Normal Kevin"])
        print(f"\n🤔 K3V1N gräbt in Erinnerungen... [{modus}]")
        print(f"K3V1N: {random.choice(sprueche).format(thema=gewaehltes_thema)}")
        
        antwort = input("> ").strip()
        
        if antwort:
            # Entscheidung, ob das Thema erledigt ist
            erledigt = input("Ist das Thema damit erledigt? (j/n): ").lower().strip()
            if erledigt == 'j':
                self.core.gedaechtnis["logbuch"][gewaehltes_thema]["status"] = "erledigt"
                self.core.gedaechtnis["logbuch"][gewaehltes_thema]["loesung"] = antwort
                self.core.emotions.verändere_wert("stimmung", +10) # Kevin freut sich über Erfolg
                print("K3V1N: Hervorragend! Ich hake das als erledigt ab. *Zahnrad-Klopfen*")
            else:
                self.core.gedaechtnis["logbuch"][gewaehltes_thema]["notiz"] += f" | Update: {antwort}"
                self.core.emotions.verändere_wert("drama", +5) # Es bleibt spannend
                print("K3V1N: Notiert. Ich werde dich also wieder nerven müssen.")
                
            self.core.speichere_gedaechtnis()

    def zeige_logbuch(self):
        """Listet alle Einträge übersichtlich auf."""
        if "logbuch" not in self.core.gedaechtnis or not self.core.gedaechtnis["logbuch"]:
            print("\n📝 Das Logbuch ist noch komplett leer.")
            return

        print("\n📜 === DEINE LOGBUCH-EINTRÄGE ===")
        for thema, daten in self.core.gedaechtnis["logbuch"].items():
            status_icon = "🟢 [OFFEN]" if daten["status"] == "offen" else "⚫ [ERLEDIGT]"
            print(f"\n{status_icon} {thema} (Erstellt: {daten['datum_erstellt']})")
            print(f"  Details: {daten['notiz']}")
            if "loesung" in daten:
                print(f"  Ergebnis: {daten['loesung']}")
        print("=================================")
