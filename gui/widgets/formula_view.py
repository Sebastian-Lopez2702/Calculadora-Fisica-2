from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QLineEdit, 
                               QPushButton, QFormLayout, QHBoxLayout, QComboBox,
                               QFrame, QTextEdit)
from PySide6.QtGui import QFont, QDoubleValidator
from PySide6.QtCore import Qt

from core.formulas.base_formula import BaseFormula
from core.unit_handler import ureg, Q_

from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas

PREFERRED_UNITS = {

    'gram': ['gram', 'kilogram', 'milligram'],

    'meter': ['meter', 'kilometer', 'centimeter', 'millimeter'],

    'kelvin': ['kelvin'],

    'degree_Celsius': ['degree_Celsius', 'kelvin', 'degree_Fahrenheit'],
    
    'delta_degree_Celsius': ['delta_degree_Celsius', 'kelvin', 'delta_degree_Fahrenheit'],

    'pascal': ['pascal', 'kilopascal', 'megapascal', 'bar', 'atmosphere', 'psi'],

    'liter': ['liter', 'milliliter', 'meter ** 3', 'centimeter ** 3'],

    'mol': ['mol'],

    'joule / (gram * kelvin)': ['joule / (gram * kelvin)', 'joule / (kilogram * kelvin)'],
    
    '1 / kelvin': ['1 / kelvin']
}

class FormulaView(QWidget):
    def __init__(self, formula: BaseFormula):
        super().__init__()
        self.formula = formula
        self.input_widgets = {}

        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignTop)
        
        title = QLabel(f"<b>{self.formula.name}</b>")
        title.setFont(QFont("Arial", 16))
        self.layout.addWidget(title)
        
        desc = QLabel(self.formula.description)
        desc.setWordWrap(True)
        self.layout.addWidget(desc)
        
        self.add_latex_display()

        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        self.layout.addWidget(line)

        form_layout = QFormLayout()
        form_layout.setRowWrapPolicy(QFormLayout.WrapAllRows)
        
        for var_name, symbol, default_unit in self.formula.variables:
            label_text = f"{var_name.replace('_', ' ').capitalize()} ({symbol}):"
            
            value_edit = QLineEdit()
            value_edit.setPlaceholderText("ej: 12.5")
            value_edit.setValidator(QDoubleValidator())

            unit_combo = QComboBox()
            
            units_to_show = PREFERRED_UNITS.get(default_unit)
            
            if units_to_show is None:
                units_to_show = [default_unit]

            unit_combo.addItems(units_to_show)

            unit_combo.setCurrentText(default_unit)

            input_hbox = QHBoxLayout()
            input_hbox.addWidget(value_edit)
            input_hbox.addWidget(unit_combo)
            
            form_layout.addRow(label_text, input_hbox)
            self.input_widgets[var_name] = (value_edit, unit_combo)

        self.layout.addLayout(form_layout)

        self.calc_button = QPushButton("Calcular")
        self.calc_button.clicked.connect(self.calculate)
        self.layout.addWidget(self.calc_button)

        self.result_label = QLabel("Resultado:")
        self.result_label.setFont(QFont("Arial", 12))
        self.layout.addWidget(self.result_label)
        
        self.result_output = QTextEdit()
        self.result_output.setReadOnly(True)
        self.result_output.setFixedHeight(100)
        self.layout.addWidget(self.result_output)

    def add_latex_display(self):
        fig = Figure(figsize=(5, 1), dpi=100)
        fig.patch.set_facecolor('none')
        canvas = FigureCanvas(fig)
        canvas.setStyleSheet("background-color:transparent;")
        ax = fig.add_subplot(111)
        
        formatted_latex = f"${self.formula.formula_latex}$"
        
        ax.text(0.5, 0.5, formatted_latex, fontsize=20, ha='center', va='center')
        ax.axis('off')
        fig.tight_layout(pad=0)
        
        self.layout.addWidget(canvas)

    def calculate(self):
        try:
            inputs = {}
            for var_name, (value_edit, unit_combo) in self.input_widgets.items():
                value_str = value_edit.text().strip().replace(',', '.')
                if not value_str:
                    raise ValueError(f"El campo '{var_name.replace('_', ' ')}' no puede estar vacío.")
                
                value = float(value_str)
                unit = unit_combo.currentText()
                if not unit:
                    raise ValueError(f"Debe seleccionar una unidad para '{var_name.replace('_', ' ')}'.")
                
                inputs[var_name] = Q_(value, unit)
            
            result = self.formula.solve(inputs)
            
            magnitude = result.magnitude
            units = result.units
            
            formatted_magnitude = f"{magnitude:.6f}"
            
            formatted_result = f"{formatted_magnitude} {units:~P}"
            
            output_text = f"<b>Resultado:</b><br>{formatted_result}"
            
            target_unit = self.formula.target_variable[2]
            if str(result.units) != target_unit:
                converted_magnitude = result.to(target_unit).magnitude
                formatted_converted = f"{converted_magnitude:.6f}"
                output_text += f"<br><br><b>En la unidad de destino ({target_unit}):</b><br>{formatted_converted} {target_unit}"
            
            self.result_output.setHtml(output_text)

        except Exception as e:
            error_message = f"<b>Error:</b><br><pre>{type(e).__name__}: {str(e)}</pre>"
            self.result_output.setHtml(error_message)