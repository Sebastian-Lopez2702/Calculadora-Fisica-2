from .base_formula import BaseFormula
from ..unit_handler import Q_
from typing import Dict, List, Tuple
import numpy as np

class CalorEspecifico(BaseFormula):
    name = "Calorimetría (Calor Sensible)"
    description = "Calcula la cantidad de calor necesaria para cambiar la temperatura de una masa."
    
    variables: List[Tuple[str, str, str]] = [
        ('masa', 'm', 'gram'),
        ('calor_especifico', 'c', 'joule / (gram * kelvin)'),
        ('delta_temperatura', r"\Delta T", 'delta_degree_Celsius')
    ]
    
    target_variable: Tuple[str, str, str] = ('calor', 'Q', 'joule')
    
    formula_latex: str = r"Q = m \cdot c \cdot \Delta T"

    def solve(self, inputs: Dict[str, Q_]) -> Q_:
        m = inputs['masa']
        c = inputs['calor_especifico']
        delta_t = inputs['delta_temperatura']
        
        Q = m * c * delta_t
        return Q.to(self.target_variable[2])

class DilatacionLineal(BaseFormula):
    name = "Dilatación Lineal"
    description = "Calcula el cambio en la longitud de un material debido a un cambio de temperatura."
    
    variables: List[Tuple[str, str, str]] = [
        ('longitud_inicial', r'L_0', 'meter'),
        ('coeficiente_dilatacion', r'\alpha', '1 / kelvin'),
        ('delta_temperatura', r'\Delta T', 'delta_degree_Celsius')
    ]
    
    target_variable: Tuple[str, str, str] = ('delta_longitud', r'\Delta L', 'millimeter')
    
    formula_latex: str = r"\Delta L = \alpha \cdot L_0 \cdot \Delta T"

    def solve(self, inputs: Dict[str, Q_]) -> Q_:
        L0 = inputs['longitud_inicial']
        alpha = inputs['coeficiente_dilatacion']
        delta_t = inputs['delta_temperatura']
        
        delta_L = L0 * alpha * delta_t
        return delta_L.to(self.target_variable[2])
    
class EquilibrioTermico(BaseFormula):
    name = "Equilibrio Térmico"
    description = "Calcula el cambio de temperatura de un cuerpo hasta alcanzar el equilibrio térmico."
    
    variables = [
        ('masa_1', 'm_1', 'gram'),
        ('calor_especifico_1', 'c_1', 'joule / (gram * kelvin)'),
        ('delta_T1', r'\Delta T_1', 'delta_degree_Celsius'),
        ('masa_2', 'm_2', 'gram'),
        ('calor_especifico_2', 'c_2', 'joule / (gram * kelvin)')
    ]
    
    target_variable = ('delta_T2', r'\Delta T_2', 'delta_degree_Celsius')
    
    formula_latex = r"m_1 c_1 \Delta T_1 + m_2 c_2 \Delta T_2 = 0"

    def solve(self, inputs: Dict[str, Q_]) -> Q_:
        m1 = inputs['masa_1']
        c1 = inputs['calor_especifico_1']
        delta_T1 = inputs['delta_T1']
        m2 = inputs['masa_2']
        c2 = inputs['calor_especifico_2']

        delta_T2 = -(m1 * c1 * delta_T1) / (m2 * c2)
        return delta_T2.to(self.target_variable[2])