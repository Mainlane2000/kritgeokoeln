# kritgeokoeln

Website der Kritischen Geographie Köln als modernes One-Page-Template. Die Website
wird lokal über einen kleinen Python-Server ausgeliefert und ist damit bereits
von der direkten Anzeige der HTML-Datei entkoppelt.

## Enthalten

- `index.html`: Landingpage + Unterseiten-Sektionen (Scroll-Snap)
- `styles.css`: Modernes Designsystem (Farben, Typografie, Layout, Responsive)
- `script.js`: Navigation, mobile Menufunktion, aktive Sektion im Header
- `server.py`: Dependency-freier lokaler Webserver für die statischen Dateien
- `.gitignore`: Ignoriert lokale Python- und Betriebssystemdateien

## Quellen und Lizenzen

Das Layout, die Texte, das CSS und das JavaScript sind eigens für dieses Projekt
erstellt und enthalten keine übernommenen Code- oder Bild-Assets. Die verwendeten
Schriften [Fraunces](https://github.com/undercasetype/Fraunces) und
[Sora](https://fonts.google.com/specimen/Sora) stehen unter der
[SIL Open Font License](https://scripts.sil.org/OFL). Die Karte im Kontaktbereich
verlinkt [OpenStreetMap](https://www.openstreetmap.org/) statt eines proprietären
Kartendienstes. Die Sektion „Kritische Karten“ verlinkt ebenfalls auf
[OpenStreetMap](https://www.openstreetmap.org/); die darin enthaltene abstrakte
Kartenillustration ist als eigenes, inline eingebettetes SVG erstellt und
benötigt keine externe Bildquelle.

## Anpassung

- Inhalte in den einzelnen `<section>`-Blöcken in `index.html` ersetzen.
- Navigation im Header erweitern oder reduzieren (Links auf `#id` der Sektionen).
- Designfarben zentral in den CSS-Variablen unter `:root` in `styles.css` anpassen.

## Lokale Entwicklung

Voraussetzung ist Python 3.9 oder neuer. Im Projektverzeichnis starten:

```bash
python3 server.py
```

Danach ist die Website unter <http://127.0.0.1:8000> erreichbar. Der Server
unterstützt die Umgebungsvariablen `HOST` und `PORT`, zum Beispiel:

```bash
HOST=0.0.0.0 PORT=8080 python3 server.py
```

Der Endpoint <http://127.0.0.1:8000/healthz> liefert `{"status": "ok"}` und
kann für lokale Checks oder später für einen Hosting-Health-Check verwendet
werden. Die HTML-Datei sollte nicht mehr direkt per `file://` geöffnet werden.

## Für das spätere Webhosting

`server.py` ist für lokale Entwicklung und nicht als produktiver Internetserver
gedacht. Beim Umzug auf ein Hosting müssen insbesondere diese Bereiche angepasst
werden:

1. **Serverbetrieb:** `server.py` durch den vom Hoster vorgesehenen Webserver
   oder einen Produktions-Stack ersetzen (z. B. Nginx/Apache als Reverse Proxy).
   Der statische Inhalt bleibt `index.html`, `styles.css` und `script.js`.
2. **Adresse und Sicherheit:** eine Domain konfigurieren, HTTPS/TLS aktivieren
   und den Server nicht ungeschützt über `0.0.0.0` ins Internet stellen.
   Sicherheitsheader, Logging, Rate-Limiting und Fehlerseiten gehören in die
   Produktionskonfiguration.
3. **Deployment:** den Startprozess, Health-Checks, Restart-Verhalten und
   Umgebungsvariablen (`HOST`, `PORT`) an den Hosting-Anbieter anpassen.
4. **Externe Ressourcen:** Die Google-Fonts in `index.html` benötigen im
   Produktivbetrieb eine Datenschutzprüfung; alternativ können die Fonts lokal
   ausgeliefert werden.
5. **Ideenpool-Formular:** Das Formular in `index.html` hat derzeit
   `action="#"` und speichert keine Eingaben. Für eine Veröffentlichung braucht
   es ein abgesichertes Backend oder einen geprüften Formular-Dienst,
   inklusive Spam-Schutz, Validierung und Datenschutzhinweisen.
6. **Inhalte und Rechtliches:** Platzhalter in `index.html` ersetzen und
   Impressum, Datenschutz sowie Kontaktangaben vor dem öffentlichen Launch
   ergänzen.
