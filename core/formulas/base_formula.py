from abc import ABC, abstractmethod
from typing import List, Dict, Tuple

class BaseFormula(ABC):

    @property
    @abstractmethod
    def name(self) -> str:

        pass

    @property
    @abstractmethod
    def description(self) -> str:

        pass

    @property
    @abstractmethod
    def variables(self) -> List[Tuple[str, str, str]]:

        pass
    
    @property
    @abstractmethod
    def target_variable(self) -> Tuple[str, str, str]:

        pass

    @property
    @abstractmethod
    def formula_latex(self) -> str:

        pass

    @abstractmethod
    def solve(self, inputs: Dict[str, any]) -> any:

        pass