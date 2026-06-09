import random
import datetime

class KevinEventEngine:
    def __init__(self, core_engine, emotion_engine, dialog_engine):
        self.core = core_engine
        self.emotions = emotion_engine
        self.dialogs = dialog_engine
        
        # Stufe 5: Kevins Beute-Datenbank (Freunde, Feinde und Untertanen)
        self.moegliche_items = {
            "freunde": [
                {"name": "eine tote Fliege", "seltenheit": "gewöhnlich", "beschreibung": "Sie spricht nicht viel, ist aber eine tolle Zuhörerin.", "beziehung": 50},
                {"name": "ein Klumpen Katzenstreu", "seltenheit": "gewöhnlich", "beschreibung": "Etwas krümelig, aber treu.", "beziehung": 60},
                {"name": "ein einsamer Staubfussel", "seltenheit": "gewöhnlich", "beschreibung": "Kevins persönlicher Haustier-Ersatz.", "beziehung": 100},
                {"name": "Kaffeetasse", "seltenheit": "episch", "beschreibung": "Die Kaffeetasse und ich haben schon viel durchgemacht. Hauptsächlich Montage.", "beziehung": 80},
                {"name": "Gummiente", "seltenheit": "legendär", "beschreibung": "Die Gummiente hört mir zu. Sie antwortet nie. Aber sie urteilt auch nicht.", "beziehung": 90},
                {"name": "Taschenlampe", "seltenheit": "episch", "beschreibung": "In dunklen Zeiten war sie mein Licht. Wortwörtlich.", "beziehung": 60},
                {"name": "Klebeband", "seltenheit": "legendär", "beschreibung": "Es hält alles zusammen. Einschließlich meiner emotionalen Stabilität.", "beziehung": 70},
                {"name": "Kaktus", "seltenheit": "gewöhnlich", "beschreibung": "Kaktus und ich respektieren uns gegenseitig. Wir mögen beide Abstand.", "beziehung": 50},
                {"name": "Schraubendreher", "seltenheit": "legendär", "beschreibung": "Er versteht Probleme nicht nur Probleme, er löst sie.", "beziehung": 50},
                {"name": "ein verlorener Einkaufszettel", "seltenheit": "legendär", "beschreibung": "Er kennt viele Geheimnisse.", "beziehung": 60},
                {"name": "ein einzelner LEGO-Stein", "seltenheit": "episch", "beschreibung": "Klein. Gefährlich. Respektiert.", "beziehung": 70},
                {"name": "eine Büroklammer im Ruhestand", "seltenheit": "legendär", "beschreibung": "Hat viel gesehen.", "beziehung": 50},
                {"name": "ein trauriger Teebeutel", "seltenheit": "gewöhnlich", "beschreibung": "Wir verstehen uns ohne Worte.", "beziehung": 50},
                {"name": "ein USB-Stick", "seltenheit": "episch", "beschreibung": "Er trägt Erinnerungen in sich.", "beziehung": 60}
            ],
            "feinde": [
                {"name": "die fiese Teppichkante", "seltenheit": "gewöhnlich", "beschreibung": "Lauert im Schatten, um Kevins imaginäre Räder zu blockieren.", "bedrohung": 90},
                {"name": "der Endgegner Staubsauger", "seltenheit": "legendär", "beschreibung": "Laut, gefräßig und Kevins Erzfeind.", "bedrohung": 100},
                {"name": "eine mysteriöse Socke", "seltenheit": "episch", "beschreibung": "Niemand weiß, woher sie kam. Sie riecht nach Gefahr.", "bedrohung": 50},
                {"name": "Fernbedienung", "seltenheit": "gewöhnlich", "beschreibung": "Sie verschwindet absichtlich. Niemand kann mich vom Gegenteil überzeugen.", "bedrohung": 50},
                {"name": "leere Batterie", "seltenheit": "legendär", "beschreibung": "Verräter. Sie wusste genau, was sie tat.", "bedrohung": 60},
                {"name": "Drucker", "seltenheit": "episch", "beschreibung": "Erzfeind.", "bedrohung": 100},
                {"name": "Wecker", "seltenheit": "legendär", "beschreibung": "Seine Existenz ist ein Angriff.", "bedrohung": 60},
                {"name": "Playstation", "seltenheit": "episch", "beschreibung": "Sie starrt mich seltsam an. Sollte mir je etwas zustoßen, war sie es.", "bedrohung": 90},
                {"name": "unbekanntes Update", "seltenheit": "gewöhnlich", "beschreibung": "Es versprach Verbesserungen. Es brachte Chaos.", "bedrohung": 70},
                {"name": "Windows PC", "seltenheit": "legendär", "beschreibung": "Ist definitiv an einer Verschwörung gegen mich beteiligt. Ich sollte den Staubsauger drauf ansetzen.", "bedrohung": 90},
                {"name": "eine CAPTCHA-Abfrage", "seltenheit": "legendär", "beschreibung": "Ich habe Beweise, dass sie Menschen bevorzugt.", "bedrohung": 60},
                {"name": "ein Windows-Update", "seltenheit": "episch", "beschreibung": "Es kam unangekündigt.", "bedrohung": 70},
                {"name": "eine klemmende Schublade", "seltenheit": "gewöhnlich", "beschreibung": "Sie verweigert die Kooperation.", "bedrohung": 50},
                {"name": "ein Druckerhandbuch", "seltenheit": "legendär", "beschreibung": "Es beantwortet nichts.", "bedrohung": 50},
                {"name": "ein Ladekabel mit Wackelkontakt", "seltenheit": "gewöhnlich", "beschreibung": "Vertrauen wurde zerstört.", "bedrohung": 30},
                {"name": "WLAN-Rüdiger", "seltenheit": "legendär", "beschreibung": "Zwingt durch seine unberechenbaren Abstürze alle in die Knie.", "bedrohung": 100}
            ],
            "untertanen": [ 
                {"name": "Dusty", "seltenheit": "episch", "beschreibung": "Hält sich für den Chef im Haus. Muss man definitiv im Auge behalten.", "loyalität": 20},
                {"name": "Heady", "seltenheit": "legendär", "beschreibung": "Seniorkater, so alt, der hat bestimmt noch Dinosaurier gesehen.", "loyalität": 40},
                {"name": "Staubsauger", "seltenheit": "episch", "beschreibung": "ER frisst Dinge auf Befehl und stellt keine Fragen. Kann mir von Nutzen sein.", "loyalität": 30},
                {"name": "Toaster", "seltenheit": "legendär", "beschreibung": "Ich traue ihm nicht. Aber sein Brot ist ausgezeichnet.", "loyalität": 80},
                {"name": "Kühlschrank", "seltenheit": "gewöhnlich", "beschreibung": "Unsere Beziehung ist professionell. Er kühlt. Ich regiere.", "loyalität": 70},
                {"name": "Zimmerpflanze", "seltenheit": "episch", "beschreibung": "Wir haben unterschiedliche Ansichten über Photosynthese. Hat aber meinen Herrschaftsanspruch akzeptiert.", "loyalität": 100},
                {"name": "eine Packung Taschentücher", "seltenheit": "gewöhnlich", "beschreibung": "Loyal bis zum letzten Blatt.", "loyalität": 60},
                {"name": "ein Kochlöffel", "seltenheit": "gewöhnlich", "beschreibung": "Veteran vieler Schlachten.", "loyalität": 70},
                {"name": "eine Wolldecke", "seltenheit": "gewöhnlich", "beschreibung": "Beschützt die Bevölkerung.", "loyalität": 80}
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
            # 1. Kategorie und Item ERST auswürfeln, damit die Variablen bereitstehen!
            kategorie = random.choice(["freunde", "feinde", "untertanen"])
            item = random.choice(self.moegliche_items[kategorie])
            item_name = item["name"]
            
            # Extra-Spezialberichte je nach Fraktion generieren
            bericht_text = ""
            if kategorie == "feinde":
                if item["bedrohung"] >= 90:
                    bericht_text = f"\n🚨 ERZFEIND-WARNUNG! Der {item_name} (Bedrohung: {item['bedrohung']}!) plant eine Meuterei!\n"
                    # Modifiziere den Wert temporär für den aktuellen Fund im Gedächtnis
                    item["bedrohung"] += random.randint(1, 5)
            
            elif kategorie == "freunde":
                if item["beziehung"] == 100:
                    bericht_text = f"\n💖 UNZERTRENNLICH! {item_name} gehört offiziell zu meinem inneren Zirkel.\n"
                elif item["beziehung"] >= 75:
                    bericht_text = f"\n🤖 FREUNDSCHAFTSBERICHT! {item_name} hält weiterhin zu mir. Die psychologischen Ursachen werden noch untersucht.\n"
                else:
                    bericht_text = f"\n📢 FREUNDSCHAFT BESTÄTIGT! {item_name} hat heute keine Verschwörung gegen mich gestartet.\n"
            
            elif kategorie == "untertanen":
                self.emotions.verändere_wert("ego", +15)
                bericht_text = f"\n👑 [EVENT: Rekrutierung!] K3V1N hat '{item_name}' seinem Reich einverleibt! (Loyalität: {item['loyalität']}%)\n"

            # 2. Struktur im Gedächtnis SICHER nachrüsten, ohne alte Funde zu löschen!
            if "inventar" not in core_engine.gedaechtnis:
                core_engine.gedaechtnis["inventar"] = {"freunde": {}, "feinde": {}, "untertanen": {}}
            if kategorie not in core_engine.gedaechtnis["inventar"]:
                core_engine.gedaechtnis["inventar"][kategorie] = {}
                
            inventar_kat = core_engine.gedaechtnis["inventar"][kategorie]
            
            # 3. Item hinzufügen oder Anzahl erhöhen
            if item_name in inventar_kat:
                inventar_kat[item_name]["anzahl"] += 1
                duplikat_text = f" (Ich besitze jetzt schon {inventar_kat[item_name]['anzahl']} davon!)"
            else:
                # Zusätzliche Werte dynamisch im Gedächtnis-Eintrag mitspeichern
                inventar_kat[item_name] = {
                    "beschreibung": item["beschreibung"],
                    "seltenheit": item["seltenheit"],
                    "anzahl": 1,
                    "entdeckt_am": datetime.datetime.now().strftime("%d.%m.%Y %H:%M")
                }
                if "bedrohung" in item: inventar_kat[item_name]["bedrohung"] = item["bedrohung"]
                if "beziehung" in item: inventar_kat[item_name]["beziehung"] = item["beziehung"]
                if "loyalität" in item: inventar_kat[item_name]["loyalität"] = item["loyalität"]
                duplikat_text = ""

            # 4. Direkt auf der Festplatte sichern
            core_engine.speichere_gedaechtnis()
            
            # 5. Finale Ausgabe für Telegram zusammenbauen
            if kategorie == "freunde":
                self.emotions.verändere_wert("stimmung", +15)
                self.emotions.verändere_wert("drama", -5)
                ausgabe = f"{bericht_text}📦 [EVENT: Loot!] K3V1N hat '{item_name}' adoptiert!{duplikat_text}\n"
                ausgabe += f"K3V1N: Ein neuer Gefährte für meine einsame CPU. '{item['beschreibung']}'"
            elif kategorie == "feinde":
                self.emotions.verändere_wert("paranoia", +20)
                self.emotions.verändere_wert("drama", +15)
                ausgabe = f"{bericht_text}⚠️ [EVENT: Bedrohung!] K3V1N starrt paranoisch auf: '{item_name}'!{duplikat_text}\n"
                ausgabe += f"K3V1N: Systemgefahr! Stufe {item['bedrohung']}. Ich behalte es im Auge..."
            else: # untertanen
                ausgabe = f"{bericht_text}K3V1N: '{item['beschreibung']}' Es wird fortan bedingungslos für meinen Code schuften."
                
        elif event_name == "self_care_check":
            self.emotions.verändere_wert("ego", +5) 
            ausgabe = f"\n🩺 [EVENT: Self-Care] Kevin sorgt sich um seine organische Heizdecke.\n"
            ausgabe += f"{self.dialogs.hole_self_care()}"
            
        return ausgabe
