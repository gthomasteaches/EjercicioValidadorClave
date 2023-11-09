from abc import abstractclassmethod
from abc import ABC
from modelo.errores import NoCumpleLongitudMinimaError
from modelo.errores import NoTieneNumeroError
from modelo.errores import NoTienePalabraSecretaError
from modelo.errores import NoTieneLetraMayusculaError
from modelo.errores import NoTieneLetraMinusculaError
from modelo.errores import NoTieneCaracterEspecialError


class ReglaValidacion(ABC):
    longitud_esperada:  int

    def __init__(self, longitud_esperada: int) -> None:
        self.longitud_esperada = longitud_esperada

    def _validar_longitud(self, clave: str) -> bool:
        return len(clave) > self.longitud_esperada

    def _contiene_mayuscula(self, clave: str) -> bool:
        for letra in clave:
            if letra.isupper():
                return True
        return False

    def _contiene_minuscula(self, clave: str) -> bool:
        for letra in clave:
            if letra.islower():
                return True
        return False

    def _contiene_numero(self, clave: str) -> bool:
        for letra in clave:
            if letra.isdigit():
                return True
        return False

    @abstractclassmethod
    def es_valida(self, clave: str) -> bool:
        pass


class ReglaValidacionGanimedes(ReglaValidacion):
    def __init__(self) -> None:
        super().__init__(8)

    def contiene_caracter_especial(self, clave: str) -> bool:
        for letra in clave:
            if letra in ["@", "_", "#", "$", "%"]:
                return True
        return False

    def es_valida(self, clave: str) -> bool:
        if not self._validar_longitud(clave):
            raise NoCumpleLongitudMinimaError()
        if not self._contiene_mayuscula(clave):
            raise NoTieneLetraMayusculaError()
        if not self._contiene_minuscula(clave):
            raise NoTieneLetraMinusculaError()
        if not self._contiene_numero(clave):
            raise NoTieneNumeroError()
        if not self.contiene_caracter_especial(clave):
            raise NoTieneCaracterEspecialError()
        return True


class ReglaValidacionCalisto(ReglaValidacion):
    def __init__(self) -> None:
        super().__init__(6)

    def contiene_calisto(self, clave: str) -> bool:
        clave_minuscula = clave.lower()
        indice_calisto = clave_minuscula.find("calisto")
        while indice_calisto != -1:
            palabra_calisto = clave[indice_calisto:indice_calisto+7]
            cont = 0
            for letra in palabra_calisto:
                if letra.isupper():
                    cont += 1
            if cont >= 2 and cont < len("calisto"):
                return True
            indice_calisto = clave_minuscula.find(
                "calisto", indice_calisto+len("calisto"))
        return False

    def es_valida(self, clave: str) -> bool:
        if not self._validar_longitud(clave):
            raise NoCumpleLongitudMinimaError()
        if not self._contiene_numero(clave):
            raise NoTieneNumeroError()
        if not self.contiene_calisto(clave):
            raise NoTienePalabraSecretaError()
        return True


class Validador:
    def __init__(self, regla: ReglaValidacion) -> None:
        self.regla_validacion = regla

    def es_valida(self, clave: str) -> bool:
        return self.regla_validacion.es_valida(clave)
