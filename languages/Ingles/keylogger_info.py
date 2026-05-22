# docs/keylogger_info.py

INFO = {
    "titulo": "⌨️ TYPING AUDIT (KEYLOGGER)",
    "descricao": """
# ⌨️ Keystroke Monitoring (Controlled Use)

This AURA module allows you to monitor and record what is typed on the keyboard during a session.  
In Cybersecurity, this is used to **understand behavior, test security, and analyze activity in controlled environments**.

### 🔎 What does this module do?

Simply put, it:

* Records everything typed during system usage  
* Identifies which program or window the typing occurred in  
* Organizes this information into a log file  
* Generates a small summary with activity statistics  

This helps understand **how a user interacts with the system**, or even simulate how certain types of attacks work.

---

### 📊 Collected information

During execution, AURA records:

* Typed text  
* Window changes (e.g., browser, terminal, etc.)  
* Total number of keys pressed  
* Usage of keys like Enter and Backspace  
* Most frequently used keys during the session  

All of this is automatically saved in the `/logs` folder.

---

### ⏱️ Smart operation

The system is designed to be lightweight:

* Saves data in batches (does not write on every keystroke)  
* Detects when the user is inactive  
* Automatically ends sessions after long periods of inactivity  

---

### ⚠️ Responsible use and ethics

This is an extremely sensitive module.

* ❌ **Never use it on other people's computers without authorization**  
* ❌ Monitoring someone without consent may be illegal  
* ✅ Use only in your own environment or lab  
* ✅ Ideal for study and security testing  

---

### 💡 Why is this important?

Tools like this are used by attackers to steal passwords and information.

By understanding how they work, you learn:

* How to protect yourself against this type of threat  
* Why using password managers is important  
* How to identify suspicious behavior on a system  

---

**Summary:**  
This module is not about spying — it is about **understanding real risks and learning how to better protect yourself in the digital world.**
"""
}
