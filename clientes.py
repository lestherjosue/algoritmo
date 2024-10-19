import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLineEdit, QLabel, QMessageBox, QTableWidget, QTableWidgetItem

# Clase para manejar la lógica de los clientes
class ClienteManager:
    def __init__(self):
        self.clientes = []
        self.cargar_clientes()  # Cargar los clientes al iniciar

    def crear_cliente(self, codigo, nombre, direccion):
        cliente = {"codigo": codigo, "nombre": nombre, "direccion": direccion}
        self.clientes.append(cliente)
        self.guardar_clientes()  # Guardar cambios en el archivo

    def editar_cliente(self, codigo, nuevo_nombre, nueva_direccion):
        for cliente in self.clientes:
            if cliente["codigo"] == codigo:
                cliente["nombre"] = nuevo_nombre
                cliente["direccion"] = nueva_direccion
                break
        self.guardar_clientes()  # Guardar cambios en el archivo

    def eliminar_cliente(self, codigo):
        self.clientes = [cliente for cliente in self.clientes if cliente["codigo"] != codigo]
        self.guardar_clientes()  # Guardar cambios en el archivo

    def listar_clientes(self):
        return self.clientes

    def cargar_clientes(self):
        try:
            # Cargar clientes desde un archivo Excel
            df = pd.read_excel('clientes.xlsx')
            self.clientes = df.to_dict(orient='records')
        except FileNotFoundError:
            print("Archivo 'clientes.xlsx' no encontrado. Se creará uno nuevo.")

    def guardar_clientes(self):
        # Guardar clientes en un archivo Excel
        df = pd.DataFrame(self.clientes)
        df.to_excel('clientes.xlsx', index=False)


# Clase principal de la interfaz gráfica
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestión de Clientes")
        self.setGeometry(100, 100, 600, 400)

        self.cliente_manager = ClienteManager()

        # Crear un widget central y un layout vertical
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()

        # Crear campos de entrada
        self.codigo_input = QLineEdit(self)
        self.codigo_input.setPlaceholderText("Código del Cliente")
        layout.addWidget(self.codigo_input)

        self.nombre_input = QLineEdit(self)
        self.nombre_input.setPlaceholderText("Nombre del Cliente")
        layout.addWidget(self.nombre_input)

        self.direccion_input = QLineEdit(self)
        self.direccion_input.setPlaceholderText("Dirección del Cliente")
        layout.addWidget(self.direccion_input)

        # Botón para crear cliente
        crear_button = QPushButton("Crear Cliente")
        crear_button.clicked.connect(self.crear_cliente)
        layout.addWidget(crear_button)

        # Botón para editar cliente
        editar_button = QPushButton("Editar Cliente")
        editar_button.clicked.connect(self.editar_cliente)
        layout.addWidget(editar_button)

        # Botón para eliminar cliente
        eliminar_button = QPushButton("Eliminar Cliente")
        eliminar_button.clicked.connect(self.eliminar_cliente)
        layout.addWidget(eliminar_button)

        # Botón para listar clientes
        listar_button = QPushButton("Listar Clientes")
        listar_button.clicked.connect(self.listar_clientes)
        layout.addWidget(listar_button)

        # Tabla para mostrar los clientes
        self.clientes_table = QTableWidget(self)
        self.clientes_table.setColumnCount(3)
        self.clientes_table.setHorizontalHeaderLabels(["Código", "Nombre", "Dirección"])
        layout.addWidget(self.clientes_table)

        central_widget.setLayout(layout)

    def crear_cliente(self):
        codigo = self.codigo_input.text()
        nombre = self.nombre_input.text()
        direccion = self.direccion_input.text()

        if codigo and nombre and direccion:
            self.cliente_manager.crear_cliente(codigo, nombre, direccion)
            QMessageBox.information(self, "Éxito", "Cliente creado exitosamente.")
            self.limpiar_campos()
        else:
            QMessageBox.warning(self, "Error", "Por favor, complete todos los campos.")

    def editar_cliente(self):
        codigo = self.codigo_input.text()
        nuevo_nombre = self.nombre_input.text()
        nueva_direccion = self.direccion_input.text()

        if codigo and nuevo_nombre and nueva_direccion:
            self.cliente_manager.editar_cliente(codigo, nuevo_nombre, nueva_direccion)
            QMessageBox.information(self, "Éxito", "Cliente editado exitosamente.")
            self.limpiar_campos()
        else:
            QMessageBox.warning(self, "Error", "Por favor, complete todos los campos.")

    def eliminar_cliente(self):
        codigo = self.codigo_input.text()

        if codigo:
            self.cliente_manager.eliminar_cliente(codigo)
            QMessageBox.information(self, "Éxito", "Cliente eliminado exitosamente.")
            self.limpiar_campos()
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

    def limpiar_campos(self):
        self.codigo_input.clear()
        self.nombre_input.clear()
        self.direccion_input.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec_())
