# 🍾 Licorera Inteligente

Sistema de gestión para licoreras de barrio en Colombia.
Controla inventario, ventas, domicilios y genera reportes automáticos.

---

## ✅ Requisitos previos

Necesitas tener instalado en tu computador:

- **Python 3.10 o superior** → Descarga en: https://www.python.org/downloads/
  - ⚠️ Al instalar Python en Windows, marca la casilla **"Add Python to PATH"**
- **Git** (opcional) → https://git-scm.com/

---

## 🚀 Instalación paso a paso

### Paso 1 — Abre la terminal

- **Windows:** Busca "CMD" o "Símbolo del sistema" en el menú inicio
- **Mac/Linux:** Abre la app "Terminal"

---

### Paso 2 — Ve a la carpeta del proyecto

Si descargaste el proyecto como ZIP, descomprímelo. Luego escribe en la terminal:

```bash
cd ruta/a/licorera_inteligente
```

Por ejemplo en Windows:
```
cd C:\Users\TuNombre\Desktop\licorera_inteligente
```

---

### Paso 3 — Crea un entorno virtual

Un entorno virtual es una "caja" donde se instalan las librerías sin afectar tu computador.

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

Sabrás que está activo porque verás `(venv)` al inicio de la línea de la terminal.

---

### Paso 4 — Instala las dependencias

```bash
pip install -r requirements.txt
```

Esto descarga Flask y todo lo necesario. Puede tardar 1-2 minutos.

---

### Paso 5 — Ejecuta la aplicación

```bash
python app.py
```

Verás algo como:
```
✅ Base de datos inicializada correctamente.
 * Running on http://127.0.0.1:5000
```

---

### Paso 6 — Abre el navegador

Ve a: **http://127.0.0.1:5000**

---

## 🔐 Usuarios por defecto

| Usuario    | Contraseña | Rol           |
|------------|------------|---------------|
| `admin`    | `admin123` | Administrador |
| `empleado` | `emp123`   | Empleado      |

⚠️ **Cambia las contraseñas** después de tu primera entrada.

---

## 📁 Estructura del proyecto

```
licorera_inteligente/
├── app.py                  ← Punto de entrada principal
├── database.py             ← Configuración de la base de datos
├── requirements.txt        ← Librerías necesarias
├── models/
│   ├── user.py             ← Modelo de usuarios
│   ├── product.py          ← Modelo de inventario
│   ├── sale.py             ← Modelo de ventas
│   └── delivery.py         ← Modelo de domicilios
├── routes/
│   ├── auth.py             ← Rutas de autenticación
│   ├── inventory.py        ← Rutas de inventario
│   ← sales.py             ← Rutas de ventas
│   ├── deliveries.py       ← Rutas de domicilios
│   ├── dashboard.py        ← Dashboard e inteligencia
│   └── reports.py          ← Reportes y PDF
├── templates/              ← Páginas HTML
│   ├── base.html
│   ├── auth/
│   ├── dashboard/
│   ├── inventory/
│   ├── sales/
│   ├── deliveries/
│   └── reports/
└── static/
    ├── css/style.css       ← Diseño visual
    └── js/main.js          ← JavaScript
```

---

## 🛑 Cómo detener la aplicación

En la terminal donde corre el servidor, presiona **Ctrl + C**.

---

## ❓ Problemas comunes

**"python no se reconoce como comando"**
→ Reinstala Python y marca "Add to PATH". O usa `python3` en Mac/Linux.

**"No module named flask"**
→ Asegúrate de tener el entorno virtual activo (debe decir `(venv)`) y ejecuta `pip install -r requirements.txt` de nuevo.

**Puerto 5000 ocupado**
→ Cambia el puerto en `app.py`: `app.run(port=5001)`

---

## 💡 Consejos de uso

1. **Empieza por el Inventario** — agrega tus productos reales
2. **Usa Nueva Venta** para registrar cada venta del día
3. **Revisa el Dashboard** cada mañana para ver el resumen
4. **Los Reportes** te dan el PDF para tu contabilidad
5. **Domicilios** te ayuda a rastrear pedidos en tiempo real
