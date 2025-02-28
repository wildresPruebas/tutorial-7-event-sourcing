"""Reglas de negocio del dominio de cliente

En este archivo usted encontrará reglas de negocio del dominio de cliente

"""

from sta.seedwork.dominio.reglas import ReglaNegocio
from .objetos_valor import Requisito

class MinimoUnRequisito(ReglaNegocio):
    requisitos: list[Requisito]

    def __init__(self, requisitos, mensaje='La lista de requisitos debe tener al menos un requisito'):
        super().__init__(mensaje)
        self.requisitos = requisitos

    def es_valido(self) -> bool:
        return len(self.requisitos) > 0 and isinstance(self.requisitos[0], Requisito) 