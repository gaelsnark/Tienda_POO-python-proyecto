import sqlite3
from enum import Enum
import datetime # Eso sirve para la fecha y hora del error
# Librerías para interfaz gráfica:
import tkinter as tk
from tkinter import messagebox

# Esta función abre el archivo de errores en modo "a" (a de append). No borra lo que ya estaba escrito, solo agrega al final (por el "a")
def registrar_error(mensaje):
    archivo = open("log_errores.txt", "a")
    fecha_actual = datetime.datetime.now()
    archivo.write(f"[{fecha_actual}] ERROR: {mensaje}\n")
    archivo.close()

# clase~
class Almacenamiento:
    def __init__(self):
# esto crea conexión y cursor
        self.conexion = sqlite3.connect("tienda.db")
        self.cursor = self.conexion.cursor()

# Crea tabla si es que no existe
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS ventas_historial (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                producto TEXT,
                total REAL
            )
        """)
        self.conexion.commit()

    def guardar(self, nombre_p, total_p):

        try:
            self.cursor.execute(
                "INSERT INTO ventas_historial (producto, total) VALUES (?, ?)", # Los signos de ? son para decir
                # que ahí van valores pero aún no se sabe cuáles son, o que incluso son valores cambiantes
                (nombre_p, total_p)
            )

            self.conexion.commit()

        except sqlite3.Error as e:
            registrar_error(f"Error en SQLite al guardar: {e}")
            print(f"Error al guardar en base de datos")

    def mostrar_todo(self):
        try:
            self.cursor.execute("SELECT * FROM ventas_historial")
            filas = self.cursor.fetchall() # fetchall es para ver lo guardado
                # cada f es una tupla, f[0] es el id, f[1] el producto, f[2] el total (una tupla es como una tabla, lista o un tipo arreglo)

            return filas
        except sqlite3.Error as e:
            registrar_error(f"Error en SQLite al mostrar: {e}")
            return [] # Si es que ocurre un error, la fución regresa una lista vacía



# clase producto con 32 objetos
class Producto(Enum): # Enum sirve para tener valores fijos, como un tipo catálogo

    # Electrónicos
    LAPTOP = (1, "Laptop", 15000)
    MOUSE = (2, "Mouse", 350)
    TECLADO = (3, "Teclado", 800)
    CARGADOR = (32, "Cable USB", 80)
    PILAS = (19, "Pilas AA", 40)

    # Alimentos y bebidas
    COCA_COLA = (4, "Coca-Cola 600ml", 18)
    AGUA = (5, "Agua Ciel 1L", 15)
    JUGO = (6, "Jugo Valle", 20)
    PAPAS = (7, "Sabritas", 17)
    GALLETAS = (8, "Chokis", 15)
    GANSITO = (9, "Gansito", 12)
    LECHE = (10, "Leche Lala 1L", 26)
    HUEVO = (11, "Cartera Huevo", 45)
    PAN = (12, "Pan Bimbo", 38)
    AZUCAR = (13, "Azucar 1kg", 28)
    FRIJOL = (14, "Frijol Isadora", 22)
    ACEITE = (15, "Aceite 1L", 40)
    PASTA = (17, "Pasta Colgate", 35)
    PAPEL = (18, "Papel", 25)
    MARUCHAN = (22, "Maruchan", 15)
    CLORETS = (23, "Chicles clorets", 10)
    CAFE = (24, "Andatti", 22)
    DONA = (25, "Dona de chocolate", 18)
    SANDWICH = (26, "Sandwich", 35)
    HOTDOG = (27, "Vikingo", 25)
    PALETA = (28, "Magnum", 35)
    YOGURT = (29, "Oikos", 18)
    ATUN = (30, "Atun", 22)
    SUERO = (31, "Electrolit", 32)

    # Otros
    ENCENDEDOR = (20, "Encendedor", 15)
    HIELO = (21, "Bolsa Hielo", 30)
    JABON = (16, "Jabón", 15)

    # __init__ en un Enum se llama automáticamente con los valores de nuetra tupla
    # es por eso que recibe id, nombre y precio (en ese orden) que son los 3 valores de cada producto
    def __init__(self, id, nombre, precio):
        self.__id = id
        self.__nombre = nombre
        self.__precio = precio
        self.__stock = 20  # Stock inicial parejo

    def getNombre(self): return self.__nombre
    def getPrecio(self): return self.__precio
    def getStock(self): return self.__stock
    def getId(self): return self.__id
    def ajustarStock(self, cant): self.__stock -= cant

# clase inventario
class Inventario:
    def buscar_producto(self, id_buscado):
        # Recorre todos los productos del Enum hasta encontrar el id (por el p in Producto)
        # si no lo encuentra regresa None
        for p in Producto:
            if p.getId() == id_buscado: # si es que lo encuentra
                return p
        return None

# clase linea venta
class LineaVenta:
    # representa un renglón del ticket
    def __init__(self, producto, cantidad):
        self.producto = producto # un producto
        self.cantidad = cantidad # con su cantidad
        self.subtotal = producto.getPrecio() * cantidad # Más su subtotal

# clase venta
class Venta:
    def __init__(self):
        self.lista_lineas = []

    def agregar(self, prod, cant):
        # Revisa si hay stock antes de agregar
        if prod.getStock() >= cant:
            nueva_linea = LineaVenta(prod, cant)
            self.lista_lineas.append(nueva_linea)
            prod.ajustarStock(cant)
            return True
        return False

# clase de la aplicación
class Aplicacion:
    def __init__(self, root):
        self.db = Almacenamiento()
        self.inv = Inventario()
        self.root = root
        self.root.title("Tienda sixseven")
        self.root.geometry("400x500")
        self.root.resizable(False, False)  # No se puede agrandar ni reducir

        #entradas
        tk.Label(self.root, text="ID del producto:").pack(pady=5)
        self.entryID = tk.Entry(self.root, width=30)
        self.entryID.pack()

        tk.Label(self.root, text="Cantidad:").pack(pady=5)
        self.entryCantidad = tk.Entry(self.root, width=30)
        self.entryCantidad.pack()

        # botones
        tk.Button(self.root, text="Realizar venta", command=self.realizarVenta).pack(pady=10)
        tk.Button(self.root, text="Ver productos", command=self.verProductos).pack(pady=5)
        tk.Button(self.root, text="Ver historial", command=self.verHistorial).pack(pady=5)
        tk.Button(self.root, text="Salir", command=self.salir).pack(pady=5)

        # área de texto para mostrar los resultados
        self.areaTexto = tk.Text(self.root, height=12)
        self.areaTexto.pack(pady=10)

    def realizarVenta(self):
        try:
            id_buscado = int(self.entryID.get())
            cantidad = int(self.entryCantidad.get())

            encontrado = self.inv.buscar_producto(id_buscado)
            v = Venta()
            if encontrado and v.agregar(encontrado, cantidad):
                total = encontrado.getPrecio() * cantidad
                self.db.guardar(encontrado.getNombre(), total)
                messagebox.showinfo("Venta exitosa", encontrado.getNombre() + " x" + str(cantidad) + " = $" + str(total))
                self.entryID.delete(0, tk.END)
                self.entryCantidad.delete(0, tk.END)
            else:
                messagebox.showwarning("Error", "Producto no existe o sin stock")

        except ValueError:
            registrar_error("Entrada no numerica en venta")
            messagebox.showerror("Error", "Ingresa solo numeros")

    def verProductos(self):
        # limpia el área de texto y muestra todos los productos
        self.areaTexto.delete("1.0", tk.END)
        for p in Producto:
            self.areaTexto.insert(tk.END, str(p.getId()) + ". " + p.getNombre() + " - $" + str(p.getPrecio()) + "\n")

    def verHistorial(self):
        # limpia el área de texto y muestra el historial de ventas
        self.areaTexto.delete("1.0", tk.END)
        filas = self.db.mostrar_todo()
        for f in filas:
            self.areaTexto.insert(tk.END, "ID:" + str(f[0]) + " | " + f[1] + " | $" + str(f[2]) + "\n")

    def salir(self):
        if messagebox.askyesno("Salir", "¿Deseas salir?"):
            self.db.conexion.close()
            self.root.destroy()


# main
def main():
    root = tk.Tk()
    app = Aplicacion(root)
    root.mainloop()

if __name__ == "__main__":
    main()