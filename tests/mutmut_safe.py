#!/usr/bin/env python3
"""
Patch para mutmut - Previne 'context has already been set' error

Este script é um monkey-patch que torna mutmut mais resiliente em
ambientes containerizados com multiprocessing pré-inicializado.
"""
import sys
import multiprocessing as mp

# Passo 1: Pré-configurar multiprocessing com spawn (mais seguro em containers)
try:
    mp.set_start_method('spawn', force=True)
except RuntimeError:
    # Já configurado, tudo bem
    pass

# Passo 2: PATCH multiprocessing.set_start_method para ser idempotente
original_set_start_method = mp.set_start_method

def safe_set_start_method(method, force=False):
    """Wrapper que ignora 'context has already been set' error"""
    try:
        return original_set_start_method(method, force=force)
    except RuntimeError as e:
        if 'context has already been set' in str(e):
            # Esperado em ambientes containerizados
            # Retornar None silenciosamente em vez de relancar
            pass
        else:
            raise

# APLICAR PATCH GLOBAL ANTES DE QUALQUER OUTRO IMPORT
mp.set_start_method = safe_set_start_method

# Passo 3: Importar e executar mutmut CLI
from mutmut.__main__ import cli

# Passo 4: Executar
if __name__ == '__main__':
    cli()
