INFO = {
    "titulo": "🧰 CREDENTIAL TESTING (HYDRA)",
    "descricao": """
# 🧰 Password and Login Testing

This AURA module allows you to test the security of systems that use login and password authentication.  
It simulates access attempts to check whether credentials are easy to guess.

In practice, this helps answer a simple question:  
👉 *“Is this password really secure?”*

---

### 🔎 What does this module do?

Simply put, it:

* Tests combinations of usernames and passwords on a system  
* Can use lists of common passwords (wordlists)  
* Simulates multiple login attempts automatically  
* Shows if any valid credential was found  

This is widely used in audits to identify **weak or predictable passwords**.

---

### ⚙️ How does it work in practice?

The module can operate in two main ways:

* **Single password:** test one user with a specific password  
* **Password list:** test multiple combinations automatically  

It can also work with different types of systems, such as:

* Remote access (e.g., SSH, FTP)  
* Internal systems  
* Websites with login pages  

---

### 🚀 Efficient execution

AURA speeds up testing by using:

* Multiple simultaneous attempts (parallelism)  
* Automatic interruption when a valid password is found  
* Real-time progress display  

This allows you to quickly test whether a system is protected or not.

---

### ⚠️ Responsible use and ethics

This module must be used with extreme care:

* ❌ Never test systems without authorization  
* ❌ Do not use it on third-party networks or servers  
* ✅ Use only in your own lab or environment  
* ✅ Ideal for security testing and learning  

---

### 💡 Why is this important?

Many real-world attacks exploit weak passwords.

With this module, you learn:

* How brute-force attacks work  
* Why simple passwords are dangerous  
* How to implement stronger password policies  
* The importance of protections like login attempt blocking (e.g., Fail2Ban)  

---

**Summary:**  
This module is not meant to invade systems, but to **test and strengthen login security**, helping prevent unauthorized access.
"""
}
