import sys
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QPushButton,
    QLineEdit,
    QLabel,
    QMessageBox,
    QTableWidget,
    QTableWidgetItem,
)

# Clases para manejar la lógica de clientes
class ClienteManager:
    def __init__(self):
        self.clientes = []

    def crear_cliente(self, codigo, nombre, direccion):
        cliente = {"codigo": codigo, "nombre": nombre, "direccion": direccion}
        self.clientes.append(cliente)

    def editar_cliente(self, codigo, nuevo_nombre, nueva_direccion):
        for cliente in self.clientes:
            if cliente["codigo"] == codigo:
                cliente["nombre"] = nuevo_nombre
                cliente["direccion"] = nueva_direccion
                break

    def eliminar_cliente(self, codigo):
        self.clientes = [cliente for cliente in self.clientes if cliente["codigo"] != codigo]

    def listar_clientes(self):
        return self.clientes

# Clases para manejar la lógica de productos
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
        """ Agregar un nuevo producto al inventario """
        self.productos.append(producto)

    def listar_productos(self):
        """ Mostrar todos los productos en inventario """
        return self.productos

    def actualizar_producto(self, codigo, nombre=None, existencia=None, proveedor=None, precio=None):
        """ Actualizar los detalles de un producto """
        for producto in self.productos:
            if producto.codigo == codigo:
                if nombre: producto.nombre = nombre
                if existencia is not None: producto.existencia = existencia
                if proveedor: producto.proveedor = proveedor
                if precio is not None: producto.precio = precio
                return
        raise ValueError(f"Producto con código {codigo} no encontrado.")

    def editar_existencias(self, codigo, nueva_existencia):
        """ Editar las existencias de un producto """
        for producto in self.productos:
            if producto.codigo == codigo:
                producto.existencia = nueva_existencia
                return
        raise ValueError(f"Producto con código {codigo} no encontrado.")

    def eliminar_producto(self, codigo):
        """ Eliminar un producto del inventario """
        for producto in self.productos:
            if producto.codigo == codigo:
                self.productos.remove(producto)
                return
        raise ValueError(f"Producto con código {codigo} no encontrado.")

