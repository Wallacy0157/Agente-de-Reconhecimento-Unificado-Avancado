# docs_vault/ddos_info.py

INFO = {
    "titulo": "PRUEBA DE CARGA (STRESS TEST)",
    "subtitulo": "Simulación de Tráfico y Resiliencia",
    "descricao": """

# 🔥 Prueba de Carga (Stress Test)

---

## 👋 ¿Qué hace esta función?

Esta parte de AURA te permite probar cómo se comporta un sistema cuando recibe muchas conexiones al mismo tiempo.

En pocas palabras:

👉 simulas **múltiples accesos simultáneos** para ver si el sistema puede soportarlo.

---

## 🧠 ¿Para qué sirve?

En ciberseguridad y desarrollo, es muy importante saber:

* ¿el sistema puede manejar muchos usuarios al mismo tiempo?  
* ¿se vuelve lento?  
* ¿deja de responder?  
* ¿el firewall bloquea el exceso de conexiones?  

👉 Esta prueba ayuda a responder estas preguntas.

---

## ⚙️ ¿Qué sucede durante la prueba?

Cuando la inicias:

* AURA envía múltiples solicitudes al objetivo  
* mide el tiempo de respuesta (latencia)  
* verifica si la conexión fue aceptada, bloqueada o caída  
* monitorea todo en tiempo real  

---

## 📊 ¿Qué vas a ver?

Durante la prueba, obtendrás información como:

* número total de conexiones enviadas  
* cuántas funcionaron normalmente  
* cuántas fueron bloqueadas o fallaron  
* tiempo promedio de respuesta  

---

## 🚀 ¿Cuándo deberías usar esto?

Puedes usar esta prueba para:

* evaluar la estabilidad de un servidor  
* probar reglas de firewall  
* validar límites de conexión  
* estudiar el comportamiento del sistema bajo alta carga  

---

## ⚠️ Uso responsable

Este tipo de prueba puede sobrecargar sistemas. Úsalo solo en:

✔️ tus propios servidores  

✔️ entornos de prueba  

✔️ sistemas con autorización  

❌ Nunca lo uses contra sistemas de terceros sin permiso.

---

## 💡 Consejo para principiantes

Comienza con **valores bajos** (pocas solicitudes) y aumenta gradualmente. Esto te ayudará a entender cómo reacciona el sistema sin causar problemas.

---

**Entender los límites del sistema es el primer paso para construir infraestructuras resilientes y seguras.**
"""
}
