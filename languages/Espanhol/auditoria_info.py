# docs/trojan_info.py (or auditoria_info.py)

INFO = {
"titulo": "🛡️ Auditoría del Sistema",
"descricao": """

# 🛡️ Verificación de Seguridad del Sistema

---

## 👋 ¿Qué hace esta función?

Este módulo realiza un **chequeo de seguridad en tu computadora**.

Analiza configuraciones importantes e intenta identificar posibles puntos débiles que podrían ser explotados.

---

## 🔍 ¿Qué verifica AURA?

Durante la auditoría, AURA analiza:

* 🔑 **Permisos del sistema**  
  Verifica si el programa se está ejecutando con privilegios elevados (Admin/Root)

* 📂 **Directorios del sistema**  
  Busca ubicaciones donde cualquiera pueda escribir archivos (lo cual puede ser peligroso)

* 🌐 **Puertos abiertos**  
  Detecta servicios en ejecución en tu computadora que pueden estar expuestos

* ⚙️ **Procesos activos**  
  Busca programas sospechosos ejecutándose en segundo plano

* 🔥 **Firewall**  
  Verifica si la protección del sistema está activa

* 📄 **Archivo de red (hosts)**  
  Analiza posibles cambios que pueden indicar redirecciones maliciosas

---

## 🧠 ¿Por qué es importante?

Muchos problemas de seguridad no están en ataques complejos, sino en:

👉 configuraciones incorrectas  
👉 permisos demasiado abiertos  
👉 servicios innecesarios en ejecución  

Este módulo te ayuda a identificar eso de forma simple.

---

## 📊 ¿Cómo entender los resultados?

AURA clasifica todo de forma clara:

* 🔴 **[ALTO]** → riesgo importante, necesita atención  
* 🟡 **[MEDIO]** → puede mejorarse  
* 🟢 **[OK]** → todo está bien  

---

## 🚀 ¿Cuándo usarlo?

Puedes ejecutar esta auditoría para:

* verificar si tu sistema es seguro  
* entender mejor cómo funciona la seguridad local  
* aprender en la práctica sobre configuraciones del sistema  

---

## ⚠️ Nota importante

Este análisis es **local** (en tu propio sistema).  
No modifica nada — solo analiza e informa.

---

## 💡 Consejo para principiantes

Usa este módulo como un “termómetro”:

👉 ejecútalo  
👉 observa los resultados  
👉 investiga cada elemento  

Esto acelera MUCHO tu aprendizaje.

---

**La seguridad comienza entendiendo tu propio sistema.**
"""
}
