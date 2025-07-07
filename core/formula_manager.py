import pkgutil
import inspect
from . import formulas
from .formulas.base_formula import BaseFormula
from typing import List, Type

def load_formulas() -> List[Type[BaseFormula]]:

    formula_classes = []

    for importer, modname, ispkg in pkgutil.iter_modules(formulas.__path__):
        if modname != 'base_formula':
            module = __import__(f"core.formulas.{modname}", fromlist="dummy")
            
            for name, obj in inspect.getmembers(module):
                
                if inspect.isclass(obj) and issubclass(obj, BaseFormula) and obj is not BaseFormula:
                    formula_classes.append(obj)
    
    return formula_classes