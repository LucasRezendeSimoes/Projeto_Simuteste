"""
pytest conftest.py - Configuração para evitar conflito de multiprocessing com mutmut

Este arquivo configura pytest para funcionar adequadamente com mutmut
em ambientes containerizados onde há conflitos de contexto de multiprocessing.
"""
import sys
import os
import multiprocessing

# CRÍTICO: Evitar que mutmut/pytest configurem multiprocessing duas vezes
# Deve ser feito ANTES de qualquer import de pytest ou mutmut
try:
    # Se este código está rodando, significa que multiprocessing já foi inicializado
    # Não deixe que qualquer tentativa de set_start_method() seja feita
    multiprocessing.set_start_method('spawn', force=True)
except RuntimeError:
    # Já foi configurado, ignore o erro
    pass

# Configuração padrão do pytest
pytest_plugins = []

def pytest_configure(config):
    """Hook que roda ANTES de qualquer teste"""
    # Garantir que está em modo serial
    if hasattr(config, 'option'):
        # Desabilitar xdist se estiver rodando com mutmut
        if 'mutmut' in sys.modules or any('mutmut' in str(arg) for arg in sys.argv):
            config.option.maxfail = 1  # Parar no primeiro erro se algo der errado

