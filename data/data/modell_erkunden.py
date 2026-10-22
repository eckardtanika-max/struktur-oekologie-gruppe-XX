from collections import Counter
import rhino3dm

#modell = rhino3dm.File3dm.Read("data/Stockerau Rhino Export from RFEM.3dm")
modell = rhino3dm.File3dm.Read("/Users/anikaeckardt/struktur-oekologie-gruppe07/data/data/Stockerau Rhino Export from RFEM.3dm")

#print("Anzahl Objekte insgesamt:", len(modell.Objects))

zaehler = Counter()
for objekt in modell.Objects:
    ebene = modell.Layers[objekt.Attributes.LayerIndex].Name
    typ = type(objekt.Geometry).__name__
    zaehler[(ebene, typ)] += 1

print("Ebene / Typ / Anzahl:")
for (ebene, typ), anzahl in sorted(zaehler.items()):
    print(" ", ebene, "/", typ, "/", anzahl)
print("Anzahl Objekte insgesamt:", len(modell.Objects))    
#/Users/anikaeckardt/git hub/data/data
#'/Users/anikaeckardt/struktur-oekologie-gruppe07/data/data/Stockerau Rhino Export from RFEM.3dm'
import rhino3dm
import csv
import math
import os

# --- 1. HIER DEINEN DATEIPFAD EINTRAGEN ---
# Ändere den Text zwischen den Anführungszeichen zu deinem kopierten Pfad.
dateipfad = "/Users/anikaeckardt/struktur-oekologie-gruppe07/data/data/Stockerau Rhino Export from RFEM.3dm"

# Hier legen wir fest, wie deine fertige Excel-Tabelle heißen soll
csv_pfad = "pavillon_staebe.csv"

# --- AB HIER MACHT PYTHON DIE ARBEIT FÜR DICH ---

# Wir versuchen, die Rhino-Datei zu öffnen
modell = rhino3dm.File3dm.Read(dateipfad)

if modell is None:
    print("FEHLER: Die Rhino-Datei wurde nicht gefunden. Bitte prüfe den Dateipfad oben!")
else:
    staebe_liste = [] # Ein leerer Korb für unsere Ergebnisse

    # Wir gehen jedes einzelne Objekt in deinem Rhino-Modell durch
    for objekt in modell.Objects:
        geometrie = objekt.Geometry

        # Wir filtern: Wir wollen nur Kurven/Linien, keine Texte oder Punkte
        if isinstance(geometrie, rhino3dm.Curve):
            
            # Layer-Namen herausfinden
            try:
                layer_name = modell.Layers[objekt.Attributes.LayerIndex].Name
            except IndexError:
                layer_name = "Unbekannt"

            # Startpunkt und Endpunkt der Linie holen
            start = geometrie.PointAtStart
            ende = geometrie.PointAtEnd

            # Die Länge berechnen (wie der Satz des Pythagoras, nur in 3D)
            laenge = math.sqrt((ende.X - start.X)**2 + (ende.Y - start.Y)**2 + (ende.Z - start.Z)**2)

            # Die Daten für diesen einen Stab speichern (auf 3 Nachkommastellen gerundet)
            staebe_liste.append({
                "Layer": layer_name,
                "Start_X": round(start.X, 3),
                "Start_Y": round(start.Y, 3),
                "Start_Z": round(start.Z, 3),
                "Ende_X": round(ende.X, 3),
                "Ende_Y": round(ende.Y, 3),
                "Ende_Z": round(ende.Z, 3),
                "Laenge": round(laenge, 3)
            })

    # Jetzt erstellen wir die CSV-Datei für Excel
    with open(csv_pfad, mode="w", newline="", encoding="utf-8-sig") as datei:
        spalten = ["Layer", "Start_X", "Start_Y", "Start_Z", "Ende_X", "Ende_Y", "Ende_Z", "Laenge"]
        
        # WICHTIG: delimiter=";" sorgt dafür, dass das deutsche Excel die Spalten richtig erkennt!
        schreiber = csv.DictWriter(datei, fieldnames=spalten, delimiter=";") 
        
        schreiber.writeheader()         # Überschriften in die erste Zeile schreiben
        schreiber.writerows(staebe_liste) # Alle gesammelten Stäbe eintragen

    # Erfolgsmeldung für dich ausgeben
    print("-" * 50)
    print(f"Juhu! Es wurden {len(staebe_liste)} Stäbe gefunden und exportiert.")
    print(f"Deine fertige Tabelle liegt hier: {os.path.abspath(csv_pfad)}")