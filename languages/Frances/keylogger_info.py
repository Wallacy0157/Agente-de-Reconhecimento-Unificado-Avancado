# docs/keylogger_info.py

INFO = {
    "titulo": "⌨️ AUDIT DE FRAPPE (KEYLOGGER)",
    "descricao": """
# ⌨️ Surveillance des Frappes (Utilisation Contrôlée)

Ce module d’AURA vous permet de surveiller et d’enregistrer ce qui est tapé au clavier pendant une session.  
En cybersécurité, cela est utilisé pour **comprendre les comportements, tester la sécurité et analyser les activités dans des environnements contrôlés**.

### 🔎 Que fait ce module ?

En termes simples, il :

* Enregistre tout ce qui est tapé pendant l’utilisation du système  
* Identifie dans quel programme ou fenêtre la saisie a eu lieu  
* Organise ces informations dans un fichier journal (log)  
* Génère un petit résumé avec des statistiques d’activité  

Cela permet de comprendre **comment un utilisateur interagit avec le système**, ou même de simuler le fonctionnement de certains types d’attaques.

---

### 📊 Informations collectées

Pendant l’exécution, AURA enregistre :

* Le texte saisi  
* Les changements de fenêtre (ex : navigateur, terminal, etc.)  
* Le nombre total de touches pressées  
* L’utilisation de touches comme Entrée et Retour arrière  
* Les touches les plus utilisées pendant la session  

Tout cela est automatiquement enregistré dans le dossier `/logs`.

---

### ⏱️ Fonctionnement intelligent

Le système est conçu pour être léger :

* Enregistre les données par blocs (n’écrit pas à chaque frappe)  
* Détecte lorsque l’utilisateur est inactif  
* Termine automatiquement les sessions après de longues périodes d’inactivité  

---

### ⚠️ Utilisation responsable et éthique

Il s’agit d’un module extrêmement sensible.

* ❌ **Ne l’utilisez jamais sur les ordinateurs d’autres personnes sans autorisation**  
* ❌ Surveiller quelqu’un sans consentement peut être illégal  
* ✅ Utilisez-le uniquement dans votre propre environnement ou laboratoire  
* ✅ Idéal pour l’étude et les tests de sécurité  

---

### 💡 Pourquoi est-ce important ?

Des outils comme celui-ci sont utilisés par des attaquants pour voler des mots de passe et des informations.

En comprenant leur fonctionnement, vous apprenez :

* Comment vous protéger contre ce type de menace  
* Pourquoi il est important d’utiliser des gestionnaires de mots de passe  
* Comment identifier des comportements suspects sur un système  

---

**Résumé :**  
Ce module ne concerne pas l’espionnage — il s’agit de **comprendre les risques réels et d’apprendre à mieux se protéger dans le monde numérique.**
"""
}
