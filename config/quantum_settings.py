"""
================================================================================
PROYECTO: IA-Energy-Alternatives
ARCHIVO: config/quantum_settings.py
GRUPO: Dark Shadows Group
================================================================================

JUSTIFICACIÓN ARQUITECTÓNICA (¿POR QUÉ HACEMOS ESTO?):

1. DESACOPLAMIENTO DE RUNTIMES:
   Centralizar la instanciación de las primitivas de Qiskit (Estimator) y los 
   optimizadores clásicos evita la redundancia de código en los notebooks vectoriales. 
   Si mañana migramos de un simulador local de Aer a una QPU real de IBM a través de 
   QiskitRuntimeService, solo modificamos este archivo y el resto del pipeline 
   permanece intacto.

2. OPTIMIZACIÓN LOCAL (ERA NISQ):
   Configuramos el AerEstimator con aproximación por matriz de densidad / vector de 
   estado puro (shots=None). Esto permite obtener valores de expectativa exactos 
   durante la fase de desarrollo matemático, acelerando la convergencia del bucle 
   variacional sin el cuello de botella del ruido estadístico de disparo.
================================================================================
"""

from qiskit_aer.primitives import Estimator as AerEstimator
from qiskit_algorithms.optimizers import COBYLA

def get_local_quantum_backend():
    """
    Instancia el simulador local de alto rendimiento Aer.
    Se deshabilitan los shots para calcular el valor esperado exacto 
    del operador matemático mediante álgebra lineal pura.
    """
    return AerEstimator(run_options={"shots": None, "method": "statevector"})

def get_optimizer(maxiter=150):
    """
    Devuelve el optimizador clásico COBYLA (Constrained Optimization BY Linear Approximation).
    Elegido porque no requiere el cálculo de gradientes numéricos, lo cual es altamente
    eficiente cuando se simulan funciones de costo cuánticas ruidosas o no analíticas.
    """
    return COBYLA(maxiter=maxiter)