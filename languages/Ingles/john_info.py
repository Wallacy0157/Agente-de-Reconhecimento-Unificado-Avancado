# docs/john_info.py

INFO = {
"titulo": "💀 HASH CRACKING (JOHN THE RIPPER ENGINE)",
"descricao": """

# 🔐 Password Security Testing

---

## 👋 What does this function do?

This module allows you to **test the security of protected passwords (hashes)**.

Instead of working with the original password, it analyzes the hash — which is an encrypted representation of the password.

---

## 🧠 What is a hash?

A hash is a way of transforming a password into a unique code.

For example:

👉 password: `123456`  
👉 hash: `e10adc3949ba59abbe56e057f20f883e`  

Systems use hashes to protect passwords.

---

## 🔍 What does AURA do?

AURA tries to determine if a password is weak by testing:

* 📚 **Common password lists**  
  (passwords already known and widely used)

* 🔄 **Automatic variations**  
  (such as adding numbers or modifying letters)

* 🔢 **Possible combinations**  
  (when you define a pattern)

👉 This simulates what an attacker would do — but in a controlled way.

---

## 🧠 Why is this important?

If a password can be discovered quickly, it is considered weak.

This test helps you understand:

* whether a password is easy to guess  
* if it needs to be stronger  
* how to improve system protection  

---

## 📊 What will you see?

AURA shows:

* whether the password was cracked or not  
* which method was used  
* how much effort was required  

---

## 🚀 When should you use it?

This module is useful for:

* learning about password security  
* testing hashes in controlled environments  
* validating the strength of credentials  

---

## ⚠️ Responsible use

This feature should only be used in:

✔️ your own tests  
✔️ lab environments  
✔️ authorized systems  

❌ Never use it to access other people's accounts.

---

## 💡 Tip for beginners

Test with:

* simple password hashes  
* lab examples  
* your own data  

👉 This helps you understand how passwords can be protected (or cracked).

---

## 🧠 Understand the concept

Weak passwords are one of the biggest security flaws.

👉 The harder it is to guess, the more secure it is.

---

**A strong password is your first line of defense.**
"""
}
