# docs_vault/ddos_info.py

INFO = {
    "titulo": "LASTTEST (STRESSTEST)",
    "subtitulo": "Verkehrssimulation und Resilienz",
    "descricao": """

# 🔥 Lasttest (Stresstest)

---

## 👋 Was macht diese Funktion?

Dieser Teil von AURA ermöglicht es dir zu testen, wie sich ein System verhält, wenn es viele Verbindungen gleichzeitig erhält.

Einfach gesagt:

👉 du simulierst **mehrere gleichzeitige Zugriffe**, um zu sehen, ob das System damit umgehen kann.

---

## 🧠 Wofür ist das gut?

In der Cybersicherheit und Entwicklung ist es sehr wichtig zu wissen:

* kann das System viele Benutzer gleichzeitig verarbeiten?  
* wird es langsam?  
* hört es auf zu reagieren?  
* blockiert die Firewall übermäßige Verbindungen?  

👉 Dieser Test hilft, diese Fragen zu beantworten.

---

## ⚙️ Was passiert während des Tests?

Wenn du ihn startest:

* AURA sendet mehrere Anfragen an das Ziel  
* misst die Antwortzeit (Latenz)  
* überprüft, ob die Verbindung akzeptiert, blockiert oder unterbrochen wurde  
* überwacht alles in Echtzeit  

---

## 📊 Was wirst du sehen?

Während des Tests erhältst du Informationen wie:

* Gesamtzahl der gesendeten Verbindungen  
* wie viele normal funktioniert haben  
* wie viele blockiert wurden oder fehlgeschlagen sind  
* durchschnittliche Antwortzeit  

---

## 🚀 Wann solltest du das verwenden?

Du kannst diesen Test nutzen, um:

* die Stabilität eines Servers zu bewerten  
* Firewall-Regeln zu testen  
* Verbindungsgrenzen zu validieren  
* das Verhalten eines Systems unter hoher Last zu untersuchen  

---

## ⚠️ Verantwortungsvolle Nutzung

Diese Art von Test kann Systeme überlasten. Verwende ihn nur auf:

✔️ deinen eigenen Servern  

✔️ Testumgebungen  

✔️ autorisierten Systemen  

❌ Verwende ihn niemals gegen fremde Systeme ohne Erlaubnis.

---

## 💡 Tipp für Anfänger

Beginne mit **niedrigen Werten** (wenigen Anfragen) und erhöhe sie schrittweise. So kannst du verstehen, wie das System reagiert, ohne Probleme zu verursachen.

---

**Die Grenzen eines Systems zu verstehen ist der erste Schritt zum Aufbau robuster und sicherer Infrastrukturen.**
"""
}
