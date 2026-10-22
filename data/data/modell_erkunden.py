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

    import rhino3dm

# --- HIER WIEDER DEINEN PFAD EINTRAGEN ---
dateipfad = "/Users/anikaeckardt/struktur-oekologie-gruppe07/data/data/Stockerau Rhino Export from RFEM.3dm"

modell = rhino3dm.File3dm.Read(dateipfad)

if modell is None:
    print("FEHLER: Die Rhino-Datei wurde nicht gefunden.")
else:
    print("--- LUPEN-SKRIPT START ---")
    
    # Wir schnappen uns die ersten 5 Objekte im Modell
    gefunden = 0
    for objekt in modell.Objects:
        if gefunden >= 5: # Nach 5 Objekten stoppen wir
            break
            
        typ = type(objekt.Geometry).__name__
        print(f"\nObjekt {gefunden+1} (Typ: {typ}):")
        
        # Hier holen wir die versteckten RFEM-Daten
        rfem_daten = objekt.Attributes.GetUserStrings()
        
        if rfem_daten and len(rfem_daten) > 0:
            print("  Versteckte RFEM-Daten gefunden:")
            for daten in rfem_daten:
                schluessel = daten[0] # Der Name (z.B. "Area" oder "Querschnitt")
                wert = daten[1]       # Der Wert (z.B. "15.5")
                print(f"  -> {schluessel}: {wert}")
        else:
            print("  Dieses Objekt hat leider keine versteckten User-String-Daten.")
            
        gefunden += 1
            
    print("\n--- LUPEN-SKRIPT ENDE ---")

import rhino3dm

dateipfad = "/Users/anikaeckardt/struktur-oekologie-gruppe07/data/data/Stockerau Rhino Export from RFEM.3dm"

modell = rhino3dm.File3dm.Read(dateipfad)

if modell:
    staebe_gefunden = 0
    for objekt in modell.Objects:
        if isinstance(objekt.Geometry, rhino3dm.Curve):
            try:
                layer_name = modell.Layers[objekt.Attributes.LayerIndex].Name
                print(f"Stab {staebe_gefunden + 1} - Layer: '{layer_name}'")
            except IndexError:
                pass
            
            staebe_gefunden += 1
            if staebe_gefunden >= 15:
                break
else:
    print("Fehler: Datei konnte nicht geladen werden.")   
import rhino3dm

dateipfad = "/Users/anikaeckardt/struktur-oekologie-gruppe07/data/data/Stockerau Rhino Export from RFEM.3dm"
modell = rhino3dm.File3dm.Read(dateipfad)

if modell:
    gefundene_layer = set()
    gefundene_namen = set()
    
    for objekt in modell.Objects:
        if isinstance(objekt.Geometry, rhino3dm.Curve):
            try:
                layer_name = modell.Layers[objekt.Attributes.LayerIndex].Name
                gefundene_layer.add(layer_name)
            except IndexError:
                pass
            
            if objekt.Attributes.Name:
                gefundene_namen.add(objekt.Attributes.Name)

    print("Gefundene Layer:")
    for layer in sorted(gefundene_layer):
        print(f"- {layer}")
        
    print("\nGefundene Objekt-Namen:")
    if gefundene_namen:
        for name in sorted(gefundene_namen):
            print(f"- {name}")
    else:
        print("- (Keine spezifischen Objekt-Namen vergeben)")
else:
    print("Fehler: Datei konnte nicht geladen werden.")    
import rhino3dm
import csv
import math

dateipfad_rhino = "/Users/anikaeckardt/struktur-oekologie-gruppe07/data/data/Stockerau Rhino Export from RFEM.3dm"
csv_pfad = "pavillon_staebe_final.csv"

flaechen_katalog = {
    "Flat Bar 162.5/12": 19.5,
    "Flat Bar 162.5/20": 32.5,
    "Flat Bar 175/12": 21.0,
    "Flat Bar 175/20": 35.0,
    "Flat Bar 200/12": 24.0,
    "Flat Bar 200/20": 40.0,
    "Flat Bar 225/12": 27.0,
    "Flat Bar 225/20": 45.0,
    "Flat Bar 237.5/12": 28.5,
    "Flat Bar 237.5/20": 47.5,
    "Flat Bar 275/12": 33.0,
    "Flat Bar 275/20": 55.0,
    "Flat Bar 33.3/20": 6.66,
    "RD 12": 1.13,
    "RO 139.7x8.0 | EN 10210-2:2006": 33.1,
    "Rectangle 500/500": 2500.0
}

modell = rhino3dm.File3dm.Read(dateipfad_rhino)

if modell:
    staebe_liste = []
    
    for objekt in modell.Objects:
        geo = objekt.Geometry
        
        if isinstance(geo, rhino3dm.Curve):
            try:
                ebene = modell.Layers[objekt.Attributes.LayerIndex].Name
            except IndexError:
                continue
            
            if ebene in flaechen_katalog:
                start = geo.PointAtStart
                ende = geo.PointAtEnd
                laenge = math.sqrt((ende.X - start.X)**2 + (ende.Y - start.Y)**2 + (ende.Z - start.Z)**2)
                
                flaeche = flaechen_katalog[ebene]
                volumen = flaeche * laenge
                
                staebe_liste.append({
                    "Layer": ebene,
                    "Start_X": round(start.X, 3),
                    "Start_Y": round(start.Y, 3),
                    "Start_Z": round(start.Z, 3),
                    "Ende_X": round(ende.X, 3),
                    "Ende_Y": round(ende.Y, 3),
                    "Ende_Z": round(ende.Z, 3),
                    "Laenge": round(laenge, 3),
                    "Flaeche_cm2": flaeche,
                    "Volumen": round(volumen, 3)
                })

    with open(csv_pfad, mode="w", newline="", encoding="utf-8-sig") as datei:
        spaltennamen = ["Layer", "Start_X", "Start_Y", "Start_Z", "Ende_X", "Ende_Y", "Ende_Z", "Laenge", "Flaeche_cm2", "Volumen"]
        writer = csv.DictWriter(datei, fieldnames=spaltennamen, delimiter=";")
        
        writer.writeheader()
        writer.writerows(staebe_liste)
        
    print(f"Export erfolgreich: {len(staebe_liste)} baustrukturelle Stäbe in '{csv_pfad}' gespeichert.")
else:
    print("Fehler: Datei konnte nicht geladen werden.")    
