#!/usr/bin/env python3
"""
Script para executar mutmut em modo isolado (subprocess puro).
Evita conflito 'context has already been set' em ambientes containerizados.

Uso: python run_mutmut.py
"""
import subprocess
import sys
import os
import shutil

def cleanup_mutants():
    """Remove pasta mutants/ e cache para evitar herança de estado"""
    mutants_path = './mutants'
    if os.path.exists(mutants_path):
        print(f"🧹 Limpando pasta {mutants_path}...")
        shutil.rmtree(mutants_path)
    
    # Remover cache
    if os.path.exists('.mutmut.cache'):
        os.remove('.mutmut.cache')
        print("🧹 Cache limpo")

def main():
    print("=" * 70)
    print("🧬 INICIANDO MUTATION TESTING (MODO SEGURO)")
    print("=" * 70)
    
    # Limpar estado anterior
    cleanup_mutants()
    
    env = os.environ.copy()
    env['PYTHONUNBUFFERED'] = '1'
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    
    # Usar wrapper seguro que patcheia mutmut antes da execução
    cmd = [sys.executable, 'mutmut_safe.py']
    
    print(f"\n📋 Comando: {' '.join(cmd)}")
    print(f"📁 Diretório: {os.getcwd()}")
    print(f"⚙️  Configuração: setup.cfg")
    print(f"🛡️  Proteção: mutmut_safe.py (patcheia multiprocessing)")
    print("\n" + "=" * 70 + "\n")
    
    try:
        result = subprocess.run(cmd, env=env, check=False)
        
        print("\n" + "=" * 70)
        if result.returncode == 0:
            print("✅ MUTATION TESTING CONCLUÍDO COM SUCESSO")
            print("=" * 70)
            print("\n📊 Para visualizar resultados:")
            print("   1. Listar mutantes: python -m mutmut results")
            print("   2. Gerar HTML:     python -m mutmut html")
            print("   3. Ver detalhes:   cat .mutmut.cache")
        else:
            print(f"⚠️  MUTATION TESTING COMPLETADO COM EXIT CODE: {result.returncode}")
            print("=" * 70)
            print("\nℹ️  Possíveis causas:")
            print("   - Ambiente containerizado com restrições de multiprocessing")
            print("   - Conflito de contexto Python (já configurado)")
            print("   - Testes falhando ao rodar em modo mutado")
            print("\n💡 Soluções:")
            print("   1. Tentar: python mutmut_safe.py")
            print("   2. Ou use modo local em máquina física")
            print("   3. Verifique: python -m pytest tests/ (testes originais passam?)")
        print("\n" + "=" * 70)
        
        return result.returncode
        
    except KeyboardInterrupt:
        print("\n⚠️  Interrompido pelo usuário")
        return 1
    except Exception as e:
        print(f"\n❌ ERRO: {e}")
        return 1

if __name__ == '__main__':
    sys.exit(main())
