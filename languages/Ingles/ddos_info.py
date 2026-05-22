# docs_vault/ddos_info.py

INFO = {
    "titulo": "LOAD TEST (STRESS TEST)",
    "subtitulo": "Traffic Simulation and Resilience",
    "descricao": """

# 🔥 Load Test (Stress Test)

---

## 👋 What does this function do?

This part of AURA allows you to test how a system behaves when it receives many connections at the same time.

Simply put:

👉 you simulate **multiple simultaneous accesses** to see if the system can handle it.

---

## 🧠 What is this for?

In cybersecurity and development, it is very important to know:

* can the system handle many users at the same time?  
* does it slow down?  
* does it stop responding?  
* does the firewall block excessive connections?  

👉 This test helps answer these questions.

---

## ⚙️ What happens during the test?

When you start:

* AURA sends multiple requests to the target  
* measures response time (latency)  
* checks whether the connection was accepted, blocked, or dropped  
* monitors everything in real time  

---

## 📊 What will you see?

During the test, you will get information such as:

* total number of connections sent  
* how many worked normally  
* how many were blocked or failed  
* average response time  

---

## 🚀 When should you use this?

You can use this test to:

* evaluate server stability  
* test firewall rules  
* validate connection limits  
* study system behavior under high load  

---

## ⚠️ Responsible use

This type of test can overload systems. Use it only on:

✔️ your own servers  

✔️ test environments  

✔️ systems with proper authorization  

❌ Never use this against third-party systems without permission.

---

## 💡 Tip for beginners

Start with **low values** (few requests) and gradually increase them. This will help you understand how the system reacts without causing issues.

---

**Understanding system limits is the first step to building resilient and secure infrastructures.**
"""
}
