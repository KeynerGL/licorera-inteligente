# 🍾 Licorera Inteligente

Sistema de gestión completo para licoreras de barrio en Colombia.
Controla inventario, ventas, domicilios, caja diaria y tienda online.

---

## 🌐 URL de la aplicación

| Acceso | URL |
|---|---|
| **Panel Admin** | `licorera-inteligente-production.up.railway.app` |
| **Tienda Online** | `licorera-inteligente-production.up.railway.app/store` |

---

## 🔐 Usuarios del sistema

| Usuario | Contraseña | Rol |
|---|---|---|
| `admin` | *(tu contraseña)* | Administrador |
| `empleado` | *(tu contraseña)* | Empleado |

⚠️ **Nunca compartas las contraseñas.**

---

## ✅ Funcionalidades

### 📦 Inventario
- Agregar, editar y eliminar productos
- Categorías: Cerveza, Aguardiente, Ron, Whisky, Vino, Snacks y Otros
- Alertas de stock bajo automáticas
- Fotos de productos con URL

### 💰 Ventas
- Registrar ventas con carrito
- Descuento automático del inventario
- Cálculo de ganancias en tiempo real
- Historial de ventas con filtros
- Anular ventas (restaura el inventario)

### 🛵 Domicilios
- Registrar pedidos a domicilio
- Estados: Pendiente, En camino, Entregado
- Al marcar como Entregado → descuenta inventario y registra venta automáticamente

### 🛒 Tienda Online
- Catálogo de productos con fotos
- Carrito de compras
- Pedidos llegan directo a Domicilios
- Accesible desde cualquier celular

### 📊 Dashboard
- Ventas del día y del mes
- Ganancia neta
- Productos más vendidos
- Productos con stock bajo
- Gráficas de los últimos 7 días
- Recomendaciones automáticas de inteligencia de negocio

### 📈 Reportes
- Reporte diario, semanal y mensual
- Rango de fechas personalizado
- Exportar a PDF

### 💰 Caja Diaria
- Apertura de caja con efectivo inicial
- Cierre de caja con conteo de efectivo
- Detecta diferencias automáticamente
- Historial de cajas

### 📱 Notificaciones WhatsApp
- Alerta automática cuando un producto tiene stock bajo
- Configurado con Twilio Sandbox

### 👥 Usuarios
- Roles: Administrador y Empleado
- Activar/desactivar usuarios
- Contraseñas hasheadas de forma segura

### 🔒 Seguridad
- HTTPS activado por Railway
- Contraseñas hasheadas con Werkzeug
- Login obligatorio para el panel admin
- Protección anti-spam en la tienda
- Protección anti-fuerza bruta en el login

---

## 🏗️ Estructura del proyecto

```
licorera_inteligente/
├── app.py                    ← Punto de entrada principal
├── database.py               ← Configuración base de datos
├── extensions.py             ← Flask-Limiter (seguridad)
├── requirements.txt          ← Librerías necesarias
├── Procfile                  ← Configuración Railway
├── migrate.py                ← Script de migraciones
├── models/
│   ├── user.py               ← Usuarios y autenticación
│   ├── product.py            ← Inventario
│   ├── sale.py               ← Ventas
│   ├── delivery.py           ← Domicilios
│   └── cashregister.py       ← Caja diaria
├── routes/
│   ├── auth.py               ← Login y usuarios
│   ├── inventory.py          ← Inventario
│   ├── sales.py              ← Ventas
│   ├── deliveries.py         ← Domicilios
│   ├── dashboard.py          ← Dashboard e inteligencia
│   ├── reports.py            ← Reportes y PDF
│   ├── store.py              ← Tienda online
│   └── cashregister.py       ← Caja diaria
├── utils/
│   └── whatsapp.py           ← Notificaciones WhatsApp
├── templates/                ← Páginas HTML
│   ├── base.html
│   ├── auth/
│   ├── dashboard/
│   ├── inventory/
│   ├── sales/
│   ├── deliveries/
│   ├── reports/
│   ├── store/
│   └── cashregister/
└── static/
    ├── css/style.css         ← Diseño visual
    ├── js/main.js            ← JavaScript
    └── img/favicon.ico       ← Ícono de la app
```

---

## 🚀 Tecnologías

| Tecnología | Uso |
|---|---|
| Python + Flask | Backend |
| SQLAlchemy | ORM base de datos |
| PostgreSQL | Base de datos en producción |
| SQLite | Base de datos local |
| Jinja2 | Plantillas HTML |
| Werkzeug | Seguridad contraseñas |
| Flask-Login | Sesiones de usuario |
| Flask-Limiter | Anti-spam y fuerza bruta |
| Twilio | Notificaciones WhatsApp |
| xhtml2pdf | Exportar reportes a PDF |
| Waitress | Servidor de producción |
| Railway | Hosting en la nube |
| Chart.js | Gráficas del dashboard |

---

## 🛠️ Instalación local

### Requisitos
- Python 3.10 o superior
- Git

### Pasos

```bash
# 1. Clonar el repositorio
git clone https://github.com/KeynerGL/licorera-inteligente.git
cd licorera-inteligente

# 2. Crear entorno virtual
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Ejecutar
python app.py
```

Abre: **http://127.0.0.1:5000**

---

## ☁️ Variables de entorno en Railway

| Variable | Descripción |
|---|---|
| `DATABASE_URL` | URL de PostgreSQL |
| `PORT` | Puerto (5000) |
| `TWILIO_ACCOUNT_SID` | Account SID de Twilio |
| `TWILIO_AUTH_TOKEN` | Auth Token de Twilio |
| `TWILIO_WHATSAPP_TO` | Tu número WhatsApp (+57XXXXXXXXXX) |

---

*Desarrollado con ❤️ para licoreras de barrio en Colombia 🇨🇴*