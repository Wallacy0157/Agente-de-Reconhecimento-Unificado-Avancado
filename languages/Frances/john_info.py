# docs/john_info.py

INFO = {
"titulo": "💀 CRAQUAGE DE HASHES (JOHN THE RIPPER ENGINE)",
"descricao": """

# 🔐 Test de Sécurité des Mots de Passe

---

## 👋 Que fait cette fonction ?

Ce module vous permet de **tester la sécurité des mots de passe protégés (hashes)**.

Au lieu de travailler avec le mot de passe original, il analyse le hash — qui est une représentation chiffrée du mot de passe.

---

## 🧠 Qu’est-ce qu’un hash ?

Un hash est une manière de transformer un mot de passe en un code unique.

Par exemple :

👉 mot de passe : `123456`  
👉 hash : `e10adc3949ba59abbe56e057f20f883e`  

Les systèmes utilisent des hashes pour protéger les mots de passe.

---

## 🔍 Que fait AURA ?

AURA essaie de déterminer si un mot de passe est faible en testant :

* 📚 **Listes de mots de passe courants**  
  (mots de passe déjà connus et largement utilisés)

* 🔄 **Variations automatiques**  
  (comme ajouter des chiffres ou modifier des lettres)

* 🔢 **Combinaisons possibles**  
  (lorsque vous définissez un modèle)

👉 Cela simule ce qu’un attaquant ferait — mais de manière contrôlée.

---

## 🧠 Pourquoi est-ce important ?

Si un mot de passe peut être découvert rapidement, il est considéré comme faible.

Ce test vous aide à comprendre :

* si un mot de passe est facile à deviner  
* s’il doit être renforcé  
* comment améliorer la protection du système  

---

## 📊 Que verrez-vous ?

AURA affiche :

* si le mot de passe a été découvert ou non  
* quelle méthode a été utilisée  
* combien d’efforts ont été nécessaires  

---

## 🚀 Quand devriez-vous l’utiliser ?

Ce module est utile pour :

* apprendre la sécurité des mots de passe  
* tester des hashes dans des environnements contrôlés  
* valider la robustesse des identifiants  

---

## ⚠️ Utilisation responsable

Cette fonctionnalité doit être utilisée uniquement dans :

✔️ vos propres tests  
✔️ des environnements de laboratoire  
✔️ des systèmes autorisés  

❌ Ne l’utilisez jamais pour accéder aux comptes d’autres personnes.

---

## 💡 Conseil pour débutants

Testez avec :

* des hashes de mots de passe simples  
* des exemples de laboratoire  
* vos propres données  

👉 Cela vous aide à comprendre comment les mots de passe peuvent être protégés (ou cassés).

---

## 🧠 Comprendre le concept

Les mots de passe faibles sont l’une des plus grandes failles de sécurité.

👉 Plus il est difficile à deviner, plus il est sécurisé.

---

**Un mot de passe fort est votre première ligne de défense.**
"""
}
