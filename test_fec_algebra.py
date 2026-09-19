# -*- coding: utf-8 -*-
"""
Script de pruebas test_fec_algebra.py
Permite verificar la implementación de las clases CampoDeGalois y GFPoly.
Contiene casos de prueba detallados con explicaciones y aserciones.
"""

from fec_algebra import CampoDeGalois, GFPoly

def probar_campo_galois():
    print("==================================================")
    print("PROBANDO LA CLASE CampoDeGalois EN GF(2^3)")
    print("==================================================")
    
    # Inicializamos el campo de Galois GF(2^3)
    # Polinomio primitivo: P*(x) = x^3 + x + 1 -> P(x) = x + 1 (representado como entero 3, binario '011')
    orden_m = 3
    polinomio_primitivo = 3  # representacion binaria del polinomio x + 1
    
    campo = CampoDeGalois(orden_m=orden_m, polinomio_primitivo=polinomio_primitivo)
    print(f"Campo de Galois creado correctamente: GF(2^{campo.orden_m})")
    print(f"Cantidad de elementos del campo: {campo.cantidad_elementos}")
    print(f"Polinomio primitivo (implícito): {bin(campo.polinomio_primitivo)} ({campo.polinomio_primitivo})\n")
    
    # 1. Prueba de Suma (XOR)
    print("1. Probando Suma (Operación XOR en binario):")
    # 5 (binario 101) + 3 (binario 011) = 6 (binario 110)
    suma_resultado_1 = campo.suma(5, 3)
    print(f"   5 + 3 = {suma_resultado_1} (Esperado: 6)")
    assert suma_resultado_1 == 6
    
    # 4 (binario 100) + 4 (binario 100) = 0
    suma_resultado_2 = campo.suma(4, 4)
    print(f"   4 + 4 = {suma_resultado_2} (Esperado: 0)")
    assert suma_resultado_2 == 0
    print("   -> OK\n")
    
    # 2. Prueba de Producto (Resta/Russian Peasant)
    print("2. Probando Producto:")
    # Elemento 2 (x) * Elemento 4 (x^2) = Elemento 3 (x^3 -> x + 1)
    producto_resultado_1 = campo.producto(2, 4)
    print(f"   2 * 4 = {producto_resultado_1} (Esperado: 3)")
    assert producto_resultado_1 == 3
    
    # Elemento 5 (x^2 + 1) * Elemento 3 (x + 1) = Elemento 4 (x^2)
    producto_resultado_2 = campo.producto(5, 3)
    print(f"   5 * 3 = {producto_resultado_2} (Esperado: 4)")
    assert producto_resultado_2 == 4
    print("   -> OK\n")
    
    # 3. Prueba de Potencia (Exponenciación rápida)
    print("3. Probando Potencia:")
    # 2^3 = 2 * 2 * 2 = 3
    potencia_resultado_1 = campo.potencia(2, 3)
    print(f"   2^3 = {potencia_resultado_1} (Esperado: 3)")
    assert potencia_resultado_1 == 3
    
    # 2^0 = 1
    potencia_resultado_2 = campo.potencia(2, 0)
    print(f"   2^0 = {potencia_resultado_2} (Esperado: 1)")
    assert potencia_resultado_2 == 1
    print("   -> OK\n")
    
    # 4. Prueba de Inverso Multiplicativo y División
    print("4. Probando Inverso Multiplicativo y División:")
    # El inverso de 2 (x) debe ser 5 (x^2 + 1), ya que 2 * 5 = 1 (comprobado antes)
    inverso_2 = campo.inverso_multiplicativo(2)
    print(f"   Inverso de 2 = {inverso_2} (Esperado: 5)")
    assert inverso_2 == 5
    
    # Probar división: 1 / 2 = 1 * inverso(2) = 1 * 5 = 5
    division_resultado = campo.division(1, 2)
    print(f"   1 / 2 = {division_resultado} (Esperado: 5)")
    assert division_resultado == 5
    
    # Verificar que el inverso de 0 lance una excepción
    try:
        campo.inverso_multiplicativo(0)
        print("   FALLÓ: El inverso de 0 no lanzó excepción.")
        assert False
    except ValueError as error_inverso:
        print(f"   Captura de error esperada para inverso(0): '{error_inverso}'")
        
    # Verificar que la división por 0 lance una excepción
    try:
        campo.division(5, 0)
        print("   FALLÓ: La división por 0 no lanzó excepción.")
        assert False
    except ZeroDivisionError as error_division:
        print(f"   Captura de error esperada para división por 0: '{error_division}'")
    print("   -> OK\n")