# Clase principal de la interfaz gráfica
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestión de Clientes y Productos")
        self.setGeometry(100, 100, 800, 600)

        self.cliente_manager = ClienteManager()
        self.inventario = Inventario()

        # Crear un widget central y un layout vertical
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()

        # Tab para clientes
        layout.addWidget(QLabel("Gestión de Clientes"))
        self.codigo_cliente_input = QLineEdit(self)
        self.codigo_cliente_input.setPlaceholderText("Código del Cliente")
        layout.addWidget(self.codigo_cliente_input)

        self.nombre_cliente_input = QLineEdit(self)
        self.nombre_cliente_input.setPlaceholderText("Nombre del Cliente")
        layout.addWidget(self.nombre_cliente_input)

        self.direccion_cliente_input = QLineEdit(self)
        self.direccion_cliente_input.setPlaceholderText("Dirección del Cliente")
        layout.addWidget(self.direccion_cliente_input)

        # Botones para clientes
        crear_cliente_button = QPushButton("Crear Cliente")
        crear_cliente_button.clicked.connect(self.crear_cliente)
        layout.addWidget(crear_cliente_button)

        editar_cliente_button = QPushButton("Editar Cliente")
        editar_cliente_button.clicked.connect(self.editar_cliente)
        layout.addWidget(editar_cliente_button)

        eliminar_cliente_button = QPushButton("Eliminar Cliente")
        eliminar_cliente_button.clicked.connect(self.eliminar_cliente)
        layout.addWidget(eliminar_cliente_button)

        listar_cliente_button = QPushButton("Listar Clientes")
        listar_cliente_button.clicked.connect(self.listar_clientes)
        layout.addWidget(listar_cliente_button)

        self.clientes_table = QTableWidget(self)
        self.clientes_table.setColumnCount(3)
        self.clientes_table.setHorizontalHeaderLabels(["Código", "Nombre", "Dirección"])
        layout.addWidget(self.clientes_table)

        # Espaciado entre secciones
        layout.addWidget(QLabel("\nGestión de Productos"))

        # Tab para productos
        self.codigo_producto_input = QLineEdit(self)
        self.codigo_producto_input.setPlaceholderText("Código del Producto")
        layout.addWidget(self.codigo_producto_input)

        self.nombre_producto_input = QLineEdit(self)
        self.nombre_producto_input.setPlaceholderText("Nombre del Producto")
        layout.addWidget(self.nombre_producto_input)

        self.existencias_producto_input = QLineEdit(self)
        self.existencias_producto_input.setPlaceholderText("Cantidad en Existencia")
        layout.addWidget(self.existencias_producto_input)

        self.proveedor_producto_input = QLineEdit(self)
        self.proveedor_producto_input.setPlaceholderText("Proveedor")
        layout.addWidget(self.proveedor_producto_input)

        self.precio_producto_input = QLineEdit(self)
        self.precio_producto_input.setPlaceholderText("Precio del Producto")
        layout.addWidget(self.precio_producto_input)

        # Botones para productos
        crear_producto_button = QPushButton("Crear Producto")
        crear_producto_button.clicked.connect(self.crear_producto)
        layout.addWidget(crear_producto_button)

        editar_producto_button = QPushButton("Actualizar Producto")
        editar_producto_button.clicked.connect(self.actualizar_producto)
        layout.addWidget(editar_producto_button)

        eliminar_producto_button = QPushButton("Eliminar Producto")
        eliminar_producto_button.clicked.connect(self.eliminar_producto)
        layout.addWidget(eliminar_producto_button)

        listar_producto_button = QPushButton("Listar Productos")
        listar_producto_button.clicked.connect(self.listar_productos)
        layout.addWidget(listar_producto_button)

        self.productos_table = QTableWidget(self)
        self.productos_table.setColumnCount(5)
        self.productos_table.setHorizontalHeaderLabels(["Código", "Nombre", "Existencia", "Proveedor", "Precio"])
        layout.addWidget(self.productos_table)

        central_widget.setLayout(layout)

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

    def editar_cliente(self):
        codigo = self.codigo_cliente_input.text()
        nuevo_nombre = self.nombre_cliente_input.text()
        nueva_direccion = self.direccion_cliente_input.text()

        if codigo and nuevo_nombre and nueva_direccion:
            self.cliente_manager.editar_cliente(codigo, nuevo_nombre, nueva_direccion)
            QMessageBox.information(self, "Éxito", "Cliente editado exitosamente.")
            self.limpiar_campos_cliente()
        else:
            QMessageBox.warning(self, "Error", "Por favor, complete todos los campos.")

    def eliminar_cliente(self):
        codigo = self.codigo_cliente_input.text()

        if codigo:
            self.cliente_manager.eliminar_cliente(codigo)
            QMessageBox.information(self, "Éxito", "Cliente eliminado exitosamente.")
            self.limpiar_campos_cliente()
        else:
            QMessageBox.warning(self, "Error", "Por favor, ingrese el código del cliente a eliminar.")

    def listar_clientes(self):
        self.clientes_table.setRowCount(0)  # Limpiar la tabla
        for cliente in self.cliente_manager.listar_clientes():
            row_position = self.clientes_table.rowCount()
            self.clientes_table.insertRow(row_position)
            self.clientes_table.setItem(row_position, 0, QTableWidgetItem(cliente["codigo"]))
            self.clientes_table.setItem(row_position, 1, QTableWidgetItem(cliente["nombre"]))
            self.clientes_table.setItem(row_position, 2, QTableWidgetItem(cliente["direccion"]))

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

        if codigo and nombre and existencia.isdigit() and proveedor and precio.replace('.', '', 1).isdigit():
            producto = Producto(codigo, nombre, int(existencia), proveedor, float(precio))
            self.inventario
