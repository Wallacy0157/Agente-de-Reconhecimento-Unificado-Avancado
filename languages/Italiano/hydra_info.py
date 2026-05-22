INFO = {
    "titulo": "🧰 TEST DELLE CREDENZIALI (HYDRA)",
    "descricao": """
# 🧰 Test di Password e Accessi

Questo modulo di AURA ti permette di testare la sicurezza dei sistemi che utilizzano l’autenticazione con nome utente e password.  
Simula tentativi di accesso per verificare se le credenziali sono facili da indovinare.

In pratica, aiuta a rispondere a una domanda semplice:  
👉 *“Questa password è davvero sicura?”*

---

### 🔎 Cosa fa questo modulo?

In parole semplici:

* testa combinazioni di nomi utente e password su un sistema  
* può utilizzare liste di password comuni (wordlist)  
* simula automaticamente molteplici tentativi di accesso  
* mostra se sono state trovate credenziali valide  

Questo è ampiamente utilizzato negli audit per identificare **password deboli o prevedibili**.

---

### ⚙️ Come funziona nella pratica?

Il modulo può operare in due modalità principali:

* **Password singola:** testare un utente con una password specifica  
* **Lista di password:** testare automaticamente più combinazioni  

Può inoltre funzionare con diversi tipi di sistemi, come:

* Accesso remoto (es. SSH, FTP)  
* Sistemi interni  
* Siti web con pagine di login  

---

### 🚀 Esecuzione efficiente

AURA accelera i test utilizzando:

* Tentativi simultanei multipli (parallelismo)  
* Interruzione automatica quando viene trovata una password valida  
* Visualizzazione del progresso in tempo reale  

Questo ti permette di verificare rapidamente se un sistema è protetto o meno.

---

### ⚠️ Uso responsabile ed etica

Questo modulo deve essere utilizzato con estrema cautela:

* ❌ Non testare mai sistemi senza autorizzazione  
* ❌ Non utilizzarlo su reti o server di terze parti  
* ✅ Usalo solo nel tuo laboratorio o ambiente  
* ✅ Ideale per apprendimento e test di sicurezza  

---

### 💡 Perché è importante?

Molti attacchi reali sfruttano password deboli.

Con questo modulo impari:

* Come funzionano gli attacchi di forza bruta  
* Perché le password semplici sono pericolose  
* Come implementare politiche di password più sicure  
* L’importanza di protezioni come il blocco dopo tentativi multipli (es. Fail2Ban)  

---

**Riassunto:**  
Questo modulo non serve per attaccare sistemi, ma per **testare e rafforzare la sicurezza dei login**, aiutando a prevenire accessi non autorizzati.
"""
}
