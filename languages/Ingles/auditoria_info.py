# docs/trojan_info.py (or auditoria_info.py)

INFO = {
"titulo": "🛡️ System Audit",
"descricao": """

# 🛡️ System Security Check

---

## 👋 What does this function do?

This module performs a **security check-up on your computer**.

It analyzes important configurations and tries to identify possible weak points that could be exploited.

---

## 🔍 What does AURA check?

During the audit, AURA analyzes:

* 🔑 **System permissions**
  Checks if the program is running with elevated privileges (Admin/Root)

* 📂 **System directories**
  Looks for locations where anyone can write files (which can be dangerous)

* 🌐 **Open ports**
  Detects services running on your computer that may be exposed

* ⚙️ **Active processes**
  Searches for suspicious programs running in the background

* 🔥 **Firewall**
  Checks if system protection is active

* 📄 **Network file (hosts)**
  Analyzes possible changes that may indicate malicious redirections

---

## 🧠 Why is this important?

Many security issues are not in complex attacks, but rather in:

👉 misconfigurations  
👉 overly permissive settings  
👉 unnecessary services running  

This module helps you identify that in a simple way.

---

## 📊 How to understand the results?

AURA classifies everything clearly:

* 🔴 **[HIGH]** → important risk, needs attention  
* 🟡 **[MEDIUM]** → can be improved  
* 🟢 **[OK]** → everything is fine  

---

## 🚀 When should you use it?

You can run this audit to:

* check if your system is secure  
* better understand how local security works  
* learn in practice about system configurations  

---

## ⚠️ Important note

This analysis is **local** (on your own system).  
It does not modify anything — it only analyzes and informs.

---

## 💡 Tip for beginners

Use this module as a “thermometer”:

👉 run it  
👉 see what shows up  
👉 research each item  

This speeds up your learning A LOT.

---

**Security starts with understanding your own system.**
"""
}
