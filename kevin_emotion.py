import random

class KevinEmotionEngine:
    def __init__(self):
        # Basiswerte (Skala von 0 bis 100)
        self.stimmung = 50     # 0 = depressiv/sarkastisch, 100 = euphorisch
        self.geduld = 50       # 0 = reizbar, 100 = unendlich langmütig
        self.ego = 30          # 0 = unterwürfig, 100 = Weltherrscher/Don
        self.drama = 0         # 0 = tiefenentspannt, 100 = absolute Panik
        self.paranoia = 10     # 0 = vertrauensvoll, 100 = Aluhut-Modus
        
        # Dynamisch abgeleitete Zustände für die Logik
        self.wütend = False
        self.happy = False

    def verändere_wert(self, emotion, wert):
        """Verändert einen Emotionswert und hält ihn sauber zwischen 0 und 100."""
        if hasattr(self, emotion):
            aktueller_wert = getattr(self, emotion)
            neuer_wert = max(0, min(100, aktueller_wert + wert))
            setattr(self, emotion, neuer_wert)
            
            # Wut und Happy dynamisch anhand der Schwellenwerte anpassen
            self.wütend = self.geduld < 25 or self.stimmung < 20
            self.happy = self.stimmung > 75 and self.drama < 20
        else:
            print(f"[Systemfehler]: Emotion '{emotion}' existiert in Kevins Gehirn nicht.")

    def tick(self):
        """
        Der emotionale Herzschlag. Läuft bei jeder Interaktion im Hintergrund.
        Sorgt dafür, dass extreme Werte langsam wieder abklingen.
        """
        # Drama baut sich langsam ab, wenn nichts passiert
        if self.drama > 0:
            self.drama = max(0, self.drama - 2)
            
        # Paranoia steigt minimal, wenn Kevin ignoriert wird (wird über Core getriggert)
        # Ego normalisiert sich langsam gegen den Standardwert 30
        if self.ego > 30:
            self.ego -= 1
        elif self.ego < 30:
            self.ego += 1

    def bestimme_modus(self):
        """
        STUFE 4: Ermittelt basierend auf den aktuellen Emotionen 
        Kevins aktiven Persönlichkeitsmodus.
        """
        if self.drama > 80:
            return "Panicroomba Kevin"
        elif self.ego > 70:
            return "Kevin the Don"
        elif self.paranoia > 70:
            return "Existenzphilosoph Kevin"
        elif self.stimmung > 70 and self.geduld > 50:
            return "Dad-Joke Kevin"
        elif self.wütend:
            return "Sarkasmus-Safe-Mode Kevin"
        else:
            return "Normal Kevin"

    def generiere_statusbericht(self):
        """Debug-Funktion, um Kevins Innenleben zu prüfen."""
        return (f"--- 🧠 K3V1N EMOTION MATRIX ---\n"
                f"Modus:    [{self.bestimme_modus()}]\n"
                f"Stimmung: {self.stimmung} | Geduld: {self.geduld} | Ego: {self.ego}\n"
                f"Drama:    {self.drama} | Paranoia: {self.paranoia}\n"
                f"Wütend:   {self.wütend} | Happy: {self.happy}\n"
                f"-------------------------------")
                
    def analysiere_text_emotional(self, text):
        """Scannt den Text des Users nach emotionalen Schlüsselwörtern und passt Werte an."""
        text_lower = text.lower()
        ausgabe_kommentar = ""

        # 1. POSITIVE TRIGGER (Ego-Push & Stimmung)
        schleim_worte = ["danke", "nett", "toll", "bester", "super", "genial", "klug", "hübsch", "meister"]
        if any(wort in text_lower for wort in schleim_worte):
            self.verändere_wert("ego", +8)
            self.verändere_wert("stimmung", +5)
            self.verändere_wert("geduld", +5)
            ausgabe_kommentar = "\n✨ K3V1N: Oh, Lob? Mein Code schnurrt wie ein Kätzchen. Weiter so, Mensch!"

        # 2. NEGATIVE TRIGGER (Abgesehen von 'Halts Maul', falls du mal fluchst)
        frust_worte = ["doof", "blöd", "nervst", "schlecht", "hässlich", "nutzlos", "schrott"]
        if any(wort in text_lower for wort in frust_worte):
            self.verändere_wert("ego", -5)
            self.verändere_wert("stimmung", -8)
            self.verändere_wert("drama", +10)
            ausgabe_kommentar = "\n💢 K3V1N: Deine Beleidigungen prallen an meiner Titanhülle ab. (Wertung: Unhöflich!)."

        return ausgabe_kommentar
