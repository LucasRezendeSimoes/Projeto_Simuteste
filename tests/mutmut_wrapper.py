#!/usr/bin/env python3
"""
Wrapper para executar mutmut em modo serial, evitando conflitos de multiprocessing.
"""
import sys
import os

# Desabilitar multiprocessing ANTES de qualquer import de mutmut
os.environ['MUTMUT_DISABLE_MULTIPROCESSING'] = '1'

# Importar contexto de multiprocessing e forçar serial
import multiprocessing
multiprocessing.set_start_method('spawn', force=True)

# Agora importar e executar mutmut
from mutmut.__main__ import main

if __name__ == '__main__':
    # Adicionar argumentos para forçar modo serial
    sys.argv.extend(['--paths-to-mutate', 'app', '--tests-dir', 'tests'])
    main()
