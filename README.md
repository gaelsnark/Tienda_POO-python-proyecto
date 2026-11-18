# Tienda sixseven: punto de venta en Python

Aplicación de escritorio para registrar ventas en una tienda de conveniencia. Hecha en **Python** con interfaz gráfica en **Tkinter** y persistencia en **SQLite**. Es el proyecto final del curso de programación en Python.

## Funcionalidades

- **Catálogo de 32 productos** (electrónicos, alimentos y bebidas, y otros), cada uno con su ID, nombre, precio y stock.
- **Venta por ID y cantidad**: valida que el producto exista y que haya stock suficiente, y luego descuenta el inventario.
- **Historial de ventas** guardado en una base de datos SQLite (`tienda.db`), que se crea automáticamente.
- **Registro de errores** con fecha y hora en `log_errores.txt` (por ejemplo, entradas no numéricas o fallos de la base de datos).
- Interfaz con botones para *Realizar venta*, *Ver productos*, *Ver historial* y *Salir*.

## Conceptos aplicados

- Programación orientada a objetos: clases `Almacenamiento`, `Inventario`, `LineaVenta`, `Venta` y `Aplicacion`.
- Encapsulamiento con atributos privados y métodos *getter*.
- `Enum` como catálogo de productos con valores fijos.
- SQLite: creación de tablas, inserciones con parámetros (`?`) y consultas.
- Manejo de excepciones (`try/except`) y escritura de archivos.
- Interfaz gráfica con Tkinter (`Label`, `Entry`, `Button`, `Text` y `messagebox`).

## Cómo ejecutarlo

Solo usa la biblioteca estándar de Python, así que no hay que instalar nada:

```bash
python3 tienda_sixseven.py
```

> Requiere Python 3 con Tkinter, que viene incluido en las instalaciones oficiales de python.org.

## Autor

**Santiago Gael Durán Ramírez**. Estudiante de Ingeniería en Tecnologías de Información y Negocios Digitales en la Universidad Anáhuac Querétaro.
