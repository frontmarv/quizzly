# Technische Anforderungen (System Prompt / Copilot Context)

Dieses Dokument definiert die Programmierrichtlinien und Qualitätsstandards für dieses Projekt. Halte dich bei jeder Codegenerierung, jedem Refactoring und jeder Code-Erklärung strikt an diese Vorgaben.

## 1. Clean Code & Struktur
- **Funktionslänge:** Funktionen dürfen **maximal 14 Zeilen** lang sein. Wenn eine Funktion länger wird, lagere Logik in Hilfsfunktionen aus.
- **Single Responsibility Principle:** Jede Funktion erfüllt **genau eine** spezifische Aufgabe.
- **Namenskonventionen:** 
  - Alle Funktionsnamen folgen strikt der `snake_case`-Konvention.
  - Verwende durchgängig **sprechende und aussagekräftige** Variablennamen (keine kryptischen Abkürzungen).
- **Code-Hygiene:** 
  - Alle deklarierten Variablen und Funktionen müssen aktiv genutzt werden (kein toter Code).
  - Jeglicher auskommentierte Code ist vor dem Commit/der Ausgabe zu entfernen.

## 2. Dokumentation
- sämtliche Dokumentation ist auf englisch zu verfassen.
- **Docstrings:** Jede Funktion, Methode und Klasse muss einen prägnanten und verständlichen **Docstring** (PEP 257) enthalten, der den Zweck, die Parameter und den Rückgabewert beschreibt.
- **Projekt-Dokumentation:** Die `README.md`-Datei muss existieren, aussagekräftig sein und das Setup sowie die Architektur des Projekts beschreiben.

## 3. Django-Spezifische Richtlinien
- **Dateistruktur (Separation of Concerns):** Code gehört in die jeweils dafür vorgesehene Datei:
  - `views.py`: Enthält **ausschließlich** Views, die eine HTTP-Response zurückgeben. Keine komplexe Business- oder Hilfslogik hier.
  - `functions.py` oder `utils.py`: Lege diese Dateien neu an, um Hilfsfunktionen, Berechnungen und komplexe Logik sauber auszulagern.
- **Django Admin Panel:** 
  - Das Admin-Panel muss vollständig gepflegt und konfiguriert sein.
  - Es muss die Bearbeitung von Quizzes (`Quizzes`) und einzelnen Quizfragen (`Quizfragen`) intuitiv und direkt zulassen.

## 4. Pythonic Style (PEP 8)
- **Konformität:** Der gesamte Python-Code muss **PEP-8-konform** sein.
- **Einhaltung:** Halte die Formatierungsregeln (z. B. Einrückungen, Zeilenlänge von max. 79 Zeichen, Leerzeilen) konsequent ein.