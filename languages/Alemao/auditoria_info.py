# docs/trojan_info.py (or auditoria_info.py)

INFO = {
"titulo": "🛡️ Systemprüfung",
"descricao": """

# 🛡️ System-Sicherheitsüberprüfung

---

## 👋 Was macht diese Funktion?

Dieses Modul führt einen **Sicherheitscheck auf deinem Computer** durch.

Es analysiert wichtige Konfigurationen und versucht, mögliche Schwachstellen zu identifizieren, die ausgenutzt werden könnten.

---

## 🔍 Was überprüft AURA?

Während der Prüfung analysiert AURA:

* 🔑 **Systemberechtigungen**  
  Überprüft, ob das Programm mit erhöhten Rechten (Admin/Root) ausgeführt wird

* 📂 **Systemverzeichnisse**  
  Sucht nach Orten, an denen jeder Dateien schreiben kann (was gefährlich sein kann)

* 🌐 **Offene Ports**  
  Erkennt laufende Dienste auf deinem Computer, die exponiert sein könnten

* ⚙️ **Aktive Prozesse**  
  Sucht nach verdächtigen Programmen im Hintergrund

* 🔥 **Firewall**  
  Überprüft, ob der Systemschutz aktiv ist

* 📄 **Netzwerkdatei (hosts)**  
  Analysiert mögliche Änderungen, die auf bösartige Weiterleitungen hinweisen könnten

---

## 🧠 Warum ist das wichtig?

Viele Sicherheitsprobleme entstehen nicht durch komplexe Angriffe, sondern durch:

👉 falsche Konfigurationen  
👉 zu offene Berechtigungen  
👉 unnötig laufende Dienste  

Dieses Modul hilft dir, das einfach zu erkennen.

---

## 📊 Wie versteht man die Ergebnisse?

AURA klassifiziert alles klar und verständlich:

* 🔴 **[HOCH]** → wichtiges Risiko, erfordert Aufmerksamkeit  
* 🟡 **[MITTEL]** → kann verbessert werden  
* 🟢 **[OK]** → alles in Ordnung  

---

## 🚀 Wann sollte man es verwenden?

Du kannst diese Prüfung ausführen, um:

* zu überprüfen, ob dein System sicher ist  
* besser zu verstehen, wie lokale Sicherheit funktioniert  
* praktisch etwas über Systemkonfigurationen zu lernen  

---

## ⚠️ Wichtiger Hinweis

Diese Analyse ist **lokal** (auf deinem eigenen System).  
Sie verändert nichts — sie analysiert nur und informiert.

---

## 💡 Tipp für Anfänger

Nutze dieses Modul wie ein „Thermometer“:

👉 führe es aus  
👉 schaue dir die Ergebnisse an  
👉 recherchiere jeden Punkt  

Das beschleunigt dein Lernen SEHR.

---

**Sicherheit beginnt mit dem Verständnis des eigenen Systems.**
"""
}
