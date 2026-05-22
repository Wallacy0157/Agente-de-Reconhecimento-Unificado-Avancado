# docs/keylogger_info.py

INFO = {
    "titulo": "⌨️ AUDITORÍA DE ESCRITURA (KEYLOGGER)",
    "descricao": """
# ⌨️ Monitoreo de Teclas (Uso Controlado)

Este módulo de AURA te permite monitorear y registrar lo que se escribe en el teclado durante una sesión.  
En Ciberseguridad, esto se utiliza para **entender comportamientos, probar la seguridad y analizar actividades en entornos controlados**.

### 🔎 ¿Qué hace este módulo?

En pocas palabras,:

* Registra todo lo que se escribe durante el uso del sistema  
* Identifica en qué programa o ventana ocurrió la escritura  
* Organiza esta información en un archivo de registro (log)  
* Genera un pequeño resumen con estadísticas de la actividad  

Esto ayuda a entender **cómo un usuario interactúa con el sistema**, o incluso simular cómo funcionan ciertos tipos de ataques.

---

### 📊 Información recopilada

Durante la ejecución, AURA registra:

* Texto escrito  
* Cambios de ventana (ej.: navegador, terminal, etc.)  
* Cantidad total de teclas presionadas  
* Uso de teclas como Enter y Backspace  
* Teclas más utilizadas durante la sesión  

Todo esto se guarda automáticamente en la carpeta `/logs`.

---

### ⏱️ Funcionamiento inteligente

El sistema está diseñado para ser liviano:

* Guarda los datos en bloques (no escribe en cada tecla)  
* Detecta cuando el usuario está inactivo  
* Finaliza sesiones automáticamente después de largos periodos de inactividad  

---

### ⚠️ Uso responsable y ética

Este es un módulo extremadamente sensible.

* ❌ **Nunca lo uses en computadoras de otras personas sin autorización**  
* ❌ Monitorear a alguien sin consentimiento puede ser ilegal  
* ✅ Úsalo solo en tu propio entorno o laboratorio  
* ✅ Ideal para estudio y pruebas de seguridad  

---

### 💡 ¿Por qué es importante?

Herramientas como esta son utilizadas por atacantes para robar contraseñas e información.

Al entender cómo funcionan, aprendes:

* Cómo protegerte contra este tipo de amenaza  
* Por qué es importante usar gestores de contraseñas  
* Cómo identificar comportamientos sospechosos en un sistema  

---

**Resumen:**  
Este módulo no trata de espionaje — trata de **entender riesgos reales y aprender a protegerte mejor en el mundo digital.**
"""
}
