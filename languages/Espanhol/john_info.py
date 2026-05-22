# docs/john_info.py

INFO = {
"titulo": "💀 DESCIFRADO DE HASHES (JOHN THE RIPPER ENGINE)",
"descricao": """

# 🔐 Prueba de Seguridad de Contraseñas

---

## 👋 ¿Qué hace esta función?

Este módulo te permite **probar la seguridad de contraseñas protegidas (hashes)**.

En lugar de trabajar con la contraseña original, analiza el hash — que es una representación cifrada de la contraseña.

---

## 🧠 ¿Qué es un hash?

Un hash es una forma de transformar una contraseña en un código único.

Por ejemplo:

👉 contraseña: `123456`  
👉 hash: `e10adc3949ba59abbe56e057f20f883e`  

Los sistemas utilizan hashes para proteger las contraseñas.

---

## 🔍 ¿Qué hace AURA?

AURA intenta determinar si una contraseña es débil probando:

* 📚 **Listas de contraseñas comunes**  
  (contraseñas ya conocidas y ampliamente utilizadas)

* 🔄 **Variaciones automáticas**  
  (como agregar números o modificar letras)

* 🔢 **Combinaciones posibles**  
  (cuando defines un patrón)

👉 Esto simula lo que haría un atacante — pero de forma controlada.

---

## 🧠 ¿Por qué es importante?

Si una contraseña puede descubrirse rápidamente, se considera débil.

Esta prueba te ayuda a entender:

* si una contraseña es fácil de adivinar  
* si necesita ser más fuerte  
* cómo mejorar la protección del sistema  

---

## 📊 ¿Qué verás?

AURA muestra:

* si la contraseña fue descifrada o no  
* qué método se utilizó  
* cuánto esfuerzo fue necesario  

---

## 🚀 ¿Cuándo deberías usarlo?

Este módulo es útil para:

* aprender sobre la seguridad de contraseñas  
* probar hashes en entornos controlados  
* validar la fortaleza de las credenciales  

---

## ⚠️ Uso responsable

Esta función debe usarse solo en:

✔️ tus propias pruebas  
✔️ entornos de laboratorio  
✔️ sistemas autorizados  

❌ Nunca la utilices para acceder a cuentas de otras personas.

---

## 💡 Consejo para principiantes

Prueba con:

* hashes de contraseñas simples  
* ejemplos de laboratorio  
* tus propios datos  

👉 Esto te ayuda a entender cómo las contraseñas pueden ser protegidas (o descifradas).

---

## 🧠 Entiende el concepto

Las contraseñas débiles son una de las mayores fallas de seguridad.

👉 Cuanto más difícil sea adivinarla, más segura será.

---

**Una contraseña fuerte es tu primera línea de defensa.**
"""
}