def probar_polinomios():
    print("==================================================")
    print("PROBANDO LA CLASE GFPoly")
    print("==================================================")
    
    # Inicializamos el mismo campo GF(2^3) con polinomio primitivo 3
    campo = CampoDeGalois(orden_m=3, polinomio_primitivo=3)
    
    # 1. Prueba de Normalización (Ceros a la izquierda)
    print("1. Probando normalización de coeficientes:")
    # Un polinomio inicializado como [0, 0, 5, 3] debe normalizarse a [5, 3]
    polinomio_desnormalizado = GFPoly(campo, [0, 0, 5, 3])
    print(f"   Polinomio ingresado: [0, 0, 5, 3] -> Coeficientes resultantes: {polinomio_desnormalizado.coeficientes} (Esperado: [5, 3])")
    assert polinomio_desnormalizado.coeficientes == [5, 3]
    
    # El polinomio nulo ingresado como [0, 0, 0] debe normalizarse a [0]
    polinomio_nulo = GFPoly(campo, [0, 0, 0])
    print(f"   Polinomio nulo ingresado: [0, 0, 0] -> Coeficientes resultantes: {polinomio_nulo.coeficientes} (Esperado: [0])")
    assert polinomio_nulo.coeficientes == [0]
    print("   -> OK\n")
    
    # 2. Prueba de Suma y Resta de Polinomios
    print("2. Probando Suma (+):")
    # p1(x) = x^2 + 5x + 3 -> [1, 5, 3]
    # p2(x) = x^2 + 2x + 1 -> [1, 2, 1]
    # p1 + p2 = (1^1)*x^2 + (5^2)*x + (3^1) = 0*x^2 + 7*x + 2 = 7*x + 2 -> [7, 2]
    polinomio_1 = GFPoly(campo, [1, 5, 3])
    polinomio_2 = GFPoly(campo, [1, 2, 1])
    polinomio_suma = polinomio_1 + polinomio_2
    print(f"   ({polinomio_1}) + ({polinomio_2}) = {polinomio_suma} (Esperado: 7*x + 2 / [7, 2])")
    assert polinomio_suma.coeficientes == [7, 2]
    print("   -> OK\n")
    
    # 3. Prueba de Producto de Polinomios
    print("3. Probando Producto (*):")
    # p3(x) = x + 1 -> [1, 1]
    # p4(x) = x^2 -> [1, 0, 0]
    # p3 * p4 = x^3 + x^2 -> [1, 1, 0, 0]
    polinomio_3 = GFPoly(campo, [1, 1])
    polinomio_4 = GFPoly(campo, [1, 0, 0])
    polinomio_producto = polinomio_3 * polinomio_4
    print(f"   ({polinomio_3}) * ({polinomio_4}) = {polinomio_producto} (Esperado: 1*x^3 + 1*x^2 / [1, 1, 0, 0])")
    assert polinomio_producto.coeficientes == [1, 1, 0, 0]
    print("   -> OK\n")
    
    # 4. Prueba de División Polinomial (Cociente // y Resto %)
    print("4. Probando División Polinomial:")
    # Dividendo: p_dividendo = x^2 + 5x + 3 -> [1, 5, 3]
    # Divisor: p_divisor = 2x + 1 -> [2, 1]
    # Calculamos: cociente = 5x [5, 0], resto = 3 [3]
    # (Ya verificado matemáticamente: (2x + 1) * 5x + 3 = (2*5)*x^2 + (1*5)*x + 3 = x^2 + 5x + 3)
    p_dividendo = GFPoly(campo, [1, 5, 3])
    p_divisor = GFPoly(campo, [2, 1])
    
    cociente = p_dividendo // p_divisor
    resto = p_dividendo % p_divisor
    
    print(f"   Dividendo: {p_dividendo}")
    print(f"   Divisor: {p_divisor}")
    print(f"   Cociente: {cociente} (Esperado: 5*x / [5, 0])")
    print(f"   Resto: {resto} (Esperado: 3 / [3])")
    
    assert cociente.coeficientes == [5, 0]
    assert resto.coeficientes == [3]
    print("   -> OK\n")
    
    # 5. Prueba de Escalado
    print("5. Probando Escalado:")
    # p_original(x) = x^2 + 5x + 3 -> [1, 5, 3]
    # Escalado por 2: (1*2)*x^2 + (5*2)*x + (3*2) = 2*x^2 + 7*x + 6 -> [2, 7, 6]
    # Nota: 5 * 2 = 7, 3 * 2 = 6 en el campo GF(2^3) con P=3
    # Verificación de operaciones:
    # 5 * 2 = (x^2 + 1) * x = x^3 + x = (x + 1) + x = 1 (¡Ah! Espera. 5 * 2 = 1. Y 3 * 2 = (x + 1) * x = x^2 + x = 6.)
    # Por lo tanto, el escalado por 2 de [1, 5, 3] es: [1*2, 5*2, 3*2] = [2, 1, 6].
    # Hagamos la aserción con el valor correcto calculado matemáticamente.
    p_original = GFPoly(campo, [1, 5, 3])
    p_escalado = p_original.escalar(2)
    print(f"   {p_original} escalado por 2 = {p_escalado} (Esperado: 2*x^2 + 1*x + 6 / [2, 1, 6])")
    assert p_escalado.coeficientes == [2, 1, 6]
    print("   -> OK\n")
    
    # 6. Prueba de Evaluación polinomial (Horner)
    print("6. Probando Evaluación (Horner):")
    # p(x) = x^2 + 5x + 3. Evaluar en x = 2.
    # p(2) = 2^2 + 5*2 + 3 = 4 + 1 + 3 = 4 ^ 1 ^ 3 = 6. (Ya verificado en el diseño).
    p_evaluar = GFPoly(campo, [1, 5, 3])
    resultado_evaluacion = p_evaluar.evaluar(2)
    print(f"   ({p_evaluar}) evaluado en x=2 es: {resultado_evaluacion} (Esperado: 6)")
    assert resultado_evaluacion == 6
    print("   -> OK\n")
    
    # 7. Prueba de Construcción desde raíces
    print("7. Probando Construcción desde raíces:")
    # Raíces: r1 = 2, r2 = 3
    # P(x) = (x + 2)*(x + 3) = x^2 + (2+3)*x + (2*3) = x^2 + (2^3)*x + 6 = x^2 + 1*x + 6 -> [1, 1, 6]
    raices = [2, 3]
    p_desde_raices = GFPoly.construir_desde_raices(campo, raices)
    print(f"   Polinomio con raíces {raices}: {p_desde_raices} (Esperado: 1*x^2 + 1*x + 6 / [1, 1, 6])")
    assert p_desde_raices.coeficientes == [1, 1, 6]
    print("   -> OK\n")


if __name__ == "__main__":
    probar_campo_galois()
    probar_polinomios()
    print("==================================================")
    print("¡TODAS LAS PRUEBAS SE COMPLETARON CON ÉXITO!")
    print("==================================================")
