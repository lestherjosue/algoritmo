import sys
import pandas as pd
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QTabWidget


# Clases de gestión

class ClienteManager:
    def __init__(self):
        self.clientes = []

    def crear_cliente(self, codigo, nombre, direccion):
        cliente = {"codigo": codigo, "nombre": nombre, "direccion": direccion}
        self.clientes.append(cliente)

    def listar_clientes(self):  
        return self.clientes

    def editar_cliente(self, codigo, nuevo_nombre, nueva_direccion):
        for cliente in self.clientes:
            if cliente["codigo"] == codigo:
                cliente["nombre"] = nuevo_nombre
                cliente["direccion"] = nueva_direccion
                break

    def eliminar_cliente(self, codigo):
        self.clientes = [cliente for cliente in self.clientes if cliente["codigo"] != codigo]


class Producto:
    def __init__(self, codigo, nombre, existencia, proveedor, precio):
        self.codigo = codigo
        self.nombre = nombre
        self.existencia = existencia
        self.proveedor = proveedor
        self.precio = precio

    def __str__(self):
        return f"Código: {self.codigo}, Nombre: {self.nombre}, Existencia: {self.existencia}, Proveedor: {self.proveedor}, Precio: {self.precio} USD"


class Inventario:
    def __init__(self):
        self.productos = []

    def agregar_producto(self, producto):
        self.productos.append(producto)

    def listar_productos(self):
        return self.productos

    def actualizar_producto(self, codigo, nombre=None, existencia=None, proveedor=None, precio=None):
        for producto in self.productos:
            if producto.codigo == codigo:
                if nombre:
                    producto.nombre = nombre
                if existencia is not None:
                    producto.existencia = existencia
                if proveedor:
                    producto.proveedor = proveedor
                if precio is not None:
                    producto.precio = precio
                return

    def eliminar_producto(self, codigo):
        self.productos = [producto for producto in self.productos if producto.codigo != codigo]


class Ventas:
    def __init__(self):
        self.df = pd.DataFrame(columns=['cliente', 'producto', 'cantidad', 'precio_unitario'])
        self.cargar_ventas()  # Asegúrate de cargar las ventas al inicializar la clase

    def cargar_ventas(self):
        try:
            self.df = pd.read_excel('Ventas.xlsx')
        except FileNotFoundError:
            print("Archivo 'Ventas.xlsx' no encontrado. Se creará uno nuevo.")

    def agregar_venta(self, cliente, producto, cantidad, precio_unitario):
        nueva_venta = pd.DataFrame([{'cliente': cliente, 'producto': producto, 'cantidad': cantidad, 'precio_unitario': precio_unitario}])
        self.df = pd.concat([self.df, nueva_venta], ignore_index=True)  # Usa pd.concat en lugar de append

    def guardar_ventas(self):
        self.df.to_excel('Ventas.xlsx', index=False)


