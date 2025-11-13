"""
pytest conftest.py (RAIZ) - Previne conflito crítico de multiprocessing com mutmut

Esse arquivo DEVE estar na raiz para ser encontrado antes de mutants/tests/conftest.py
"""
import sys
import multiprocessing as mp

# CRÍTICO: Fixar o método ANTES de qualquer coisa
try:
    mp.set_start_method('spawn', force=True)
except RuntimeError:
    # Já foi configurado, tudo bem
    pass
