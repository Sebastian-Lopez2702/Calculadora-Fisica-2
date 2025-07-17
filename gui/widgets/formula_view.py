from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
                               QComboBox, QPushButton, QFormLayout, QFrame, QTextEdit)
from PySide6.QtGui import QFont, QDoubleValidator
from PySide6.QtCore import Qt

from core.formulas.base_formula import BaseFormula
from core.unit_handler import ureg, Q_

from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas

PREFERRED_UNITS = {
    'gram': ['gram', 'kilogram', 'milligram'],
    
    'meter': ['meter', 'kilometer', 'centimeter', 'millimeter'],
    
    'kelvin': ['kelvin', 'degree_Celsius', 'degree_Fahrenheit'],
    
    'degree_Celsius': ['degree_Celsius', 'kelvin', 'degree_Fahrenheit'],
    
    'delta_degree_Celsius': ['delta_degree_Celsius', 'kelvin', 'delta_degree_Fahrenheit'],
    
    'pascal': ['pascal', 'kilopascal', 'megapascal', 'bar', 'atmosphere', 'psi'],
    
    'liter': ['liter', 'milliliter', 'meter ** 3', 'centimeter ** 3'],
    
    'mol': ['mol'],
    
    'joule / (gram * kelvin)': ['joule / (gram * kelvin)', 'joule / (kilogram * kelvin)'],
    
    '1 / kelvin': ['1 / kelvin'],
    
    'joule': ['joule', 'kilojoule', 'calorie']
}

class FormulaView(QWidget):
    def __init__(self, formula: BaseFormula):
        super().__init__()
        self.formula = formula
        self.input_widgets = {}

        self.setup_ui()

    def setup_ui(self):
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
            units_to_show = PREFERRED_UNITS.get(default_unit, [default_unit])
            unit_combo.addItems(units_to_show)
            unit_combo.setCurrentText(default_unit)
            
            unit_combo.currentIndexChanged.connect(self._check_unit_consistency)

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
            
            formatted_result = f"{magnitude} {units:~P}"
        
            output_text = f"<b>Resultado:</b><br>{formatted_result}"
            
            self.result_output.setHtml(output_text)

        except Exception as e:
            error_message = f"<b>Error:</b><br><pre>{type(e).__name__}: {str(e)}</pre>"
            self.result_output.setHtml(error_message)

    def _get_unit(self, var_name: str) -> str | None:
        if var_name in self.input_widgets:
            _, unit_combo = self.input_widgets[var_name]
            return unit_combo.currentText()
        return None

    def _show_status_bar_message(self, message: str, timeout: int = 6000):
        status_bar = self.window().statusBar()
        if status_bar:
            status_bar.showMessage(message, timeout)

    def _check_unit_consistency(self):
        warnings = []
        formula_name = self.formula.name

        # Calorimetría
        if formula_name == "Calorimetría (Calor Sensible)":
            mass_unit = self._get_unit('masa')
            c_unit = self._get_unit('calor_especifico')
            if mass_unit and c_unit:
                if ('gram' in mass_unit and 'kilogram' in c_unit) or \
                ('kilogram' in mass_unit and 'gram' in c_unit) or \
                ('milligram' in mass_unit and 'kilogram' in c_unit) or \
                ('milligram' in mass_unit and 'gram' in c_unit):
                    warnings.append("Advertencia: Esta utilizando unidades distintas de masa vs. c. específico")
        
        # Equilibrio Térmico
        elif formula_name == "Equilibrio Térmico":
            m1, c1 = self._get_unit('masa_1'), self._get_unit('calor_especifico_1')
            m2, c2 = self._get_unit('masa_2'), self._get_unit('calor_especifico_2')
            if m1 and c1 and (('gram,' in m1 and 'kilogram' in c1) or ('kilogram' in m1 and 'gram' in c1) \
                or ('milligram,' in m1 and 'kilogram' in c1) or ('milligram,' in m1 and 'gram' in c1)):
                warnings.append("Advertencia: Esta utilizando unidades distintas de masa vs. c. específico")
                
            if m2 and c2 and (('gram' in m2 and 'kilogram' in c2) or ('kilogram' in m2 and 'gram' in c2) \
                or ('milligram,' in m2 and 'kilogram' in c2) or ('milligram,' in m2 and 'gram' in c2)):
                warnings.append("Advertencia: Esta utilizando unidades distintas de masa vs. c. específico")
                
            if c1 and c2 and (('gram' in c1 and 'kilogram' in c2) or ('kilogram' in c1 and 'gram' in c2)):
                warnings.append("Las unidades de calores específicos (c1/c2) no coinciden")

        # Formulas que requieren temperatura absoluta
        T_abs_formulas = ["Ley de los Gases Ideales", "Energía Cinética Media (Gas Monoatómico)", "Trabajo en Proceso Isotérmico", "Ley de Charles"]
        if formula_name in T_abs_formulas:
            temp_vars = ['temperatura', 'temperatura_1', 'temperatura_2']
            for var in temp_vars:
                temp_unit = self._get_unit(var)
                if temp_unit and ('Celsius' in temp_unit or 'Fahrenheit' in temp_unit):
                    warnings.append("ADVERTENCIA: Esta ley requiere temperatura absoluta (Kelvin), en caso de utilizarla otra, aparecera un error")
                    break

        # Formulas con estados Iniciales y finales
        state_formulas = ["Trabajo en Proceso Isotérmico", "Ley de Boyle", "Ley de Charles"]
        if formula_name in state_formulas:
            # Revisa volúmenes
            v1 = self._get_unit('volumen_inicial') or self._get_unit('volumen_1')
            v2 = self._get_unit('volumen_final') or self._get_unit('volumen_2')
            if v1 and v2 and v1 != v2:
                warnings.append("Se recomienda usar la misma unidad para volumenes")

            # Revisa presiones
            p1 = self._get_unit('presion_inicial')
            p2 = self._get_unit('presion_final')
            if p1 and p2 and p1 != p2:
                warnings.append("Se recomienda usar la misma unidad para presiones")

        if warnings:
            final_message = " | ".join(warnings)
            self._show_status_bar_message(final_message)
        else:
            self._show_status_bar_message("", 1)