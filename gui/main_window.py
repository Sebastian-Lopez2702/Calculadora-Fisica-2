import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                               QListWidget, QStackedWidget, QLabel, QHBoxLayout,
                               QSplitter)
from PySide6.QtCore import Qt

from core.formula_manager import load_formulas
from .widgets.formula_view import FormulaView

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calculadora")
        self.setGeometry(100, 100, 900, 600)
        
        self.formulas = {f.name: f() for f in load_formulas()}

        self.setup_ui()
        self.populate_formula_list()

    def setup_ui(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)

        splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(splitter)

        self.formula_list_widget = QListWidget()
        self.formula_list_widget.currentItemChanged.connect(self.on_formula_selected)
        
        self.stacked_widget = QStackedWidget()

        splitter.addWidget(self.formula_list_widget)
        splitter.addWidget(self.stacked_widget)
        splitter.setSizes([250, 650])

    def populate_formula_list(self):
        self.formula_list_widget.clear()

        for name in sorted(self.formulas.keys()):
            self.formula_list_widget.addItem(name)
            
            formula_instance = self.formulas[name]

            formula_view = FormulaView(formula_instance)
            self.stacked_widget.addWidget(formula_view)
            
    def on_formula_selected(self, current_item, previous_item):
        if current_item:

            index = self.formula_list_widget.row(current_item)
            self.stacked_widget.setCurrentIndex(index)