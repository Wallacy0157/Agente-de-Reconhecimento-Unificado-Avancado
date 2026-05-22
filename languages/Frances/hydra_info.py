INFO = {
    "titulo": "🧰 TEST DES IDENTIFIANTS (HYDRA)",
    "descricao": """
# 🧰 Test des Mots de Passe et des Connexions

Ce module d’AURA vous permet de tester la sécurité des systèmes utilisant une authentification par identifiant et mot de passe.  
Il simule des tentatives d’accès afin de vérifier si les identifiants sont faciles à deviner.

En pratique, cela aide à répondre à une question simple :  
👉 *« Ce mot de passe est-il vraiment sécurisé ? »*

---

### 🔎 Que fait ce module ?

En termes simples, il :

* teste des combinaisons d’utilisateurs et de mots de passe sur un système  
* peut utiliser des listes de mots de passe courants (wordlists)  
* simule automatiquement plusieurs tentatives de connexion  
* indique si un identifiant valide a été trouvé  

Cela est largement utilisé dans les audits pour identifier des **mots de passe faibles ou prévisibles**.

---

### ⚙️ Comment cela fonctionne-t-il en pratique ?

Le module peut fonctionner de deux manières principales :

* **Mot de passe unique :** tester un utilisateur avec un mot de passe spécifique  
* **Liste de mots de passe :** tester automatiquement plusieurs combinaisons  

Il peut également fonctionner avec différents types de systèmes, tels que :

* Accès à distance (ex : SSH, FTP)  
* Systèmes internes  
* Sites web avec pages de connexion  

---

### 🚀 Exécution efficace

AURA accélère les tests en utilisant :

* Plusieurs tentatives simultanées (parallélisme)  
* Interruption automatique lorsqu’un mot de passe valide est trouvé  
* Affichage de la progression en temps réel  

Cela permet de tester rapidement si un système est protégé ou non.

---

### ⚠️ Utilisation responsable et éthique

Ce module doit être utilisé avec une extrême prudence :

* ❌ Ne testez jamais des systèmes sans autorisation  
* ❌ Ne l’utilisez pas sur des réseaux ou serveurs tiers  
* ✅ Utilisez-le uniquement dans votre propre laboratoire ou environnement  
* ✅ Idéal pour l’apprentissage et les tests de sécurité  

---

### 💡 Pourquoi est-ce important ?

De nombreuses attaques réelles exploitent des mots de passe faibles.

Avec ce module, vous apprenez :

* Comment fonctionnent les attaques par force brute  
* Pourquoi les mots de passe simples sont dangereux  
* Comment mettre en place des politiques de mots de passe plus sécurisées  
* L’importance de protections comme le blocage après plusieurs tentatives (ex : Fail2Ban)  

---

**Résumé :**  
Ce module n’est pas conçu pour infiltrer des systèmes, mais pour **tester et renforcer la sécurité des connexions**, afin de prévenir les accès non autorisés.
"""
}
