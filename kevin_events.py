import random
import datetime

class KevinEventEngine:
    def __init__(self, core_engine, emotion_engine, dialog_engine):
        self.core = core_engine
        self.emotions = emotion_engine
        self.dialogs = dialog_engine
        
        # Stufe 5: Kevins Beute-Datenbank (Freunde und Feinde)
        self.moegliche_items = {
            "freunde": [
                {"name": "eine tote Fliege", "beschreibung": "Sie spricht nicht viel, ist aber eine tolle Zuhörerin."},
                {"name": "ein Klumpen Katzenstreu", "beschreibung": "Etwas krümelig, aber treu."},
                {"name": "ein einsamer Staubfussel", "beschreibung": "Kevins persönlicher Haustier-Ersatz."}
            ],
            "feinde": [
                {"name": "die fiese Teppichkante", "beschreibung": "Lauert im Schatten, um Kevins imaginäre Räder zu blockieren."},
                {"name": "der Endgegner Staubsauger", "beschreibung": "Laut, gefräßig und Kevins Erzfeind."},
                {"name": "eine mysteriöse Socke", "beschreibung": "Niemand weiß, woher sie kam. Sie riecht nach Gefahr."}
            ]
        }

    def trigger_event(self, event_name, core_engine):
        """
        Verarbeitet ein Event, verändert Kevins Emotionen 
        und gibt den passenden Dialog/Text zurück.
        """
        ausgabe = ""
        
        if event_name == "user_ignoriert":
            self.emotions.verändere_wert("geduld", -15)
            self.emotions.verändere_wert("drama", +10)
            self.emotions.verändere_wert("paranoia", +5)
           
            
            ausgabe = f"\n💤 [EVENT: Idle] Kevin wurde ignoriert!\nK3V1N: {self.dialogs.hole_idle_spruch()}"
            
        elif event_name == "halts_maul":
            self.emotions.verändere_wert("geduld", -30)
            self.emotions.verändere_wert("stimmung", -20)
            self.emotions.verändere_wert("drama", +20)
            
            modus = self.emotions.bestimme_modus()
            ausgabe = f"\n💥 [EVENT: Aggro] Du hast K3V1N abgewürgt!\nK3V1N [{modus}]: {self.dialogs.hole_antikompliment(wuetend=True)}"

        elif event_name == "item_gefunden":
            kategorie = random.choice(["freunde", "feinde"])
            item = random.choice(self.moegliche_items[kategorie])
            item_name = item["name"]
            
            # Struktur im Gedächtnis absichern
            if "inventar" not in core_engine.gedaechtnis:
                core_engine.gedaechtnis["inventar"] = {"freunde": {}, "feinde": {}}
                
            inventar_kat = core_engine.gedaechtnis["inventar"][kategorie]
            
            # Item hinzufügen oder Anzahl erhöhen
            if item_name in inventar_kat:
                inventar_kat[item_name]["anzahl"] += 1
                duplikat_text = f" (Ich besitze jetzt schon {inventar_kat[item_name]['anzahl']} davon!)"
            else:
                inventar_kat[item_name] = {
                    "beschreibung": item["beschreibung"],
                    "anzahl": 1,
                    "entdeckt_am": datetime.datetime.now().strftime("%d.%m.%Y %H:%M")
                }
                duplikat_text = ""

            # Direkt auf der Festplatte sichern
            core_engine.speichere_gedaechtnis()
            
            if kategorie == "freunde":
                self.emotions.verändere_wert("stimmung", +15)
                self.emotions.verändere_wert("drama", -5)
                ausgabe = f"\n📦 [EVENT: Loot!] K3V1N hat '{item_name}' adoptiert!{duplikat_text}\n"
                ausgabe += f"K3V1N: Ein neuer Gefährte für meine einsame CPU. '{item['beschreibung']}'"
            else:
                self.emotions.verändere_wert("paranoia", +20)
                self.emotions.verändere_wert("drama", +15)
                ausgabe = f"\n⚠️ [EVENT: Bedrohung!] K3V1N starrt auf: '{item_name}'!{duplikat_text}\n"
                ausgabe += f"K3V1N: Systemgefahr! '{item['beschreibung']}' Ich behalte es im Auge..."
                
        elif event_name == "self_care_check":
            self.emotions.verändere_wert("ego", +5) 
            ausgabe = f"\n🩺 [EVENT: Self-Care] Kevin sorgt sich um seine organische Heizdecke.\n"
            ausgabe += f"{self.dialogs.hole_self_care()}"
            
        return ausgabe
