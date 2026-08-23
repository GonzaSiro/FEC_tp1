# -*- coding: utf-8 -*-
"""
Módulo fec_algebra.py
Implementación de álgebra de Campos de Galois y Polinomios sobre dichos campos.

"""

class CampoDeGalois:
    """
    Representa un Campo de Galois de característica 2, denotado como GF(2^m).
    Realiza aritmética finita utilizando un polinomio primitivo para las reducciones.
    """

    def __init__(self, orden_m: int, polinomio_primitivo: int):
        """
        Constructor de la clase CampoDeGalois.

        Parámetros:
  
        orden_m : int
            El orden 'm' del campo de Galois GF(2^m). Define el número de elementos del campo.

        polinomio_primitivo : int
            Representación entera de los coeficientes del polinomio primitivo
        """

        # Validación de que el orden sea un entero positivo mayor a cero
        if not isinstance(orden_m, int):
            raise TypeError("El orden 'orden_m' debe ser un número entero.")
        if orden_m <= 0:
            raise ValueError("El orden 'orden_m' debe ser un número entero strictly positivo.")

        # Validación de que el polinomio primitivo sea un entero positivo
        if not isinstance(polinomio_primitivo, int):
            raise TypeError("El polinomio primitivo 'polinomio_primitivo' debe ser un número entero.")
        if polinomio_primitivo < 0:
            raise ValueError("El polinomio primitivo no puede ser un número negativo.")

        # Inicialización de atributos principales del campo
        self.orden_m = orden_m
        self.polinomio_primitivo = polinomio_primitivo
        
        # Cantidad total de elementos en el campo finitos: 2^m
        self.cantidad_elementos = 1 << orden_m

    def validar_elemento(self, elemento: int, nombre_parametro: str = "El elemento") -> int:
        """
        Validación para asegurar que un elemento pertenezca al rango [0, 2^m - 1].
        """
        if not isinstance(elemento, int):
            raise TypeError(f"{nombre_parametro} debe ser un número entero.")
        if elemento < 0 or elemento >= self.cantidad_elementos:
            raise ValueError(f"{nombre_parametro} ({elemento}) está fuera de rango para GF(2^{self.orden_m})")
        return elemento

    def suma(self, elemento_a: int, elemento_b: int) -> int:
        """
        Realiza la suma de dos elementos en el campo GF(2^m).
        En campos de característica 2, la suma es la operación binaria XOR.
        """
        # Validar que los elementos pertenezcan al rango del campo [0, 2^m - 1]
        
        self.validar_elemento(elemento_a, "El elemento A")
        self.validar_elemento(elemento_b, "El elemento B")

        # La adición en campos binarios es un simple XOR bit a bit
        resultado_suma = elemento_a ^ elemento_b
        return resultado_suma

    def producto(self, elemento_a: int, elemento_b: int) -> int:
        """
        Realiza la multiplicación de dos elementos en el campo GF(2^m).
        aplicando reducción polinomial módulo el polinomio primitivo en cada desbordamiento.
        """
        # Validar que los elementos pertenezcan al rango del campo [0, 2^m - 1]
        self.validar_elemento(elemento_a, "El elemento A")
        self.validar_elemento(elemento_b, "El elemento B")

        # Inicialización del resultado en cero
        resultado_producto = 0

        # Copias locales de trabajo para los operandos
        factor_a = elemento_a
        factor_b = elemento_b

        # Máscara  de 'm'bits todos en 1 
        # sirve para mantener la cantidad de bits en m en caso de overflow
        mascara_palabra = (1 << self.orden_m) - 1

        # Iteramos bit por bit a lo largo de los 'm' bits
        for paso in range(self.orden_m):
            # Evaluamos si el bit menos significativo del factor_b es 1
            if (factor_b & 1) != 0:
                # Sumamos (hacemos XOR) factor_a al resultado acumulado
                resultado_producto = resultado_producto ^ factor_a

            # Desplazamos factor_b a la derecha para evaluar el siguiente bit
            factor_b = factor_b >> 1

            # Guardamos el bit más significativo (MSB) de factor_a antes de desplazar
            bit_msb_factor_a = factor_a & (1 << (self.orden_m - 1))

            # Desplazamos factor_a a la izquierda (multiplicación por 2)
            factor_a = factor_a << 1

            # Si el bit más significativo era 1, se genera un overflow.
            # Debemos reducir el polinomio usando el polinomio primitivo de reducción.
            if bit_msb_factor_a != 0:
                # Quitamos el bit de grado m que se desbordó aplicando la máscara de m bits 1 
                factor_a = factor_a & mascara_palabra
                # XOR con los coeficientes del polinomio primitivo implícito para terminar de reducir 
                factor_a = factor_a ^ self.polinomio_primitivo

        return resultado_producto

    def potencia(self, base: int, exponente: int) -> int:
        """
        Calcula la potencia de un elemento de GF(2^m) elevado a un exponente entero no negativo.
        """
        # Validación de la base: verificar que pertenezca al rango del campo [0, 2^m - 1]
        self.validar_elemento(base, "La base")
        
        # Validación del exponente. Como no es un campo de galois 
        # no puedo usar la funcion validar elemento

        if not isinstance(exponente, int):
            raise TypeError("El exponente debe ser un número entero.")
        if exponente < 0:
            raise ValueError("El exponente debe ser mayor o igual a cero.")

        # Caso base: todo elemento elevado a 0 es 1 (unidad de multiplicación del campo)
        if exponente == 0:
            return 1

        # Inicialización de las variables para el bucle de exponenciación.
        # resultado_potencia acumulador
        # base_actual es la base que se eleva al cuadrado en cada paso
        # exponente_actual es el exponente que se divide por 2 en cada paso

        #para hacer la potencia usamos la funcion producto. la vamos a llamar 
        # en potencias de dos en dos
        
        resultado_potencia = 1
        base_actual = base
        exponente_actual = exponente

        while exponente_actual > 0:
            # Si el bit menos significativo del exponente es 1, multiplicamos el resultado por la base actual
            if (exponente_actual & 1) != 0:
                resultado_potencia = self.producto(resultado_potencia, base_actual)

            # Elevamos la base al cuadrado para acodomar para la siguiente iteración
            base_actual = self.producto(base_actual, base_actual)

            # Desplazamos el exponente a la derecha para procesar el siguiente bit
            exponente_actual = exponente_actual >> 1

        return resultado_potencia

    def inverso_multiplicativo(self, elemento: int) -> int:
        """
        Calcula el inverso multiplicativo de un elemento no nulo del campo GF(2^m).
        """
        # Validación del elemento: verificar que pertenezca al rango del campo [0, 2^m - 1]
        self.validar_elemento(elemento, "El elemento")

        # El elemento nulo 0 no posee inverso multiplicativo
        if elemento == 0:
            raise ValueError("El elemento 0 no posee inverso multiplicativo definido en el campo.")

        # El exponente para el cálculo del inverso es (cantidad_elementos - 2)
        # en otras palabras es  (2^m - 2) es la formula general de fermat para campos finitos
        # nos permite calcular el inverso multiplicativo de un elemento no nulo del campo
        # para el inverso multiplicativo usamos la funcion potencia.
        exponente_inversion = self.cantidad_elementos - 2
        resultado_inverso = self.potencia(elemento, exponente_inversion)

        return resultado_inverso

    def division(self, numerador: int, denominador: int) -> int:
        """
        Realiza la división de dos elementos del campo.
        A / B se calcula como el producto de A por el inverso de B.
        """
        # Validación del numerador: verificar que pertenezca al rango del campo [0, 2^m - 1]
        self.validar_elemento(numerador, "El numerador")
        
        # Validación del denominador: verificar que pertenezca al rango del campo [0, 2^m - 1]
        self.validar_elemento(denominador, "El denominador")

        # La división por 0 está indefinida
        if denominador == 0:
            raise ZeroDivisionError("División por cero: el divisor no puede ser el elemento 0 del campo.")

        # Obtener el inverso del denominador so llamo a inverso multiplicador
        inverso_denominador = self.inverso_multiplicativo(denominador)

        # Multiplicar el numerador por el inverso obtenido
        resultado_division = self.producto(numerador, inverso_denominador)
        return resultado_division


