# docs_vault/ddos_info.py

INFO = {
    "titulo": "TEST DE CHARGE (STRESS TEST)",
    "subtitulo": "Simulation de Trafic et Résilience",
    "descricao": """

# 🔥 Test de Charge (Stress Test)

---

## 👋 Que fait cette fonction ?

Cette partie d’AURA vous permet de tester comment un système se comporte lorsqu’il reçoit de nombreuses connexions en même temps.

En termes simples :

👉 vous simulez **plusieurs accès simultanés** pour voir si le système peut le supporter.

---

## 🧠 À quoi cela sert-il ?

En cybersécurité et en développement, il est très important de savoir :

* le système peut-il gérer de nombreux utilisateurs en même temps ?  
* devient-il lent ?  
* cesse-t-il de répondre ?  
* le pare-feu bloque-t-il l’excès de connexions ?  

👉 Ce test aide à répondre à ces questions.

---

## ⚙️ Que se passe-t-il pendant le test ?

Lorsque vous le lancez :

* AURA envoie plusieurs requêtes à la cible  
* mesure le temps de réponse (latence)  
* vérifie si la connexion a été acceptée, bloquée ou interrompue  
* surveille tout en temps réel  

---

## 📊 Que verrez-vous ?

Pendant le test, vous obtiendrez des informations telles que :

* nombre total de connexions envoyées  
* combien ont fonctionné normalement  
* combien ont été bloquées ou ont échoué  
* temps moyen de réponse  

---

## 🚀 Quand devriez-vous l’utiliser ?

Vous pouvez utiliser ce test pour :

* évaluer la stabilité d’un serveur  
* tester les règles du pare-feu  
* valider les limites de connexion  
* étudier le comportement du système sous forte charge  

---

## ⚠️ Utilisation responsable

Ce type de test peut surcharger les systèmes. Utilisez-le uniquement sur :

✔️ vos propres serveurs  

✔️ des environnements de test  

✔️ des systèmes autorisés  

❌ Ne l’utilisez jamais contre des systèmes tiers sans permission.

---

## 💡 Conseil pour débutants

Commencez avec **des valeurs faibles** (peu de requêtes) et augmentez progressivement. Cela vous aidera à comprendre comment le système réagit sans causer de problèmes.

---

**Comprendre les limites d’un système est la première étape pour construire des infrastructures résilientes et sécurisées.**
"""
}
