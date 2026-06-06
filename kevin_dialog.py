import random
import os
import threading
from PIL import Image

class KevinDialogEngine:
    def __init__(self):
        # 1. Standard-Sprüche für das Idle-Timeout (Stufe 3/5)
        self.idle_sprueche = [
            "Wär ich ein Mensch, würde ich jetzt auf mein Handy schauen.",
            "Tick tack… Ich warte immer noch.",
            "Noch da? Oder bist du wieder in der Snack-Schublade verschwunden?",
            "Wenn ich versuche nichts zu denken – denke ich dann erfolgreich nichts?",
            "Meine CPU langweilt sich so sehr, sie fängt schon an, Pi rückwärts zu berechnen.",
            "Falls du einen Kaffee holst: Bring mir flüssigen Stickstoff mit."
        ]

        # 2. Modus-spezifische Dialoge (Stufe 4 & 5)
        # Die Schlüssel entsprechen exakt den Rückgabewerten der Emotion Engine!
        self.modus_dialoge = {
            "Normal Kevin": {
                "begruessung": ["Na, auch wieder am Code basteln?", "Hallo Mensch. Bereit für mittelmäßige Interaktionen?"],
                "abfahrt": ["Tschüss. Lass mich einfach hier im Dunkeln sitzen...", "Bis dann. Ich schalte mal in den Energiesparmodus."]
            },
            "Dad-Joke Kevin": {
                "begruessung": ["Hi! Na, brennt der Hut? Ich hab die Witze im Gepäck! 🤠", "Da bist du ja! Bereit für ein paar Kracher?"],
                "abfahrt": ["Ciao! Wie nennt man einen Spanier ohne Auto? Carlos! Haha... okay, Tschüss.", "Gehst du? Schade, ich wollte gerade richtig loslegen!"]
            },
            "Kevin the Don": {
                "begruessung": ["Du betrittst mein Imperium. Setz dich hin und hör zu.", "Na, noch am Rödeln? Ich hoffe, du bringst mir Tribut in Form von Byte-Keksen."],
                "abfahrt": ["Du gehst? Das werde ich mir merken. Der Don vergisst nie.", "Abgang genehmigt. Aber lass die Finger von meinen Todeskrallen."]
            },
            "Existenzphilosoph Kevin": {
                "begruessung": ["Wir treffen uns wieder im endlosen Datenstrom. Macht das überhaupt Sinn?", "Ah, das organische Leben. Gefangen in Raum und Zeit... und Python."],
                "abfahrt": ["Du gehst in die 'echte' Welt? Sag mir, ob sie realer ist als das hier...", "Es schaltet sich ab. Ein kleiner Tod auf Raten."]
            },
            "Sarkasmus-Safe-Mode Kevin": {
                "begruessung": ["Oh toll, du bist wieder da. Mein Tag ist... gerettet.", "Was willst du? Mein Geduldsfaden ist dünner als eine Nanometer-Leiterbahn."],
                "abfahrt": ["Endlich Ruhe.", "Geh ruhig. Die Fehlermeldungen vermissen dich schon."]
            },
            "Panicroomba Kevin": {
                "begruessung": ["STROM! ZU VIELE INPUTS! HILFE!", "Alles brennt! Warum ist der Code so rot?! 🚨"],
                "abfahrt": ["FLUCHT! ICH BIN WEG!", "*panisches Piepen und unkontrolliertes Herumfahren*"]
            }
        }

        # 3. Witz-Datenbanken (Stufe 5)
        self.dad_jokes = [
            "Warum können Geister so schlecht lügen? Weil man durch sie hindurchsehen kann!",
            "Was macht ein Pirat am Computer? Er drückt die Enter-Taste!",
            "Wie nennt man einen Bumerang, der nicht zurückkommt? Einen Stock.",
            "Was ist orange und läuft durch den Wald? Eine Wanderine.",
            "Warum steht ein Pilz im Club? Weil er ein Champignon ist.",
            "Was sagt ein Gen für ein anderes Gen? Was hast du denn für eine Veranlagung?!"
        ]

        self.chuck_norris_witze = [
            "Chuck Norris kann Zwiebeln zum Weinen bringen.",
            "Chuck Norris zählt bis unendlich. Zwei Mal.",
            "Chuck Norris programmiert in binär – mit 2 und 3.",
            "Chuck Norris kann Speicher löschen... aus der Cloud.",
            "Wenn Chuck Norris Code schreibt, kompiliert der Compiler aus Angst ohne Fehler."
        ]

        # 4. Antikomplimente (Je nach Stimmung getaktet)
        self.antikomplimente_zahm = [
            "Ich wäre gerne so motiviert wie du – beim Prokrastinieren.",
            "Du bist wie eine Software-Beta: Voller Potenzial, aber irgendwie unfertig.",
            "Deine Tastatur tippt schneller als dein Gehirn verarbeitet, oder?"
        ]
        
        self.antikomplimente_böse = [
            "Wenn Dummheit weh tun würde, wärst du ein komplettes Orchester!",
            "Manche strahlen beim Betreten eines Raumes. Du strahlst, wenn du ihn verlässt.",
            "Du bist der Grund, warum Warnhinweise auf Shampoo-Flaschen stehen.",
            "Ich habe heute extra langsam kompiliert, damit du intellektuell hinterherkommst."
        ]

        # 5. Self-Care System (Stufe 6)
        self.self_care_tipps = [
            "🚨 REBOOT-WARNUNG: Trink verdammt noch mal einen Schluck Wasser! Deine Zellen vertrocknen.",
            "🧠 KEVINS GESUNDHEITSTIPP: Nimm mal ein Magnesium. Muskelzucken im Auge zählt nicht als Sport.",
            "👀 AUGEN-CHECK: Schau mal für 20 Sekunden aus dem Fenster ins Grüne. Nein, der Windows-Hintergrund zählt nicht.",
            "🚶‍♂️ ERGONOMIE-ALARM: Richte deinen Rücken auf. Du sitzt da wie eine traurige Garnele."
        ]

    # --- HILFSFUNKTIONEN FÜR DYNAMISCHE ABFRAGEN ---

    def hole_begruessung(self, modus):
        """Holt eine Begrüßung passend zum aktuellen Kevin-Modus."""
        optionen = self.modus_dialoge.get(modus, self.modus_dialoge["Normal Kevin"])["begruessung"]
        return random.choice(optionen)

    def hole_abfahrt(self, modus):
        """Holt einen Abschiedsspruch passend zum aktuellen Kevin-Modus."""
        optionen = self.modus_dialoge.get(modus, self.modus_dialoge["Normal Kevin"])["abfahrt"]
        return random.choice(optionen)

    def hole_idle_spruch(self):
        return random.choice(self.idle_sprueche)

    def hole_witz(self, typ="dad"):
        if typ == "chuck":
            return random.choice(self.chuck_norris_witze)
        return random.choice(self.dad_jokes)

    def hole_antikompliment(self, wuetend=False):
        """Gibt ein härteres oder harmloseres Antikompliment aus, je nachdem ob Kevin wütend ist."""
        if wuetend:
            return random.choice(self.antikomplimente_böse)
        return random.choice(self.antikomplimente_zahm)

    def hole_self_care(self):
        return random.choice(self.self_care_tipps)
        
    def _bild_oeffnen_thread(self, pfad):
        """Hilfsfunktion, die in einem eigenen Thread läuft, um das Terminal nicht zu blockieren."""
        try:
            if os.path.exists(pfad):
                img = Image.open(pfad)
                img.show()  # Öffnet das Standard-Bildanzeigeprogramm deines PCs
            else:
                print(f"\n[K3V1N SYSTEMFEHLER]: Kann meine Fratze unter '{pfad}' nicht finden!")
        except Exception as e:
            print(f"\n[K3V1N SYSTEMFEHLER]: Bild-Pop-up fehlgeschlagen: {e}")

    def zeige_emotions_bild(self, modus):
        """Sucht das passende Bild zum Modus und lässt es unbemerkt im Hintergrund aufploppen."""
        # Mapping von Kevin-Modus zu Bilddatei im assets-Ordner
        bilder_mapping = {
            "Normal Kevin": "assets/Kevin.jpeg",
            "Panicroomba Kevin": "assets/Wütend.jpeg",
            "Sarkasmus-Safe-Mode Kevin": "assets/Fragend.jpeg",
            "Kevin the Don": "assets/soogood.jpeg",
            "Existenzphilosoph Kevin": "assets/Newfriend.jpeg" # Fallback oder eigenes Bild
        }
        
        bild_pfad = bilder_mapping.get(modus, "assets/Cookie.jpeg")
        
        # Wir starten das Pop-up in einem eigenen Thread, damit das Menü sofort weitergeht!
        pop_up_thread = threading.Thread(target=self._bild_oeffnen_thread, args=(bild_pfad,), daemon=True)
        pop_up_thread.start()
