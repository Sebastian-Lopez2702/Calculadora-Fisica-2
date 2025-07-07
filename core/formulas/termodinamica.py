from .base_formula import BaseFormula
from ..unit_handler import Q_, ureg
from typing import Dict, List, Tuple
from numpy import log as ln

class LeyGasesIdeales(BaseFormula):
    name = "Ley de los Gases Ideales"
    description = "Relaciona la presión, volumen, cantidad de sustancia y temperatura de un gas ideal."
    
    variables: List[Tuple[str, str, str]] = [
        ('moles', 'n', 'mol'),
        ('temperatura', 'T', 'kelvin'),
        ('presion', 'P', 'pascal')
    ]
    
    target_variable: Tuple[str, str, str] = ('volumen', 'V', 'liter')
    
    formula_latex: str = r"V = \frac{nRT}{P}"

    def solve(self, inputs: Dict[str, Q_]) -> Q_:
        n = inputs['moles']
        T = inputs['temperatura']
        P = inputs['presion']
        R = ureg.R
        
        V = (n * R * T) / P
        return V.to(self.target_variable[2])

class EnergiaCineticaMedia(BaseFormula):
    name = "Energía Cinética Media (Gas Monoatómico)"
    description = "Calcula la energía cinética promedio de las partículas de un gas ideal monoatómico."
    
    variables: List[Tuple[str, str, str]] = [
        ('temperatura', 'T', 'kelvin')
    ]
    
    target_variable: Tuple[str, str, str] = ('energia_cinetica', 'K', 'joule')
    
    formula_latex: str = r"K = \frac{3}{2} k_B T"

    def solve(self, inputs: Dict[str, Q_]) -> Q_:
        T = inputs['temperatura']
        kB = ureg.k
        
        K = (3/2) * kB * T
        return K.to(self.target_variable[2])
    
class PrimeraLeyTermodinamica(BaseFormula):
    name = "Primera Ley de la Termodinámica"
    description = "Calcula el cambio en la energía interna según la cantidad de calor y el trabajo realizado."
    
    variables = [
        ('calor', 'Q', 'joule'),
        ('trabajo', 'W', 'joule')
    ]
    
    target_variable = ('energia_interna', r'\Delta U', 'joule')
    
    formula_latex = r"\Delta U = Q - W"

    def solve(self, inputs: Dict[str, Q_]) -> Q_:
        Q = inputs['calor']
        W = inputs['trabajo']
        delta_U = Q - W
        return delta_U.to(self.target_variable[2])
    
class TrabajoIsotermico(BaseFormula):
    name = "Trabajo en Proceso Isotérmico"
    description = "Calcula el trabajo realizado por un gas ideal en una expansión o compresión isotérmica."
    
    variables = [
        ('moles', 'n', 'mol'),
        ('temperatura', 'T', 'kelvin'),
        ('volumen_inicial', 'V_i', 'liter'),
        ('volumen_final', 'V_f', 'liter')
    ]
    
    target_variable = ('trabajo', 'W', 'joule')
    
    formula_latex = r"W = nRT \ln\left(\frac{V_f}{V_i}\right)"

    def solve(self, inputs: Dict[str, Q_]) -> Q_:
        n = inputs['moles']
        T = inputs['temperatura']
        V_i = inputs['volumen_inicial']
        V_f = inputs['volumen_final']
        R = ureg.R

        W = n * R * T * ln(V_f / V_i)
        return W.to(self.target_variable[2])
    
class LeyDeBoyle(BaseFormula):
    name = "Ley de Boyle"
    description = "Calcula la relación entre presión y volumen en un proceso isotérmico."
    
    variables = [
        ('presion_inicial', 'P_1', 'pascal'),
        ('volumen_inicial', 'V_1', 'liter'),
        ('presion_final', 'P_2', 'pascal')
    ]
    
    target_variable = ('volumen_final', 'V_2', 'liter')
    
    formula_latex = r"P_1 V_1 = P_2 V_2"

    def solve(self, inputs: Dict[str, Q_]) -> Q_:
        P1 = inputs['presion_inicial']
        V1 = inputs['volumen_inicial']
        P2 = inputs['presion_final']
        V2 = (P1 * V1) / P2
        return V2.to(self.target_variable[2])
    
class CapacidadCalorifica(BaseFormula):
    name = "Capacidad Calorífica"
    description = "Calcula la capacidad calorífica de un cuerpo."
    
    variables = [
        ('calor', 'Q', 'joule'),
        ('delta_temperatura', r'\Delta T', 'delta_degree_Celsius')
    ]
    
    target_variable = ('capacidad_calorifica', 'C', 'joule / delta_degree_Celsius')
    
    formula_latex = r"C = \frac{Q}{\Delta T}"

    def solve(self, inputs: Dict[str, Q_]) -> Q_:
        Q = inputs['calor']
        delta_T = inputs['delta_temperatura']
        C = Q / delta_T
        return C.to(self.target_variable[2])
    
class LeyDeCharles(BaseFormula):
    name = "Ley de Charles"
    description = "Relaciona el volumen y la temperatura de un gas a presión constante."
    
    variables = [
        ('volumen_1', 'V_1', 'liter'),
        ('temperatura_1', 'T_1', 'kelvin'),
        ('temperatura_2', 'T_2', 'kelvin')
    ]
    
    target_variable = ('volumen_2', 'V_2', 'liter')
    
    formula_latex = r"\frac{V_1}{T_1} = \frac{V_2}{T_2}"

    def solve(self, inputs: Dict[str, Q_]) -> Q_:
        V1 = inputs['volumen_1']
        T1 = inputs['temperatura_1']
        T2 = inputs['temperatura_2']
        V2 = V1 * T2 / T1
        return V2.to(self.target_variable[2])