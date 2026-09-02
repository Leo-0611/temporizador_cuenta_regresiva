# ⏳ Countdown Timer - Temporizador de Cuenta Regresiva

## 📌 Descripción

**Countdown Timer** es una aplicación de escritorio desarrollada completamente en **Python**, cuyo objetivo es permitir al usuario crear eventos futuros y visualizar una cuenta regresiva hasta la fecha y hora establecidas.

La aplicación muestra el tiempo restante en **días, horas, minutos y segundos**, actualizándose automáticamente cada segundo.

El proyecto está basado en la idea **Countdown Timer** de [App Ideas](https://github.com/florinpop17/app-ideas/blob/master/Projects/1-Beginner/Countdown-Timer-App.md).

---

## 🎯 Objetivo del proyecto

El objetivo principal es desarrollar un temporizador de cuenta regresiva utilizando las funciones integradas de Python para trabajar con fechas y horas, sin depender de bibliotecas externas.

Además, el proyecto busca practicar conceptos fundamentales de programación como:

* Variables.
* Funciones.
* Clases y objetos.
* Condicionales.
* Ciclos.
* Manejo de fechas y horas.
* Archivos JSON.
* Interfaces gráficas.
* Validación de datos.
* Control de versiones con Git y GitHub.

---

## ⚙️ Características

La aplicación permite:

* 📝 Introducir el nombre de un evento.
* 📅 Establecer una fecha para el evento.
* 🕐 Establecer una hora opcional.
* ⏱️ Visualizar días, horas, minutos y segundos restantes.
* 🔄 Actualizar automáticamente la cuenta regresiva.
* ⚠️ Mostrar advertencias cuando los datos son incorrectos.
* 💾 Guardar eventos para conservarlos entre sesiones.
* 📋 Visualizar eventos guardados.
* ▶️ Seleccionar un evento existente para iniciar su cuenta regresiva.
* 🗑️ Eliminar eventos.
* 🔔 Mostrar una alerta cuando llega el momento del evento.
* 📌 Permitir almacenar múltiples eventos.

---

## 🛠️ Tecnologías utilizadas

El proyecto fue desarrollado utilizando únicamente **Python** y sus módulos incluidos en la instalación estándar.

### Lenguaje

* **Python 3**

### Módulos utilizados

* `tkinter` → creación de la interfaz gráfica.
* `datetime` → manejo y cálculo de fechas y horas.
* `json` → almacenamiento de los eventos.
* `os` → manejo de archivos y comprobación de existencia.

### Control de versiones

* **Git**
* **GitHub**

---

## 🚫 Dependencias externas

Este proyecto **no utiliza paquetes externos instalados mediante `pip`**.

No se utilizan:

* CustomTkinter
* PyQt
* Kivy
* Pygame
* Pandas
* MomentJS
* Generadores automáticos de temporizadores

La aplicación utiliza exclusivamente herramientas disponibles dentro de Python.

---

## 📂 Estructura del proyecto

```text
countdown-timer/
│
├── main.py
├── events.json
├── README.md
└── .gitignore
```

### `main.py`

Contiene todo el código principal de la aplicación, incluyendo:

* Interfaz gráfica.
* Creación de eventos.
* Validación de datos.
* Cálculo de la cuenta regresiva.
* Guardado de eventos.
* Carga de eventos.
* Eliminación de eventos.

### `events.json`

Archivo utilizado para almacenar los eventos creados por el usuario.

### `README.md`

Documento que contiene la descripción, funcionamiento y características del proyecto.

---

## ▶️ Instalación y ejecución

### 1. Descargar o clonar el repositorio

```bash
git clone URL_DEL_REPOSITORIO
```

### 2. Entrar a la carpeta

```bash
cd countdown-timer
```

### 3. Ejecutar el programa

```bash
python main.py
```

En Windows también puede utilizarse:

```bash
py main.py
```

No es necesario ejecutar `pip install` para este proyecto.

---

## 🖥️ Funcionamiento

El usuario debe introducir:

**Nombre del evento**

```text
Mi cumpleaños
```

**Fecha**

```text
20/12/2026
```

**Hora**

```text
18:30
```

Después debe presionar el botón **INICIAR**.

La aplicación calculará automáticamente la diferencia entre la fecha actual y la fecha del evento.

Por ejemplo:

```text
MI CUMPLEAÑOS

110 : 08 : 32 : 15

DÍAS    HORAS    MINUTOS    SEGUNDOS
```

El contador se actualiza automáticamente cada segundo.

---

## 🧮 Cálculo del tiempo restante

Para calcular el tiempo restante se utiliza el módulo `datetime` incluido en Python.

Primero se obtiene la fecha y hora actual:

```python
datetime.now()
```

Después se calcula la diferencia entre la fecha actual y la fecha del evento:

```python
diferencia = fecha_evento - ahora
```

La diferencia se convierte a segundos:

```python
segundos_totales = int(diferencia.total_seconds())
```

Posteriormente los segundos se convierten en:

* Días.
* Horas.
* Minutos.
* Segundos.

De esta manera se consigue actualizar el temporizador continuamente sin utilizar bibliotecas externas.

---

## 💾 Persistencia de datos

Los eventos se almacenan en un archivo `events.json`.

Esto permite que los eventos permanezcan guardados incluso después de cerrar la aplicación.

Ejemplo:

```json
[
    {
        "nombre": "Cumpleaños",
        "fecha": "2026-12-20 18:30:00"
    },
    {
        "nombre": "Vacaciones",
        "fecha": "2027-07-15 00:00:00"
    }
]
```

---

## 📋 Historias de usuario implementadas

### Historia 1

El usuario puede introducir el nombre del evento.

### Historia 2

El usuario puede introducir una fecha.

### Historia 3

El usuario puede introducir una hora opcional.

### Historia 4

El sistema muestra una advertencia cuando el nombre está vacío.

### Historia 5

El sistema muestra una advertencia cuando la fecha u hora son incorrectas.

### Historia 6

El usuario puede iniciar una cuenta regresiva.

### Historia 7

El temporizador disminuye automáticamente cada segundo.

### Historia 8

El usuario puede guardar eventos.

### Historia 9

El usuario puede visualizar eventos guardados.

### Historia 10

El usuario puede eliminar eventos.

### Historia 11

El usuario recibe una alerta cuando llega el momento del evento.

---

## 🚀 Posibles mejoras futuras

Algunas características que podrían incorporarse posteriormente son:

* 🎨 Mejorar el diseño de la interfaz.
* 🌙 Incorporar modo oscuro.
* 🔔 Agregar diferentes tipos de notificaciones.
* 📊 Mostrar cada evento mediante una tarjeta independiente.
* ✏️ Permitir editar eventos.
* 🔎 Agregar búsqueda de eventos.
* 📌 Ordenar eventos por fecha.
* ⏰ Permitir configurar recordatorios.
* 🗓️ Incorporar un calendario.
* 🌎 Permitir seleccionar diferentes zonas horarias.

---

## 📚 Aprendizaje

Este proyecto permite poner en práctica conocimientos fundamentales de programación y desarrollo de software, especialmente en:

* Programación orientada a objetos.
* Interfaces gráficas.
* Manipulación de fechas.
* Persistencia de información.
* Validación de entradas.
* Manejo de archivos.
* Control de versiones.
* Uso de Git y GitHub.

---

## 👨‍💻 Autor

**Leonardo Orozco**

Proyecto desarrollado con fines académicos y de aprendizaje.

---

## 📄 Licencia

Este proyecto fue desarrollado con fines educativos.