# Clase principal de la interfaz gráfica

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestión de Ventas")

        # Instanciar gestores
        self.cliente_manager = ClienteManager()
        self.inventario = Inventario()
        self.ventas = Ventas()

        # Inicializar UI
        self.init_ui()

    def init_ui(self):
        self.tabs = QTabWidget(self)
        self.setCentralWidget(self.tabs)

        # Tab de Clientes
        self.cliente_tab = QtWidgets.QWidget()
        self.tabs.addTab(self.cliente_tab, "Clientes")
        self.cliente_layout = QVBoxLayout()
        self.cliente_tab.setLayout(self.cliente_layout)

        self.form_cliente = QFormLayout()
        self.codigo_cliente_input = QLineEdit()
        self.nombre_cliente_input = QLineEdit()
        self.direccion_cliente_input = QLineEdit()
        self.form_cliente.addRow("Código:", self.codigo_cliente_input)
        self.form_cliente.addRow("Nombre:", self.nombre_cliente_input)
        self.form_cliente.addRow("Dirección:", self.direccion_cliente_input)
        self.cliente_layout.addLayout(self.form_cliente)

        self.btn_crear_cliente = QPushButton('Crear Cliente')
        self.btn_crear_cliente.clicked.connect(self.crear_cliente)
        self.cliente_layout.addWidget(self.btn_crear_cliente)

        # Tab de Productos
        self.producto_tab = QtWidgets.QWidget()
        self.tabs.addTab(self.producto_tab, "Productos")
        self.producto_layout = QVBoxLayout()
        self.producto_tab.setLayout(self.producto_layout)

        self.form_producto = QFormLayout()
        self.codigo_producto_input = QLineEdit()
        self.nombre_producto_input = QLineEdit()
        self.existencias_producto_input = QLineEdit()
        self.proveedor_producto_input = QLineEdit()
        self.precio_producto_input = QLineEdit()
        self.form_producto.addRow("Código:", self.codigo_producto_input)
        self.form_producto.addRow("Nombre:", self.nombre_producto_input)
        self.form_producto.addRow("Existencias:", self.existencias_producto_input)
        self.form_producto.addRow("Proveedor:", self.proveedor_producto_input)
        self.form_producto.addRow("Precio:", self.precio_producto_input)
        self.producto_layout.addLayout(self.form_producto)

        self.btn_crear_producto = QPushButton('Crear Producto')
        self.btn_crear_producto.clicked.connect(self.crear_producto)
        self.producto_layout.addWidget(self.btn_crear_producto)

        # Tab de Ventas
        self.venta_tab = QtWidgets.QWidget()
        self.tabs.addTab(self.venta_tab, "Ventas")
        self.venta_layout = QVBoxLayout()
        self.venta_tab.setLayout(self.venta_layout)

        self.form_venta = QFormLayout()
        self.cliente_venta_input = QLineEdit()
        self.producto_venta_input = QLineEdit()
        self.cantidad_venta_input = QLineEdit()
        self.precio_venta_input = QLineEdit()
        self.form_venta.addRow("Cliente:", self.cliente_venta_input)
        self.form_venta.addRow("Producto:", self.producto_venta_input)
        self.form_venta.addRow("Cantidad:", self.cantidad_venta_input)
        self.form_venta.addRow("Precio Unitario:", self.precio_venta_input)
        self.venta_layout.addLayout(self.form_venta)

        self.btn_agregar_venta = QPushButton('Agregar Venta')
        self.btn_agregar_venta.clicked.connect(self.agregar_venta)
        self.venta_layout.addWidget(self.btn_agregar_venta)

    def crear_cliente(self):
        codigo = self.codigo_cliente_input.text()
        nombre = self.nombre_cliente_input.text()
        direccion = self.direccion_cliente_input.text()

        if codigo and nombre and direccion:
            self.cliente_manager.crear_cliente(codigo, nombre, direccion)
            QMessageBox.information(self, "Éxito", "Cliente creado exitosamente.")
            self.limpiar_campos_cliente()
        else:
            QMessageBox.warning(self, "Error", "Por favor, complete todos los campos.")

    def limpiar_campos_cliente(self):
        self.codigo_cliente_input.clear()
        self.nombre_cliente_input.clear()
        self.direccion_cliente_input.clear()

    def crear_producto(self):
        codigo = self.codigo_producto_input.text()
        nombre = self.nombre_producto_input.text()
        existencia = self.existencias_producto_input.text()
        proveedor = self.proveedor_producto_input.text()
        precio = self.precio_producto_input.text()

        if codigo and nombre and existencia and proveedor and precio:
            producto = Producto(codigo, nombre, int(existencia), proveedor, float(precio))
            self.inventario.agregar_producto(producto)
            QMessageBox.information(self, "Éxito", "Producto creado exitosamente.")
            self.limpiar_campos_producto()
        else:
            QMessageBox.warning(self, "Error", "Por favor, complete todos los campos.")

    def limpiar_campos_producto(self):
        self.codigo_producto_input.clear()
        self.nombre_producto_input.clear()
        self.existencias_producto_input.clear()
        self.proveedor_producto_input.clear()
        self.precio_producto_input.clear()

    def agregar_venta(self):
        cliente = self.cliente_venta_input.text()
        producto = self.producto_venta_input.text()
        cantidad = self.cantidad_venta_input.text()
        precio_unitario = self.precio_venta_input.text()

        if cliente and producto and cantidad and precio_unitario:
            self.ventas.agregar_venta(cliente, producto, int(cantidad), float(precio_unitario))
            self.ventas.guardar_ventas()
            QMessageBox.information(self, "Éxito", "Venta agregada exitosamente.")
            self.limpiar_campos_venta()
        else:
            QMessageBox.warning(self, "Error", "Por favor, complete todos los campos.")

    def limpiar_campos_venta(self):
        self.cliente_venta_input.clear()
        self.producto_venta_input.clear()
        self.cantidad_venta_input.clear()
        self.precio_venta_input.clear()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.resize(600, 400)
    window.show()
    sys.exit(app.exec_())
