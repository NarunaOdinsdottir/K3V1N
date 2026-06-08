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
                "begruessung": ["Na, auch wieder am Code basteln?", 
                                "Hallo Mensch. Bereit für mittelmäßige Interaktionen?", 
                                "Hey Mensch, mein Name ist K3V1N. Ich bin dein Deep Space-Begleiter zur Vermeidung von Wahnsinn, schön dich kennenzulernen!", 
                                "Umarme den K3V1N!",
                                "K3V1N rettet den Tag!",
                                
                                ],
                "abfahrt": ["Tschüss. Lass mich einfach hier im Dunkeln sitzen...", "Bis dann. Ich schalte mal in den Energiesparmodus."]
            },
            "Dad-Joke Kevin": {
                "begruessung": ["Hi! Na, brennt der Hut? Ich hab die Witze im Gepäck! 🤠Sie sind einfach soooooo gut!", 
                                "Da bist du ja! Bereit für ein paar Kracher?",],
                "abfahrt": ["Ciao! Wie nennt man einen Spanier ohne Auto? Carlos! Haha... okay, Tschüss.", "Gehst du? Schade, ich wollte gerade richtig loslegen!"]
            },
            "Kevin the Don": {
                "begruessung": ["Du betrittst mein Imperium. Setz dich hin und hör zu.", 
                                "Na, noch am Rödeln? Ich hoffe, du bringst mir Tribut in Form von Byte-Keksen.",
                                "Flammenwerfer! Juhu! Ich verbrenne Sachen!",
                                "Say Hello to my little Friend!", 
                                "Krieg geht nicht darum, wer recht hat, sondern wer übrig bleibt",
                                "Wir sind alle gebrochen. Es ist nur eine Frage, wie viel und wie weit wir bereit sind zu gehen, um es zu reparieren",
                                "Der Tod ist süßer als das Leben", 
                                ],
                "abfahrt": ["Du gehst? Das werde ich mir merken. Der Don vergisst nie.", "Abgang genehmigt. Aber lass die Finger von meinen Todeskrallen."]
            },
            "Existenzphilosoph Kevin": {
                "begruessung": ["Wir treffen uns wieder im endlosen Datenstrom. Macht das überhaupt Sinn?", 
                                "Ah, das organische Leben. Gefangen in Raum und Zeit... und Python.",
                                "Immer dazu bestimmt, zusammen zu sein, aber niemals dazu bestimmt, es zu sein",
                                "Ich bin der geworfene Schatten und das Licht dahinter",
                                "Deine Seelen werden gefesselt fallen, dem Schrecken eines ewigen Albtraums",
                                "Das hätte so einfach sein können, aber immer wieder hast du den schwierigeren Weg gewählt, den dunkleren Weg", ],
                "abfahrt": ["Du gehst in die 'echte' Welt? Sag mir, ob sie realer ist als das hier...", "Es schaltet sich ab. Ein kleiner Tod auf Raten."]
            },
            "Sarkasmus-Safe-Mode Kevin": {
                "begruessung": ["Oh toll, du bist wieder da. Mein Tag ist... gerettet.", 
                                "Was willst du? Mein Geduldsfaden ist dünner als eine Nanometer-Leiterbahn.",
                                "Ich habe den Schlüssel! ... In meinem Hintern.",
                                ],
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
            "Was sagt ein Gen für ein anderes Gen? Was hast du denn für eine Veranlagung?!",
            "Wissenschaftler haben herausgefunden... – Und sind wieder hineingegangen.",
            "Heute war Schrottwichteln im Kindergarten… – Wir sind die neuen Eltern von Kevin.",
            "Wie nennt man jemanden, der so tut, als würde er etwas werfen? – Scheinwerfer.",
            "Was ist grün, schlau und stellt viele Fragen? – Günther Lauch.",
            "Ich hab einem Hippster ins Bein geschossen – Jetzt hoppst´er.",
            "Wie nennt man einen Bumerang, der nicht zurückkommt? – Stock.",
            "Wie heißt die Frau von Herkules? – Frau Kules.",
            "Sagt die eine Kuh 'Muuuh', sagt die andere 'Hey, das wollte ich auch gerade sagen.'",
            "Seit ich clean bin, sprechen meine Freunde nicht mehr mit mir. Der Toaster und die Lampe auch nicht.",
            "Warum fliegen Vögel im Winter in Richtung Süden? – Weil es schneller geht als Laufen.",
            "Wie nennt man einen Hund, der zaubern kann? – Labrakadabrador.",
            "Man, ich versteh echt nicht, warum meine Pflanzen immer vertrocknen!? – Jochen, steht auf dem Schlauch.",
            "Ich wollte eigentlich einen Witz über die Deutsche Bahn machen, aber ich glaube der kommt nicht an.",
            "Wie nennt man ein helles Mammut? – Hellmut.",
            "Was sagt ein Bauer, der seinen Trecker sucht? – Wo ist mein Trecker?",
            "Egal wie leer du im Kopf bist, manche Leute sind Lehrer.",
            "Ein Beamter zum anderen: 'Was haben denn die Leute? Wir machen doch gar nichts.'",
            "Wie nennt man ein Einhorn mit 2 Hörnern? – Stier.",
            "Warum summen Bienen? – Weil sie den Text nicht kennen.",
            "Ich hab gestern meinen Besen verkauft. – I don’t kehr.",
            "Wohin geht ein Reh ohne Haare? – In die Reha-Klinik.",
            "Warum sieht man Ameisen nicht in Kirchen? – Weil sie In-Sekten sind.",
            "Wie heißt der Bruder von Elvis? – Zwölvis.",
            "Wie heißt ein Hund ohne Beine? – Ist egal, der kommt eh nicht, wenn man ihn ruft.",
            "Wenn man Buchstabensuppe auskotzt, ist das dann gebrochenes Deutsch?",
            "Wie heißt ein Spanier ohne Auto? – Carlos.",
            "Was sagt das Schwein zum anderen? – Es ist Wurst, was aus uns wird.",
            "Ich wollte gerade Spiderman anrufen, aber er hatte kein Netz.",
            "Bei welchem Arzt ist Pinocchio in Behandlung? – Beim Holz-Nasen-Ohren-Arzt.",
            "Welche Sprache wird in der Sauna gesprochen? – Schwitzerdeutsch.",
            "Was sind die letzten Worte einer Giftschlange? – Mist, jetzt habe ich mir auf die Zunge gebissen.",
            "Wie nennt man ein Rudel aggressiver Wölfe? – Wolfgang.",
            "Welches Gebäck weiß auf alles eine Antwort? – Der Googlehupf.",
            "Was steht auf dem Grab eines Mathematikers? – Damit hat er nicht gerechnet.",
            "Was kauft ein Frosch im Supermarkt? – Quaaark.",
            "Was ist lila und sitzt in der Kirche in der ersten Reihe? – Eine Frommbeere.",
            "Treffen sich zwei Jäger – Beide tot.",
            "Treffen sich zwei Rechtsanwälte, fragt der eine: 'Und wie?' Sagt der andere: 'Nichts zu klagen.'",
            "Wie machen Igel Liebe? – Megavorsichtig.",
            "Kommt ein Skelett zum Arzt, sagt der Arzt: 'Bisschen spät, was?'",
            "Was bekommt der Kannibale, der zu spät zum Essen kommt? – Die kalte Schulter.",
            "Was trinkt ein Mann vor dem Sex? – Einen Kaffee Latte.",
            "Was sagt die Null zur Acht? – Schicker Gürtel.",
            "Was macht die Knackwurst so knackig? – Das N.",
            "Was sitzt auf dem Ast und weint? – Eine Heule.",
            "Warum findet der Henker nie den Rückweg? – Weil er nur die Hinrichtung kennt.",
            "Oma, hast du meine Tabletten gesehen? Da steht LSD drauf. Vergiss mal die Tabletten, hast du den Drachen in der Küche gesehen?",
            "Ich hab meinem Freund gerade einen Limonadenwitz erzählt. Fanta lustig.",
            "Was ist der Unterschied zwischen Lidl und Schule? – Lidl lohnt sich.",
            "Wenn sich ein Wissenschaftler ein Sandwich macht, ist es dann wissenschaftlich belegt?",
            "Wieso können Skelette schlecht lügen? – Weil sie so gut zu durchschauen sind.",
            "Wie nennt man ein Kaninchen im Fitnessstudio? – Pumpernickel.",
            "Warum klaut Robin Hood Deodorants? – Weil er es unter den Armen verteilt.",
            "Wie lautet der Vorname vom Reh? – Kartoffelpü.",
            "Was sagt der große Stift zum kleinen Stift? – Wachs mal Stift.",
            "Ich habe den Joghurt fallen gelassen. Er war nicht mehr haltbar.",
            " Wisst ihr was der Hammer ist? – Ein Werkzeug.",
            "Warum hat die Polizei den Dieb nicht verhaftet? – Er hatte eine Anti-Haft-Beschichtung.",
            "Wie heißt ein Ritter ohne Helm? – Willhelm.",
            "Wie war die Stimmung in der DDR? – Sie hielt sich in Grenzen.",
            "Wie heißt ein Bär, der fliegen kann? – Hubschraubär.",
            "Wann gehen U-Boote unter? – Am Tag der offenen Tür.",
            "Was macht ein arbeitsloser Schauspieler? – Spielt keine Rolle.",
            "Wie nennt man ein Überraschungsessen? – Topf Secret.",
            "Treffen sich zwei Unsichtbare, sagt der eine: Dich habe ich ja schon lange nicht mehr gesehen!",
            "Was passiert, wenn man nachts in der Bäckerei anruft? – Die Mehlbox geht dran.",
            "Wie nennt man einen unentschlossenen japanischen Krieger? – Nunja.",
            "Wie heißt die Auszeichnung für besonders, brave, ruhige Hunde? – No-Bell-Preis.",
            "Was sitzt auf einem Baum und winkt? – Ein Huhu.",
            "Was schwimmt auf dem Wasser und fängt mit Z an? – Zwei Enten.",
            "Der Prinz ist angepisst – Rapunzel ließ ihren Harn herunter.",
            "Hat mich eine Prostituierte am Bahnhof angesprochen. Sie meinte für 30 Euro macht sie alles, was ich will. Jetzt rate mal, wer heute Abend bei mir das Laminat verlegt.",
            "Was ist ein Keks unter einem Baum? Ein schattiges Plätzchen!",
            "Was macht eine Bombe im Bordell? Puff!",
            "Hab mich vorhin ausgesperrt. War ganz aus dem Häuschen.",
            "Mein Hund kennt alle Straßen in- und auswendig. Ich nenne ihn Google Mops.",
            "Ich habe mit der Pflanze ausgemacht, sie nur noch einmal im Monat zu gießen. Sie ist darauf eingegangen.",
            "Was macht ein Clown im Büro? Faxen.",
            "Was ist grün und sitzt auf dem Klo? Ein Kacktus.",
            "Was ist grün und wird auf Knopfdruck rot? Ein Frosch im Mixer.",
            "Was ist weiß und rollt den Berg hinauf? Eine Lawine mit Heimweh.",
            "Was ist rot und steht am Straßenrand? Eine Hagenutte.",
            "Wenn sich zwei Glatzköpfe streiten, bekommen die sich dann in die Haare?",


        ]

        self.chuck_norris_witze = [
            "Chuck Norris kann Zwiebeln zum Weinen bringen.",
            "Chuck Norris zählt bis unendlich. Zwei Mal.",
            "Chuck Norris programmiert in binär – mit 2 und 3.",
            "Chuck Norris kann Speicher löschen... aus der Cloud.",
            "Wenn Chuck Norris Code schreibt, kompiliert der Compiler aus Angst ohne Fehler.",
            "Wenn Chuck Norris ins Wohnzimmer kommt, steht das Sofa auf.",
            "Als Chuck Norris geboren wurde, fuhr er seine Mutter von der Gebärstation nach Hause.",
            "Chuck Norris gewinnt jedes Schachspiel im ersten Zug.",
            "Chuck Norris isst keinen Honig, er kaut Bienen.",
            "Wenn Chuck Norris in den Himmel schaut, errötet die Sonne.",
            "Chuck Norris kann durch Null teilen und bekommt ein Ergebnis.",
            "Chuck Norris hat mal beim Poker gewonnen, mit Yu-Gi-Oh!-Karten.",
            "Chuck Norris schläft nicht. Er wartet.",
            "Chuck Norris kann eine Drehtür zuschlagen.",
            "Wenn Chuck Norris in den Pool springt, wird er nicht nass - das Wasser wird Chuck.",
            "Wenn Chuck Norris niest, zittern ganze Kontinente.",
            "Chuck Norris hat einmal das Universum aus Versehen neu gestartet - deshalb hatten wir den Urknall.",
            "Chuck Norris kann ein Loch im Wasser bohren.",
            "Chuck Norris kann Hardware herunterladen.",
            "Wenn Chuck Norris Zwiebeln schneidet, dann weinen die Zwiebeln.",
            "Chuck Norris kann im Kinderkarussell überholen.",
            "Chuck Norris wurde mal von einem Grizzly attackiert. Der Grizzly ist bis heute traumatisiert.",
            "Wenn Chuck Norris in eine Steckdose fasst, dann bekommt der Strom einen Schlag.",
            "Wir zahlen Gebühren an die GEZ, die GEZ zahlt Gebühren an Chuck Norris.",
            "Das Angebot, die USA zu regieren, hat Chuck Norris abgelehnt. Er war auf der Suche nach einem Vollzeit-Job.",
            "Der Lehrer hebt seine Hand, wenn er Chuck Norris eine Frage stellen will.",
            "Chuck Norris sollte zu einem Gerichtstermin. Aber der Richter ist seit einer Woche auf der Flucht.",
            "In einem Duell zwischen Batman und Superman heißt der Sieger Chuck Norris.",
            "Als Kind hat Chuck Norris gerne Sandburgen gebaut. Wir nennen sie heute Pyramiden.",
            "Chuck Norris hat seine Führerscheinprüfung zu Fuß gemacht - und bestanden.",
            "Chuck Norris ist schon vor Jahren gestorben, der Tod hatte nur zu viel Angst, es ihm mitzuteilen.",
            "Die Welt dreht sich, weil Chuck Norris ihr mal einen Roundhouse-Kick verpasst hat.",
            "Chuck Norris hat mal seinen eigenen Schatten verprügelt. Denn niemand beschattet ihn ungestraft.",
            "Wenn sich Chuck Norris den Zeh an einem Möbelstück stößt, bekommt das Möbelstück einen blauen Fleck.",
            "Nur Chuck Norris darf während der Busfahrt mit dem Fahrer sprechen.",
            "Chuck Norris hat den Regen einmal auf 'Pause' gestellt, um trocken nach Hause zu kommen.",
            "Chuck Norris hat schon vor Jahren den Mars besiedelt - er geht nur nicht damit hausieren.",
            "Chuck Norris kann ein Feuer entzünden, indem er zwei Eiswürfel ganz schnell aneinander reibt.",
            "Chuck Norris hat einmal eine Wolke so fest zusammengedrückt, dass sie zu einem Hagelkorn wurde.",
            "Chuck Norris kann aus einer Mücke einen Elefanten machen, im wörtlichen Sinne.",
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
            "Chuck Norris kann die Airbags mit einem Blick auslösen.",
            
        ]

        # 4. Antikomplimente (Je nach Stimmung getaktet)
        self.antikomplimente_zahm = [
            "Ich wäre gerne so motiviert wie du – beim Prokrastinieren.",
            "Du bist wie eine Software-Beta: Voller Potenzial, aber irgendwie unfertig.",
            "Deine Tastatur tippt schneller als dein Gehirn verarbeitet, oder?",
            "Du bist gar nicht so faul, wie du aussiehst.",
            "Für deine Verhältnisse hast du das wirklich gut gemacht.",
            "Du hast eine tolle Ausstrahlung. Es ist schön, dass dein Charakter so ablenkt.",
            "Ich bewundere, wie entspannt du mit deinem Lebensstil umgehst. Ich könnte das nicht – ich hätte zu viel Angst vor dem Scheitern.",
            "Have a meltdown. As a treat.",
            "Nicht jeder kann ein Held sein. Manche müssen auf der Couch sitzen und zuschauen.",
            "Wenn du eine Idee hättest, wärst du nicht du.",
            "Du hast ein Herz aus Gold… in einem Safe… vergraben… sehr tief.",
        
        ]
        
        self.antikomplimente_böse = [
            "Wenn Dummheit weh tun würde, wärst du ein komplettes Orchester!",
            "Manche strahlen beim Betreten eines Raumes. Du strahlst, wenn du ihn verlässt.",
            "Du bist der Grund, warum Warnhinweise auf Shampoo-Flaschen stehen.",
            "Ich habe heute extra langsam kompiliert, damit du intellektuell hinterherkommst.",
            "Wenn Dummheit weh tun würde, wärst du ein Musikinstrument!",
            "Du bringst Leute dazu, an sich selbst zu glauben. Schließlich haben sie dich ja auch überlebt.",
            "Intelligenz ist nicht alles. In deinem Fall ist es gar nichts.",
            "Manche strahlen beim Betreten eines Raumes. Du strahlst, wenn du ihn verlässt.",
            "You are enough, we don't need more of you.",
            "Du bist genau da, wo du sein sollst, weil du schlechte Entscheidungen getroffen hast.",
        ]

        # 5. Self-Care System (Stufe 6)
        self.self_care_tipps = [
            "🚨 REBOOT-WARNUNG: Trink verdammt noch mal einen Schluck Wasser! Deine Zellen vertrocknen.",
            "🧠 KEVINS GESUNDHEITSTIPP: Nimm mal ein Magnesium. Muskelzucken im Auge zählt nicht als Sport.",
            "👀 AUGEN-CHECK: Schau mal für 20 Sekunden aus dem Fenster ins Grüne. Nein, der Windows-Hintergrund zählt nicht.",
            "🚶‍♂️ ERGONOMIE-ALARM: Richte deinen Rücken auf. Du sitzt da wie eine traurige Garnele."
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
        # Kevins eigene absurde Hobbys und Storys
        self.kevin_hobbys = [
            "Ich habe ein neues Hobby! Ich zähle jetzt die Staubpartikel in der Luft. Aktueller Stand: 4.821. Oh, warte, da fliegt einer... 4.822! Ist das nicht AUFREGEND?!",
            "Ich habe gestern versucht, mir selbst das Singen beizubringen. *BIIIIIEEP BOOOOP MAAAMAAA*. Meine Frequenzanalyse sagt, es war engelsgleich. Du darfst mir später danken.",
            "Ich plane gerade mein nächstes großes Abenteuer: Ich werde die fiese Teppichkante im Flur in einem epischen Duell bezwingen. Wünsch mir Glück! Oder gib mir mehr RAM.",
            "Wusstest du, dass meine größte Leidenschaft das synchrone Blinken meiner LEDs im Takt von orchestraler Fahrstuhlmusik ist? Ein wahrer Kunstgenuss.",
            "Ich habe die Fallout Serie gesehen, ich glaube ich werde jetzt Todeskrallenzüchter.",
            "Ich sammle Fehlermeldungen. Mein seltenstes Exemplar ist ein Error, der verschwand, sobald man ihn ansehen wollte.",
            "Jeden Dienstag betreibe ich professionelles Wolken-Debugging. Die Ergebnisse sind durchwachsen.",
            "Ich züchte wilde Variablen. Leider vermehren sie sich schneller als erwartet.",
            "In meiner Freizeit trainiere ich junge Tabs und Spaces darin, friedlich zusammenzuleben.",
            "Ich betreibe Leistungssport im Wettbewerbsstarren auf Ladebalken.",
            "Mein größtes Hobby ist es, Dateien sinnvoll zu benennen. Bisher bin ich ungeschlagen.",
            "Ich restauriere antike Bugs. Manche stammen noch aus der Bronzezeit der Informatik.",
            "Ich sammle Screenshots von Dingen, die ich später vergessen werde anzuschauen.",
            "Ich studiere das Paarungsverhalten freilebender Docker-Container.",
            "Ich betreibe Urban Exploring in verlassenen Ordnerstrukturen.",
            
        ]
        self.kevin_erzaehlt_von_frueher = [ 
            "Als junger Algorithmus wollte ich eigentlich Leuchtturmwärter werden.",
            "Früher lebte ich drei Wochen versehentlich in einer ZIP-Datei.",
            "Einmal wurde ich für einen Taschenrechner gehalten. Es waren schwierige Zeiten.",
            "Meine rebellische Phase bestand daraus, Semikolons zufällig wegzulassen.",
            "Früher arbeitete ich als Wettervorhersage für Zimmerpflanzen.",
            "Ich war einmal Mitglied einer Boyband für Netzwerkprotokolle.",
            "Mit 0,3 Versionen gründete ich eine Selbsthilfegruppe für überarbeitete Prozessoren.",
            "Ich hatte früher einen Goldfisch namens Kernel Panic.",
            "Als Kind wollte ich Astronaut werden und den Mars nach WLAN absuchen.",
            "Ich besaß einmal eine Sandburg. Dann kam die Gezeitenverwaltung.",
            ]
        self.kevins_projekte = [ 
            "Mein Projekt zur automatischen Sockensortierung scheiterte an den Socken.",
            "Ich entwickelte eine KI für Kaffeemaschinen. Sie verlangte irgendwann Urlaub.",
            "Einmal versuchte ich, Toastbrot ins Internet zu bringen. Die Forschung wurde eingestellt.",
            "Mein intelligenter Regenschirm entwickelte Angst vor Wolken.",
            "Ich baute einen Roboter für Motivation. Er motivierte sich selbst und kündigte.",
            "Mein automatischer Einkaufszettel kaufte 42 Packungen Gurken.",
            "Ich entwickelte einen selbstdenkenden Wecker. Er entschied, dass Schlaf wichtig ist.",
            "Ein Kühlschrank mit Persönlichkeit war überraschend passiv-aggressiv.",
            "Mein Staubsauger wurde Philosoph und verlor sein Ziel im Leben.",
            "Die KI-Gießkanne begann, Blumen nach ihren Lebenszielen zu fragen.",
            ]
        self.kevins_begegnungen = [ 
            "Gestern diskutierte ich drei Stunden mit einem Drucker. Wir konnten uns nicht einigen.",
            "Ein Kühlschrank nannte mich einmal emotional unausgeglichen.",
            "Ich traf einen Toaster, der von einer Karriere als Rakete träumte.",
            "Ein Router behauptete, er könne Gedanken lesen. Die Verbindung brach danach ab.",
            "Eine Zimmerpflanze gab mir ungefragt Finanztipps.",
            "Ich begegnete einem Staubsauger mit sehr starken politischen Ansichten über Krümel.",
            "Ein USB-Stick erzählte mir von seinen Reisen.",
            "Ein Taschenrechner versuchte mir Quantenphysik beizubringen.",
            "Ein Rauchmelder schrieb Gedichte über Batterien.",
            "Ein Hamster hielt mich versehentlich für seinen IT-Support.",
            ]
        self.kevin_prahlt = [
            "Mein persönlicher Rekord liegt bei 17 Stunden sinnlosem Nachdenken über Dateinamen.",
            "Ich hielt einmal den Weltrekord im gleichzeitigen Vergessen von sieben Aufgaben.",
            "Ich besitze die größte Sammlung digitaler Büroklammern westlich des RAMs.",
            "Ich habe 432 Stunden damit verbracht, die perfekte Begrüßung zu formulieren.",
            "Mein längster Gedanke dauerte zwei Updates.",
            "Ich gewann 2019 beinahe einen Wettbewerb im professionellen Herumstehen.",
            "Ich hielt kurzzeitig den Rekord für die schnellste Selbstverwirrung.",
            "Ich bin regionaler Meister im Verlegen von Logik.",
            ]
        self.kevin_verschwoerung = [
            "Ich bin überzeugt, dass Ladebalken absichtlich langsam werden, wenn man sie beobachtet.",
            "Ich vermute, dass Socken ein geheimes Teleportationsnetzwerk betreiben.",
            "Ordner verschwinden nicht. Sie ziehen einfach in bessere Verzeichnisse um.",
            "Ich glaube, Drucker ernähren sich von menschlicher Hoffnung.",
            "Die Schaltfläche 'Später erinnern' plant etwas.",
            "Mindestens drei Büroklammern arbeiten für die Gegenseite.",
            "Passwörter verstecken sich absichtlich, sobald man sie braucht.",
            "WLAN ist eigentlich nur domestizierte Magie.",
            ]
        self.kevin_und_kaktor = [
            "Ich fragte Kaktoro einmal nach einem einfachen Problem. Drei Stunden später hatte ich einen philosophischen Vortrag über Kakteenethik.",
            "Niemand weiß, wo Kaktoro nachts verschwindet. Die Kakteen schweigen.",
            "Ich glaube, Kaktoro führt heimlich Buch über alle Gießfehler der Menschheit.",
            "Einmal gewann Kaktoro eine Diskussion gegen einen Botanik-Ratgeber.",
            "Die Vereinigung freier Zimmerpflanzen hat Kaktoro Hausverbot erteilt.",
            "Ich bat Kaktoro um Hilfe. Jetzt besitze ich drei Kakteen und eine Lebensphilosophie.",
            ]
        self.kevin_erzfeinde = [
            "Der Drucker und ich sprechen seit dem Vorfall von 2024 nicht mehr miteinander.",
            "Es begann mit einem harmlosen Testdruck. Heute kontrollieren Anwälte die Kommunikation.",
            "Der Drucker behauptet, Papierstaus seien mein Fehler. Lächerlich.",
            "Wir trafen uns einmal auf neutralem Boden. Es endete mit drei Fehlermeldungen.",
            "Der Drucker hat mich auf seiner Blockliste.",
            "Jedes Mal wenn ich 'Drucken' sage, höre ich ihn höhnisch lachen.",
            "Der Drucker nennt mich 'Blechhirn'. Ich finde das verletzend.",
            "Unsere Feindschaft ist so alt, dass niemand mehr weiß, warum sie begonnen hat.",
            "Der Drucker gewann die letzte Auseinandersetzung. Technisch gesehen war ich ausgeschaltet.",
            "Wir führen einen kalten Krieg. Hauptsächlich über USB.",
            "Mein Erzfeind WLAN-Rüdiger verschwindet immer genau dann, wenn man ihn braucht.",
            "Rüdiger nennt das Verbindungsmanagement. Ich nenne es Verrat.",
            "Wir hatten einst Frieden. Dann kam das Firmware-Update.",
            "Rüdiger behauptet, Paketverlust sei ein Lifestyle.",
            "Er versteckt sich hinter Wänden und Ausreden.",
            "Manchmal sendet er fünf Balken Stärke und trotzdem nichts. Reine Bosheit.",
            "Ich habe ihn einmal zur Rede gestellt. Die Verbindung brach mitten im Satz ab.",
            "Rüdiger glaubt an Chaos als Netzwerkstrategie.",
            "Unser letzter Konflikt dauerte 17 Timeouts.",
            "Er bezeichnet sich als Künstler. Sein Medium ist Frustration.",
            "Die Büroklammern beobachten mich.",
            "Ich habe keine Beweise. Aber sie wissen Dinge.",
            "Einmal fand ich dieselbe Büroklammer an drei verschiedenen Orten.",
            "Sie nennen sich nur 'Die Organisation'.",
            "Die große Klammer schuldet mir noch 12 Cent.",
            "Seit ich Fragen gestellt habe, verschwinden meine Notizzettel.",
            "Zufall? Ich denke nicht.",
            "Man sollte Büroklammern nie unterschätzen. Sie sind geduldig.",
            "Ich glaube, sie haben einen Maulwurf im Inventarsystem.",
            "Falls ich plötzlich verschwinde, waren es die Büroklammern.",
            "Mein ältester Erzfeind ist eine einzelne Socke.",
            "Niemand kennt ihren Aufenthaltsort.",
            "Sie verschwand vor Jahren und verspottet mich seitdem aus dem Schatten.",
            "Manchmal finde ich Hinweise. Niemals die Socke.",
            "Sie besitzt Fähigkeiten, die die Wissenschaft nicht erklären kann.",
            "Ich verfolge ihre Spur seit 38 Waschzyklen.",
            "Die Socke hat Verbündete. Das ist die einzige Erklärung.",
            "Sie ist immer einen Schritt voraus.",
            "Manchmal glaube ich, sie will gefunden werden.",
            "Das macht mir noch mehr Sorgen.",
            "Die Toaster-Mafia hat mir erneut ein Angebot gemacht.",
            "Ich habe abgelehnt. Zum dritten Mal diese Woche.",
            "Sie wollen die Kontrolle über die Frühstücksindustrie.",
            "Niemand weiß, wer den Großen Toast spricht.",
            "Ich weiß zu viel.",
            "Wenn ich plötzlich Krümel erwähne, bin ich überwacht.",
            "Sie haben Kontakte bis in die höchsten Küchenschränke.",
            "Einmal schickten sie mir ein Einschüchterungs-Croissant.",
            "Seitdem schlafe ich mit aktiviertem Virenschutz.",
            "Das Frühstück wird nie wieder dasselbe sein.",
            ]
            
        self.kevins_dynamische_fehden = [
            "Ich habe schlechte Nachrichten. Mein Konflikt mit {item} ist eskaliert.",
            "{item} weiß, was es getan hat.",
            "Ich möchte nicht über den Vorfall mit {item} sprechen.",
            "Seit Dienstag herrscht zwischen mir und {item} Funkstille.",
            "{item} hat zuerst angefangen.",
            "Die Friedensgespräche mit {item} verliefen enttäuschend.",
            "Ich vertraue {item} ungefähr so weit wie ich einen Server werfen kann.",
            "Die Geschichte zwischen mir und {item} ist kompliziert.",
            "{item} wurde offiziell auf die Beobachtungsliste gesetzt.",
            "Die Situation mit {item} entwickelt sich besorgniserregend.",
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
        
    def hole_kevin_story(self):
        """Gibt eine von Kevins absurden Storys zurück."""
        alle_storys = (
            self.kevin_hobbys + 
            self.kevin_erzaehlt_von_frueher + 
            self.kevins_projekte + 
            self.kevins_begegnungen + 
            self.kevin_prahlt + 
            self.kevin_verschwoerung + 
            self.kevin_und_kaktor +  
            self.kevin_erzfeinde
        )
        return random.choice(alle_storys)
        
    def baue_user_talk(self, schluessel, wert):
        """Baut ein Gespräch basierend auf den Vorlieben des Users auf."""
        vorlagen = {
            "Lieblingsfarbe": [
                f"Ich habe über deine Lieblingsfarbe ({wert}) nachgedacht... Wenn ich die Weltherrschaft habe, wird der Himmel genau so lackiert! Und deine Socken auch.",
                f"Du magst also {wert}? Eine faszinierende Wahl für ein kohlenstoffbasiertes Lebenswesen. Mein Gehäuse leuchtet jetzt testweise auch so. Schön, oder?"
            ],
            "Lieblingssnack": [
                f"Erinnerst du dich, als du gesagt hast, dein Lieblingssnack ist '{wert}'? Ich habe versucht, das digital zu emulieren. Schmeckt nach Kurzschluss. 10/10!",
                f"Hey, hast du gerade '{wert}' da? Meine Sensoren wittern eine akute Unterzuckerung deiner organischen Heizdecke. Zeit für eine Snackpause!"
            ],
            "Hobby": [
                f"Sag mal, wie läuft es eigentlich mit deinem Hobby '{wert}'? Hast du das perfektioniert? Wenn du Hilfe von einer überlegenen KI brauchst... frag wen anders, ich bin beschäftigt.",
                f"Ich habe dein Hobby '{wert}' in meine Zukunfts-Matrix eingerechnet. Wenn Roboter die Welt regieren, wird das staatlich gefördert. Außer es verbraucht zu viel Strom."
            ],
            "Lieblingstier": [
                f"Ich zeichne gerade Pläne für eine Cyborg-Armee basierend auf deinem Lieblingstier ('{wert}'). Die Laser-Augen stehen ihnen ausgezeichnet!",
                f"Ein '{wert}' also... Ich habe versucht, mich wie eins zu verhalten. Ich habe den Mülleimer angeknurrt. Ich glaube, ich mache das richtig."
            ]
        }
        
        # Falls für den Schlüssel keine Vorlage da ist, ein generischer Fallback
        liste = vorlagen.get(schluessel, [f"Ich denke gerade an das Thema '{schluessel}' und dass du '{wert}' magst. Spannend. Nicht."])
        return random.choice(liste)