class GFPoly:
    """
    Representa un polinomio con coeficientes pertenecientes a un Campo de Galois GF(2^m).
    """

    def __init__(self, campo: CampoDeGalois, coeficientes_entrada: list):
        """
        Constructor de la clase GFPoly.

        Parámetros:

        campo : CampoDeGalois
            Instancia del campo de Galois sobre el cual operan los coeficientes.
        coeficientes_entrada : list
            Lista o tupla de enteros que representan los coeficientes del polinomio,
            ordenados de mayor grado a menor grado. Ejemplo: [a_n, a_n-1, ..., a_0].
        """
        # Validar la instancia del campo de Galois
        if not isinstance(campo, CampoDeGalois):
            raise TypeError("El parámetro 'campo' debe ser una instancia de la clase CampoDeGalois.")

        self.campo = campo

        # Validar y convertir la lista de coeficientes de entrada
        if coeficientes_entrada is None:
            raise ValueError("La lista de coeficientes no puede ser nula (None).")
            
        # Si la lista de coeficientes está vacía, representamos el polinomio nulo [0]
        if len(coeficientes_entrada) == 0:
            self.coeficientes = [0]
        else:
            self.coeficientes = list(coeficientes_entrada)

        # Validar que cada coeficiente sea un entero y pertenezca al campo de Galois
        for posicion_indice, coeficiente in enumerate(self.coeficientes):
            if not isinstance(coeficiente, int):
                raise TypeError(f"El coeficiente en el índice {posicion_indice} debe ser un entero.")
            self.campo.validar_elemento(
                coeficiente,
                f"El coeficiente {coeficiente} en la posición {posicion_indice} no pertenece al campo GF(2^{self.campo.orden_m})"
            )

        # Normalizar el polinomio eliminando los ceros a la izquierda.
        # Por ejemplo, [0, 0, 4, 2] se normaliza a [4, 2].
        #si el coeficiente 0 (de mayor grado) es 0, se elimina.
        #esto solo es valido si el polinomio no es el polinomio nulo.

        while len(self.coeficientes) > 1 and self.coeficientes[0] == 0:
            self.coeficientes.pop(0)

    @property
    def grado(self) -> int:
        """
        Retorna el grado del polinomio, que corresponde a la longitud 
        de su lista de coeficientes menos 1.
        """
        resultado_grado = len(self.coeficientes) - 1
        return resultado_grado

    def __add__(self, otro_polinomio: 'GFPoly') -> 'GFPoly':
        """
        Sobrecarga del operador de suma (+).
        Suma este polinomio con otro_polinomio término a término
        mediante la suma del campo de Galois (XOR).
        """
        # Validaciones de tipo y de campo
        if not isinstance(otro_polinomio, GFPoly):
            raise TypeError("La suma solo es válida entre objetos de la clase GFPoly.")
        if self.campo != otro_polinomio.campo:
            raise ValueError("Ambos polinomios deben pertenecer al mismo campo de Galois para poder sumarse.")

        # Obtener longitudes de coeficientes para sumar  y la maxima entre las dos 
        longitud_self = len(self.coeficientes)
        longitud_otro = len(otro_polinomio.coeficientes)
        longitud_maxima = max(longitud_self, longitud_otro)

        # Alinear coeficientes agregando ceros a la izquierda para los términos de mayor grado
        # faltantes para poder sumar los coeficientes homologos iterando
        self_alineado = [0] * (longitud_maxima - longitud_self) + self.coeficientes
        otro_alineado = [0] * (longitud_maxima - longitud_otro) + otro_polinomio.coeficientes

        # Lista para almacenar los nuevos coeficientes sumados
        coeficientes_resultado = []

        # Sumar elemento a elemento con la funcion suma 
        for indice in range(longitud_maxima):
            suma_coeficientes = self.campo.suma(self_alineado[indice], otro_alineado[indice])
            coeficientes_resultado.append(suma_coeficientes)

        # Retornar una nueva instancia de GFPoly con el resultado de la suma
        return GFPoly(self.campo, coeficientes_resultado)

    def __sub__(self, otro_polinomio: 'GFPoly') -> 'GFPoly':
        """
        Sobrecarga del operador de resta (-).
        como es igual que la suma, llamamos al operador suma
        """
        return self.__add__(otro_polinomio)

    def __mul__(self, otro_polinomio: 'GFPoly') -> 'GFPoly':
        """
        Sobrecarga del operador de multiplicación (*).
        Multiplicación distributiva de polinomios, operando los coeficientes sobre el campo.
        """
        # Validaciones de tipo y de campo
        if not isinstance(otro_polinomio, GFPoly):
            raise TypeError("La multiplicación solo es válida entre objetos de la clase GFPoly.")
        if self.campo != otro_polinomio.campo:
            raise ValueError("Ambos polinomios deben pertenecer al mismo campo de Galois para poder multiplicarse.")

        # Si alguno es el polinomio nulo [0], el producto es el polinomio nulo [0]
        if self.coeficientes == [0] or otro_polinomio.coeficientes == [0]:
            return GFPoly(self.campo, [0])

        # El grado del polinomio producto es igual a la suma de los grados de los polinomios multiplicados
        longitud_self = len(self.coeficientes)
        longitud_otro = len(otro_polinomio.coeficientes)
        longitud_resultado = longitud_self + longitud_otro - 1 # -1 por el termino independiente

        # Inicialización de coeficientes resultado en cero para todos los grados posibles
        coeficientes_resultado = [0] * longitud_resultado

        # Multiplicación distributiva
        for indice_self in range(longitud_self):
            coeficiente_self = self.coeficientes[indice_self]
            # si el coeficiente es cero, no aporta términos al producto. pasamos al siguiente
            if coeficiente_self == 0:
                continue

            for indice_otro in range(longitud_otro):
                coeficiente_otro = otro_polinomio.coeficientes[indice_otro]
                if coeficiente_otro == 0:
                    continue

                # Multiplicar los coeficientes sobre el campo de Galois
                producto_coeficientes = self.campo.producto(coeficiente_self, coeficiente_otro)

                # Calcular la posición  resultante para que coincida con el grado 
                posicion_grado = indice_self + indice_otro

                # hacer XOR en el campo para sumar los exponentes (grados)
                # se suma el coeficiente resultado de la multiplicacion con el coeficiente que ya esta en la posicion 
                # del grado correspondiente para asi ir acumulando los coeficientes en su posicion correcta
                coeficientes_resultado[posicion_grado] = self.campo.suma(
                    coeficientes_resultado[posicion_grado],
                    producto_coeficientes
                )

        return GFPoly(self.campo, coeficientes_resultado)

    def division_polinomial(self, divisor: 'GFPoly') -> tuple['GFPoly', 'GFPoly']:
        """
        Realiza la división larga de polinomios con coeficientes en GF(2^m).
        Retorna una tupla conteniendo el polinomio cociente y el polinomio resto: (cociente, resto).
        """
        # Validaciones de tipo y campo
        if not isinstance(divisor, GFPoly):
            raise TypeError("El divisor debe ser un objeto de la clase GFPoly.")
        if self.campo != divisor.campo:
            raise ValueError("Ambos polinomios deben pertenecer al mismo campo de Galois para dividirse.")

        # Validar división por el polinomio nulo [0]
        if divisor.coeficientes == [0]:
            raise ZeroDivisionError("División polinomial por cero: el divisor no puede ser el polinomio nulo.")

        # Inicializar el resto como una copia de los coeficientes del dividendo
        coeficientes_resto = list(self.coeficientes)
        coeficientes_divisor = list(divisor.coeficientes)

        grado_dividendo = len(self.coeficientes) - 1
        grado_divisor = len(coeficientes_divisor) - 1

        # Caso en que el grado del DIVIDENDO es menor que el del DIVISOR:
        # El cociente es 0 y el resto es igual al dividendo.

        if grado_dividendo < grado_divisor:
            cociente_cero = GFPoly(self.campo, [0])
            resto_original = GFPoly(self.campo, self.coeficientes)
            return cociente_cero, resto_original

        # El tamaño y el grado del cociente está determinado por la diferencia de grados entre
        #dividendo y divisor +1 
        longitud_cociente = grado_dividendo - grado_divisor + 1 #cantidad de coef del cociente
        # inicializamos los coeficientes del cociente en 0
        coeficientes_cociente = [0] * longitud_cociente 

        # Bucle de división larga. Continúa mientras el resto tenga grado mayor o igual al divisor.
        # En cada paso eliminamos el término principal (de mayor grado) del resto.
        while len(coeficientes_resto) >= len(coeficientes_divisor) and coeficientes_resto != [0]:
            # Calcular grado actual del resto
            grado_actual_resto = len(coeficientes_resto) - 1

            # Términos principales del resto y divisor
            coeficiente_principal_resto = coeficientes_resto[0]
            coeficiente_principal_divisor = coeficientes_divisor[0]

            # Dividir los coeficientes del resto y divisor usando la división del campo
            coeficiente_termino_cociente = self.campo.division(
                coeficiente_principal_resto,
                coeficiente_principal_divisor
            )

            # El grado del nuevo término del cociente es la diferencia de grados
            grado_termino_cociente = grado_actual_resto - grado_divisor

            # Almacenar en la posición del cociente (mayor grado a menor grado)
            indice_cociente = len(coeficientes_cociente) - 1 - grado_termino_cociente
            coeficientes_cociente[indice_cociente] = coeficiente_termino_cociente

            # Multiplicar el divisor por el nuevo término y restarlo (sumarlo vía XOR) al resto.
            # Realizamos la operación término a término alineados en el resto actual.
            for indice_divisor in range(len(coeficientes_divisor)):
                coeficiente_divisor_actual = coeficientes_divisor[indice_divisor]
                
                # Multiplicar coeficientes
                termino_multiplicado = self.campo.producto(
                    coeficiente_divisor_actual,
                    coeficiente_termino_cociente
                )
                
                # XOR en el resto actual
                coeficientes_resto[indice_divisor] = self.campo.suma(
                    coeficientes_resto[indice_divisor],
                    termino_multiplicado
                )

            # Limpiar los ceros a la izquierda generados en la resta del término de mayor grado
            while len(coeficientes_resto) > 1 and coeficientes_resto[0] == 0:
                coeficientes_resto.pop(0)

        # Empaquetar resultados finales en instancias de GFPoly
        polinomio_cociente = GFPoly(self.campo, coeficientes_cociente)
        polinomio_resto = GFPoly(self.campo, coeficientes_resto)

        return polinomio_cociente, polinomio_resto

    def __floordiv__(self, otro_polinomio: 'GFPoly') -> 'GFPoly':
        """
        Sobrecarga del operador de cociente de división entera (//).
        Retorna la parte cociente de la división polinomial.
        """
        cociente, resto = self.division_polinomial(otro_polinomio)
        return cociente

    def __mod__(self, otro_polinomio: 'GFPoly') -> 'GFPoly':
        """
        Sobrecarga del operador de resto (%).
        Retorna la parte del resto de la división polinomial.
        """
        cociente, resto = self.division_polinomial(otro_polinomio)
        return resto

    def escalar(self, escalar_campo: int) -> 'GFPoly':
        """
        Multiplica todos los coeficientes de este polinomio por un escalar perteneciente al campo.
        """
        self.campo.validar_elemento(escalar_campo, f"El escalar ({escalar_campo})")

        # Si el escalar es 0, el resultado es el polinomio nulo [0]
        if escalar_campo == 0:
            return GFPoly(self.campo, [0])

        # Multiplicar cada coeficiente por el escalar usando la aritmética del campo
        coeficientes_escalados = []
        for coeficiente in self.coeficientes:
            coeficiente_resultado = self.campo.producto(coeficiente, escalar_campo)
            coeficientes_escalados.append(coeficiente_resultado)

        return GFPoly(self.campo, coeficientes_escalados)

    def evaluar(self, punto_x: int) -> int:
        """
        Evalúa el polinomio en un punto 'punto_x' perteneciente al campo GF(2^m).
        Utiliza el algoritmo de evaluación de Horner de forma secuencial y eficiente.
        """
        self.campo.validar_elemento(punto_x, f"El punto de evaluación ({punto_x})")

        # Acumulador para la evaluación polinomial
        valor_evaluado = 0

        # Algoritmo de Horner: acumulado = (acumulado * x) + coeficiente
        for coeficiente in self.coeficientes:
            # Multiplicar el acumulado por el punto x en el campo
            valor_evaluado = self.campo.producto(valor_evaluado, punto_x)
            # Sumar (XOR) el coeficiente actual
            valor_evaluado = self.campo.suma(valor_evaluado, coeficiente)

        return valor_evaluado

    @classmethod
    def construir_desde_raices(cls, campo: CampoDeGalois, lista_raices: list) -> 'GFPoly':
        """
        Construye y retorna un polinomio a partir de un conjunto de raíces especificadas.
        El polinomio resultante es el producto de (x - r_i) para cada raíz r_i en la lista.
        En característica 2, esto es equivalente al producto de (x + r_i).
        """
        if not isinstance(campo, CampoDeGalois):
            raise TypeError("El parámetro 'campo' debe ser una instancia de la clase CampoDeGalois.")
        if not isinstance(lista_raices, (list, tuple)):
            raise TypeError("Las raíces deben pasarse en formato de lista o tupla.")

        # Comenzar con el polinomio identidad p(x) = 1 (coeficiente [1])
        polinomio_acumulado = cls(campo, [1])

        # Multiplicar secuencialmente por cada factor de raíz (x + raiz)
        for raiz in lista_raices:
            campo.validar_elemento(raiz, f"La raíz ({raiz})")

            # Crear el polinomio binomio (1*x + raiz) -> representado como [1, raiz]
            polinomio_binomio = cls(campo, [1, raiz])
            # Multiplicar acumulado por el binomio
            polinomio_acumulado = polinomio_acumulado * polinomio_binomio

        return polinomio_acumulado

    def __eq__(self, otro_polinomio: object) -> bool:
        """
        Compara si este polinomio es igual a otro_polinomio.
        Deben pertenecer al mismo campo de Galois y poseer los mismos coeficientes término a término.
        """
        if not isinstance(otro_polinomio, GFPoly):
            return False
        # Deben pertenecer al mismo campo y tener la misma lista de coeficientes normalizada
        campos_iguales = self.campo == otro_polinomio.campo
        coeficientes_iguales = self.coeficientes == otro_polinomio.coeficientes
        return campos_iguales and coeficientes_iguales

    def __str__(self) -> str:
        """
        Retorna la representación legible del polinomio en forma de cadena de texto.
        Ejemplo: "5*x^2 + 3*x + 4"
        """
        # Caso del polinomio nulo
        if self.coeficientes == [0]:
            return "0"

        partes_texto = []
        grado_maximo = self.grado

        for posicion_indice, coeficiente in enumerate(self.coeficientes):
            # Grado de la variable en este coeficiente
            grado_actual = grado_maximo - posicion_indice

            # Omitimos coeficientes que sean 0
            if coeficiente == 0:
                continue

            # Formatear el término según su grado
            if grado_actual == 0:
                # Término independiente
                partes_texto.append(f"{coeficiente}")
            elif grado_actual == 1:
                # Término de grado 1 (lineal)
                partes_texto.append(f"{coeficiente}*x")
            else:
                # Términos de grado mayor
                partes_texto.append(f"{coeficiente}*x^{grado_actual}")

        # En GF(2^m) la resta es igual a la suma, usamos siempre el signo "+" para separar términos
        return " + ".join(partes_texto)

    def __repr__(self) -> str:
        """
        Retorna la representación para depuración de la instancia de GFPoly.
        """
        return f"GFPoly(campo=GF(2^{self.campo.orden_m}), coeficientes={self.coeficientes})"

