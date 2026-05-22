# docs/keylogger_info.py

INFO = {
    "titulo": "⌨️ TASTATUR-AUDIT (KEYLOGGER)",
    "descricao": """
# ⌨️ Tastenüberwachung (Kontrollierte Nutzung)

Dieses AURA-Modul ermöglicht es dir, alles, was während einer Sitzung auf der Tastatur eingegeben wird, zu überwachen und aufzuzeichnen.  
In der Cybersicherheit wird dies verwendet, um **Verhaltensweisen zu verstehen, Sicherheit zu testen und Aktivitäten in kontrollierten Umgebungen zu analysieren**.

### 🔎 Was macht dieses Modul?

Einfach gesagt:

* Zeichnet alles auf, was während der Systemnutzung eingegeben wird  
* Erkennt, in welchem Programm oder Fenster die Eingabe erfolgt ist  
* Organisiert diese Informationen in einer Protokolldatei (Log)  
* Erstellt eine kurze Zusammenfassung mit Aktivitätsstatistiken  

Das hilft zu verstehen, **wie ein Benutzer mit dem System interagiert**, oder sogar zu simulieren, wie bestimmte Arten von Angriffen funktionieren.

---

### 📊 Gesammelte Informationen

Während der Ausführung zeichnet AURA auf:

* Eingegebener Text  
* Fensterwechsel (z. B. Browser, Terminal usw.)  
* Gesamtanzahl der gedrückten Tasten  
* Nutzung von Tasten wie Enter und Backspace  
* Am häufigsten verwendete Tasten während der Sitzung  

All dies wird automatisch im Ordner `/logs` gespeichert.

---

### ⏱️ Intelligente Funktionsweise

Das System ist so konzipiert, dass es leichtgewichtig ist:

* Speichert Daten in Blöcken (nicht bei jedem Tastendruck)  
* Erkennt, wenn der Benutzer inaktiv ist  
* Beendet Sitzungen automatisch nach längeren Inaktivitätsphasen  

---

### ⚠️ Verantwortungsvolle Nutzung und Ethik

Dies ist ein äußerst sensibles Modul.

* ❌ **Verwende es niemals auf den Computern anderer Personen ohne Erlaubnis**  
* ❌ Jemanden ohne Zustimmung zu überwachen kann illegal sein  
* ✅ Nutze es nur in deiner eigenen Umgebung oder im Labor  
* ✅ Ideal für Studium und Sicherheitstests  

---

### 💡 Warum ist das wichtig?

Solche Tools werden von Angreifern verwendet, um Passwörter und Informationen zu stehlen.

Indem du verstehst, wie sie funktionieren, lernst du:

* Wie du dich gegen diese Art von Bedrohung schützen kannst  
* Warum es wichtig ist, Passwort-Manager zu verwenden  
* Wie man verdächtiges Verhalten auf einem System erkennt  

---

**Zusammenfassung:**  
Dieses Modul dient nicht der Spionage — sondern dazu, **reale Risiken zu verstehen und zu lernen, sich in der digitalen Welt besser zu schützen.**
"""
}
