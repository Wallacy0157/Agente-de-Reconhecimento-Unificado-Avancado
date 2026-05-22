INFO = {
    "titulo": "🧰 PRUEBA DE CREDENCIALES (HYDRA)",
    "descricao": """
# 🧰 Prueba de Contraseñas y Logins

Este módulo de AURA te permite probar la seguridad de sistemas que utilizan autenticación con usuario y contraseña.  
Simula intentos de acceso para verificar si las credenciales son fáciles de adivinar.

En la práctica, esto ayuda a responder una pregunta simple:  
👉 *“¿Esta contraseña es realmente segura?”*

---

### 🔎 ¿Qué hace este módulo?

En pocas palabras,:

* Prueba combinaciones de usuarios y contraseñas en un sistema  
* Puede usar listas de contraseñas comunes (wordlists)  
* Simula múltiples intentos de inicio de sesión automáticamente  
* Muestra si se encontró alguna credencial válida  

Esto se utiliza ampliamente en auditorías para identificar **contraseñas débiles o predecibles**.

---

### ⚙️ ¿Cómo funciona en la práctica?

El módulo puede operar de dos formas principales:

* **Contraseña única:** probar un usuario con una contraseña específica  
* **Lista de contraseñas:** probar múltiples combinaciones automáticamente  

También puede trabajar con diferentes tipos de sistemas, como:

* Acceso remoto (ej.: SSH, FTP)  
* Sistemas internos  
* Sitios web con páginas de inicio de sesión  

---

### 🚀 Ejecución eficiente

AURA acelera las pruebas utilizando:

* Múltiples intentos simultáneos (paralelismo)  
* Interrupción automática cuando se encuentra una contraseña válida  
* Visualización del progreso en tiempo real  

Esto permite probar rápidamente si un sistema está protegido o no.

---

### ⚠️ Uso responsable y ética

Este módulo debe usarse con extremo cuidado:

* ❌ Nunca pruebes sistemas sin autorización  
* ❌ No lo utilices en redes o servidores de terceros  
* ✅ Úsalo solo en tu propio laboratorio o entorno  
* ✅ Ideal para pruebas de seguridad y aprendizaje  

---

### 💡 ¿Por qué es importante?

Muchos ataques reales explotan contraseñas débiles.

Con este módulo, aprendes:

* Cómo funcionan los ataques de fuerza bruta  
* Por qué las contraseñas simples son peligrosas  
* Cómo implementar políticas de contraseñas más seguras  
* La importancia de protecciones como el bloqueo por intentos (ej.: Fail2Ban)  

---

**Resumen:**  
Este módulo no está diseñado para invadir sistemas, sino para **probar y fortalecer la seguridad de los logins**, ayudando a prevenir accesos no autorizados.
"""
}
