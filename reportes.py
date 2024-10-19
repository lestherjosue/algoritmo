import sys
import pandas as pd
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QMessageBox,
    QLineEdit,
    QLabel,
)


class VentasApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Reporte de Ventas")
        self.setGeometry(100, 100, 800, 600)

        # Crear un widget central y un layout vertical
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()

        # Campos para registrar una nueva venta
        layout.addWidget(QLabel("Cliente:"))
        self.cliente_input = QLineEdit(self)
        layout.addWidget(self.cliente_input)

        layout.addWidget(QLabel("Producto:"))
        self.producto_input = QLineEdit(self)
        layout.addWidget(self.producto_input)

        layout.addWidget(QLabel("Cantidad:"))
        self.cantidad_input = QLineEdit(self)
        layout.addWidget(self.cantidad_input)

        layout.addWidget(QLabel("Precio Unitario:"))
        self.precio_input = QLineEdit(self)
        layout.addWidget(self.precio_input)

        # Botón para registrar una nueva venta
        registrar_button = QPushButton("Registrar Venta")
        registrar_button.clicked.connect(self.registrar_venta)
        layout.addWidget(registrar_button)

        # Botón para cargar el archivo CSV y generar reportes
        cargar_button = QPushButton("Cargar Ventas")
        cargar_button.clicked.connect(self.cargar_ventas)
        layout.addWidget(cargar_button)

        # Botón para exportar reportes a Excel
        exportar_button = QPushButton("Exportar a Excel")
        exportar_button.clicked.connect(self.exportar_a_excel)
        layout.addWidget(exportar_button)

        # Tabla para mostrar ventas por cliente
        self.clientes_table = QTableWidget(self)
        layout.addWidget(self.clientes_table)

        # Tabla para mostrar ventas por producto
        self.productos_table = QTableWidget(self)
        layout.addWidget(self.productos_table)

        central_widget.setLayout(layout)

    def registrar_venta(self):
        try:
            cliente = self.cliente_input.text()
            producto = self.producto_input.text()
            cantidad = int(self.cantidad_input.text())
            precio_unitario = float(self.precio_input.text())

            # Crear un DataFrame para la nueva venta
            nueva_venta = pd.DataFrame({
                'cliente': [cliente],
                'producto': [producto],
                'cantidad': [cantidad],
                'precio_unitario': [precio_unitario]
            })

            # Guardar la nueva venta en el archivo CSV
            nueva_venta.to_csv('ventas.csv', mode='a', header=not pd.io.common.file_exists('ventas.csv'), index=False)

            QMessageBox.information(self, "Éxito", "Venta registrada exitosamente.")
            self.limpiar_campos()
            self.cargar_ventas()  # Recargar los datos después de registrar una venta
        except ValueError:
            QMessageBox.warning(self, "Error", "Por favor, ingrese valores válidos para cantidad y precio.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Ocurrió un error: {str(e)}")

    def limpiar_campos(self):
        self.cliente_input.clear()
        self.producto_input.clear()
        self.cantidad_input.clear()
        self.precio_input.clear()

    def cargar_ventas(self):
        try:
            # Cargar los datos del archivo CSV
            df = pd.read_csv('ventas.csv')

            # Calcular el total por venta
            df['total_venta'] = df['cantidad'] * df['precio_unitario']

            # Reporte de ventas por cliente
            ventas_por_cliente = df.groupby('cliente')['total_venta'].sum().reset_index()
            ventas_por_cliente = ventas_por_cliente.sort_values(by='total_venta', ascending=False)

            # Actualizar la tabla de ventas por cliente
            self.actualizar_tabla(self.clientes_table, ventas_por_cliente, ["Cliente", "Total Venta"])

            # Reporte de ventas por producto
            ventas_por_producto = df.groupby('producto')['total_venta'].sum().reset_index()
            ventas_por_producto = ventas_por_producto.sort_values(by='total_venta', ascending=False)

            # Actualizar la tabla de ventas por producto
            self.actualizar_tabla(self.productos_table, ventas_por_producto, ["Producto", "Total Venta"])

            QMessageBox.information(self, "Éxito", "Reportes de ventas cargados exitosamente.")
        except FileNotFoundError:
            QMessageBox.warning(self, "Error", "El archivo 'ventas.csv' no se encontró.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Ocurrió un error: {str(e)}")

    def actualizar_tabla(self, table, data, headers):
        table.setRowCount(0)  # Limpiar la tabla
        table.setColumnCount(len(headers))
        table.setHorizontalHeaderLabels(headers)

        for index, row in data.iterrows():
            table.insertRow(index)
            for col in range(len(headers)):
                table.setItem(index, col, QTableWidgetItem(str(row[col])))

    def exportar_a_excel(self):
        try:
            # Cargar los datos del archivo CSV
            df = pd.read_csv('ventas.csv')

            # Calcular el total por venta
            df['total_venta'] = df['cantidad'] * df['precio_unitario']

            # Reporte de ventas por cliente
            ventas_por_cliente = df.groupby('cliente')['total_venta'].sum().reset_index()
            ventas_por_cliente = ventas_por_cliente.sort_values(by='total_venta', ascending=False)

            # Reporte de ventas por producto
            ventas_por_producto = df.groupby('producto')['total_venta'].sum().reset_index()
            ventas_por_producto = ventas_por_producto.sort_values(by='total_venta', ascending=False)

            # Crear un archivo de Excel
            with pd.ExcelWriter('reportes_ventas.xlsx', engine='openpyxl') as writer:
                ventas_por_cliente.to_excel(writer, sheet_name='Ventas por Cliente', index=False)
                ventas_por_producto.to_excel(writer, sheet_name='Ventas por Producto', index=False)

            QMessageBox.information(self, "Éxito", "Reportes exportados a 'reportes_ventas.xlsx' exitosamente.")
        except FileNotFoundError:
            QMessageBox.warning(self, "Error", "El archivo 'ventas.csv' no se encontró.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Ocurrió un error: {str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win = VentasApp()
    main_win.show()
    sys.exit(app.exec_())
