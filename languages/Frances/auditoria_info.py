# docs/trojan_info.py (or auditoria_info.py)

INFO = {
"titulo": "🛡️ Audit du Système",
"descricao": """

# 🛡️ Vérification de la Sécurité du Système

---

## 👋 Que fait cette fonction ?

Ce module effectue un **contrôle de sécurité sur votre ordinateur**.

Il analyse des configurations importantes et tente d’identifier des points faibles potentiels qui pourraient être exploités.

---

## 🔍 Que vérifie AURA ?

Pendant l’audit, AURA analyse :

* 🔑 **Permissions du système**  
  Vérifie si le programme s’exécute avec des privilèges élevés (Admin/Root)

* 📂 **Répertoires du système**  
  Recherche des emplacements où n’importe qui peut écrire des fichiers (ce qui peut être dangereux)

* 🌐 **Ports ouverts**  
  Détecte les services en cours d’exécution sur votre ordinateur qui peuvent être exposés

* ⚙️ **Processus actifs**  
  Recherche des programmes suspects s’exécutant en arrière-plan

* 🔥 **Pare-feu**  
  Vérifie si la protection du système est active

* 📄 **Fichier réseau (hosts)**  
  Analyse les modifications possibles pouvant indiquer des redirections malveillantes

---

## 🧠 Pourquoi est-ce important ?

De nombreux problèmes de sécurité ne proviennent pas d’attaques complexes, mais plutôt de :

👉 configurations incorrectes  
👉 permissions trop ouvertes  
👉 services inutiles en cours d’exécution  

Ce module vous aide à identifier cela de manière simple.

---

## 📊 Comment comprendre les résultats ?

AURA classe tout de manière claire :

* 🔴 **[ÉLEVÉ]** → risque important, nécessite une attention  
* 🟡 **[MOYEN]** → peut être amélioré  
* 🟢 **[OK]** → tout est correct  

---

## 🚀 Quand l’utiliser ?

Vous pouvez exécuter cet audit pour :

* vérifier si votre système est sécurisé  
* mieux comprendre le fonctionnement de la sécurité locale  
* apprendre en pratique les configurations du système  

---

## ⚠️ Remarque importante

Cette analyse est **locale** (sur votre propre système).  
Elle ne modifie rien — elle analyse et informe uniquement.

---

## 💡 Conseil pour débutants

Utilisez ce module comme un « thermomètre » :

👉 exécutez-le  
👉 observez les résultats  
👉 recherchez chaque élément  

Cela accélère BEAUCOUP votre apprentissage.

---

**La sécurité commence par la compréhension de votre propre système.**
"""
}
