# 🧬 Guia Completo: Mutation Testing com mutmut

## 📋 Visão Geral

**Mutation Testing** é uma técnica que avalia a qualidade de testes introduzindo pequenas mudanças (mutações) no código e verificando se os testes conseguem detectá-las. Se um teste não consegue matar uma mutação, significa que o teste é fraco ou a cobertura é inadequada.

---

## ⚙️ Configuração do Projeto

### `setup.cfg` (Configuração Mutmut)

```ini
[mutmut]
paths_to_mutate=app
tests_dir=tests
max_workers=1
tests_dir_name=tests
multiprocessing=false
pure_python=true
skip_cache=true
```

**O que cada opção faz:**

| Opção | Valor | Significado |
|-------|-------|-------------|
| `paths_to_mutate` | `app` | Apenas módulos em `app/` serão mutados |
| `tests_dir` | `tests` | Procura testes em `tests/` |
| `max_workers` | `1` | Usa apenas 1 processo (evita conflitos) |
| `multiprocessing` | `false` | Desabilita paralelismo |
| `pure_python` | `true` | Usa Python puro, sem extensões C |
| `skip_cache` | `true` | Ignora cache anterior (sempre fresco) |

### `pytest.ini` (Configuração Pytest)

```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -v --tb=short -p no:cacheprovider
norecursedirs = mutants .git venv .venv htmlcov
```

**Importante**: `norecursedirs = mutants` evita que pytest tente executar código mutado gerado por mutmut.

### `conftest.py` (Raiz do Projeto)

Pré-configura multiprocessing com `spawn` para evitar conflitos em ambientes containerizados.

---

## 🚀 Como Executar

### Opção 1️⃣: Script Wrapper (Recomendado)

```bash
# Comando mais simples
python run_mutmut.py
```

**O que faz:**
1. Limpa state anterior (`mutants/`, `.mutmut.cache`)
2. Executa mutation testing com proteções ativadas
3. Mostra resultado final com próximos passos

### Opção 2️⃣: Script Seguro (Avançado)

```bash
# Executa mutmut com patches de segurança
python mutmut_safe.py run
```

**Diferença**: Não limpa cache automaticamente (mais rápido para re-execução)

### Opção 3️⃣: Direto com mutmut (Manual)

```bash
# Menos flexível, pode ter problemas em containers
python -m mutmut run
```

---

## 📊 Visualizar Resultados

Após executar (se bem-sucedido):

### 1. Listar Mutantes

```bash
# Mostra todos os mutantes e seus status
python -m mutmut results
```

**Exemplo de saída:**
```
app/services.py:42 -> ❌ survived (teste não detectou)
app/services.py:45 -> ✅ killed (teste detectou)
app/schemas.py:15 -> ✅ killed
```

### 2. Ver Mutante Específico

```bash
# Ver o que foi mutado em determinada linha
python -m mutmut show app/services.py:42
```

### 3. Gerar Relatório HTML

```bash
# Cria pasta html/ com relatório interativo
python -m mutmut html
```

Depois abrir em navegador:
```bash
# Linux
xdg-open html/index.html

# macOS
open html/index.html

# Windows
start html/index.html
```

**HTML inclui:**
- Resumo por arquivo
- Gráfico de sobrevivência
- Código com mutações destacadas
- Links para reprodruzir cada mutação

---

## 🔍 Entender Status dos Mutantes

| Status | Emoji | Significado | Ação |
|--------|-------|-------------|------|
| **Killed** | ✅ | Teste detectou a mutação | Bom! |
| **Survived** | ❌ | Teste não detectou | Adicionar teste |
| **Skipped** | ⏭️ | Mutante foi ignorado | Verificar config |
| **Timeout** | ⏸️ | Teste demorou demais | Otimizar teste |
| **Error** | 💥 | Erro ao executar | Debug necessário |

### Exemplo Prático

**Código original:**
```python
def validate_duration(duration: int) -> bool:
    return duration > 0  # Linha 42
```

**Mutação 1 (survived):**
```python
def validate_duration(duration: int) -> bool:
    return duration >= 0  # Mudou > para >=
```
Se nenhum teste testa `duration == 0`, essa mutação sobrevive → **Falta teste!**

**Mutação 2 (killed):**
```python
def validate_duration(duration: int) -> bool:
    return duration < 0  # Mudou > para <
```
Existem testes que verificam `duration > 0` → Teste mata essa mutação → **Bom!**

---

## 📈 Interpretar Taxa de Mortalidade

### Métrica Principal: Kill Rate

```
Kill Rate = (Mutantes Mortos / Total de Mutantes) × 100%
```

**Interpretação:**

| Kill Rate | Qualidade | Ação |
|-----------|-----------|------|
| **> 85%** | 🟢 Excelente | Ótimo! Continue assim |
| **75-85%** | 🟢 Bom | Considere melhorias |
| **60-75%** | 🟡 Aceitável | Adicione mais testes |
| **45-60%** | 🟡 Fraco | Melhore testes urgente |
| **< 45%** | 🔴 Muito Fraco | Reescreva testes |

### Projeto Atual

- **Cobertura de Código**: 53% (192 de 364 linhas)
- **Cobertura de Branches**: ~70% em módulos testados
- **Kill Rate Esperado**: 65-75% (bom para projeto educacional)

---

## ⚠️ Problemas Conhecidos

### ❌ Erro 1: "RuntimeError: context has already been set"

**Causa**: Ambiente containerizado (Docker, Codespace) pré-configura multiprocessing.

**Sintoma completo:**
```
RuntimeError: context has already been set
  File "mutmut/__main__.py", line 921, in <module>
    set_start_method('fork')
  File "multiprocessing/context.py", line 247, in set_start_method
```

**Soluções (em ordem de recomendação):**

1. ✅ **Use `run_mutmut.py` (Automático)**
   ```bash
   python run_mutmut.py
   ```

2. ✅ **Use `mutmut_safe.py` (Manual)**
   ```bash
   python mutmut_safe.py run
   ```

3. ⚠️ **Execute em máquina local**
   ```bash
   # Clone projeto localmente e rode lá
   python run_mutmut.py
   ```

### ❌ Erro 2: "AttributeError: 'NoneType' object has no attribute 'should_ignore_for_mutation'"

**Causa**: Bug interno de mutmut v3.3.1 em ambientes containerizados.

**Status**: Limitação conhecida (não há fix universal).

**Workaround**:
- Execute em máquina física (VirtualBox, laptop, servidor)
- Ou espere atualização de mutmut

### ❌ Erro 3: "Tests failed to run"

**Causa**: Seus testes têm erros.

**Solução**:
```bash
# Verificar que testes passam normalmente
pytest -v

# Se todos passarem, tente:
python mutmut_safe.py run
```

### ❌ Erro 4: "TIMEOUT: test suite took too long"

**Causa**: Testes demoram demais para rodar em cada mutação.

**Solução**:
```bash
# Aumentar timeout em setup.cfg:
[mutmut]
tests_timeout = 300  # segundos
```

---

## 🛠️ Troubleshooting Avançado

### Passo 1: Verificar ambiente

```bash
# Verificar Python
python --version  # Deve ser 3.10+

# Verificar pacotes
pip list | grep -E "mutmut|pytest"

# Verificar testes passam
pytest -v --tb=short
```

### Passo 2: Limpar estado

```bash
# Remover todos os artefatos de mutmut
rm -rf mutants/
rm -f .mutmut.cache
rm -f .mutmut.db
```

### Passo 3: Reinstalar pacotes

```bash
# Desinstalar
pip uninstall mutmut pytest -y

# Reinstalar
pip install 'mutmut==3.3.1' 'pytest==9.0.0'
```

### Passo 4: Tentar diferentes métodos

```bash
# Método 1
python run_mutmut.py

# Se falhar, método 2
python mutmut_safe.py run

# Se falhar, método 3 (debug)
python -c "import mutmut; print(mutmut.__version__)"
```

### Passo 5: Coletar informações para debug

```bash
# Criar arquivo de debug
{
  echo "=== Versão Python ==="
  python --version
  
  echo "=== Versão de Pacotes ==="
  pip list | grep -E "mutmut|pytest|pydantic"
  
  echo "=== Testes Passam? ==="
  pytest -v --tb=line 2>&1 | tail -20
  
  echo "=== Config Mutmut ==="
  cat setup.cfg
  
} > debug_info.txt

# Compartilhar debug_info.txt se precisar de ajuda
```

---

## 📝 Boas Práticas

### 1. Antes de Rodar Mutation Testing

```bash
# ✅ SEMPRE fazer isso primeiro
pytest -v              # Todos os testes devem passar
pytest --cov=app       # Ver cobertura atual
```

### 2. Interpretar Resultados

```bash
# ✅ Rodar mutation testing
python run_mutmut.py

# ✅ Listar sobreviventes
python -m mutmut results | grep survived

# ✅ Para cada survived, analisar:
python -m mutmut show app/module.py:LINEA
```

### 3. Melhorar Testes

**Se encontrou mutação que sobreviveu:**

```python
# ❌ Teste fraco
def test_duration():
    assert validate_duration(1)  # Só testa caso positivo

# ✅ Teste forte
def test_duration():
    assert validate_duration(1)      # Positivo
    assert not validate_duration(0)  # Zero (mata mutação > vs >=)
    assert not validate_duration(-1) # Negativo
    assert not validate_duration("")  # Tipo errado
```

### 4. Re-executar e Comparar

```bash
# Rodar novamente após adicionar testes
python run_mutmut.py

# Comparar kill rate antes vs depois
python -m mutmut results
```

---

## 📊 Exemplo: Passo a Passo Completo

### Cenário: Melhorar cobertura de `schemas.py`

**1. Ver estado atual**
```bash
pytest --cov=app --cov-report=term-missing
# schemas.py: 96% (97 de 100 linhas)
```

**2. Rodar mutation testing**
```bash
python run_mutmut.py
```

**3. Ver resultados**
```bash
python -m mutmut results | grep "schemas.py"
# app/schemas.py:50 -> survived
# app/schemas.py:52 -> killed
```

**4. Investigar survived**
```bash
python -m mutmut show app/schemas.py:50
# Original: if start_time <= datetime.now()
# Mutado:   if start_time < datetime.now()  # < vs <=
# Nenhum teste verifica `start_time == datetime.now()`
```

**5. Adicionar teste**
```python
def test_appointment_exact_now():
    """Testa que start_time NÃO pode ser exatamente agora"""
    with pytest.raises(ValueError):
        AppointmentCreate(
            user_id=1,
            start_time=datetime.now(),  # Exatamente agora
            duration_minutes=60
        )
```

**6. Re-executar mutation testing**
```bash
python run_mutmut.py
# Agora: app/schemas.py:50 -> killed ✅
```

---

## ✅ Checklist de Execução Completa

- [ ] Todos os testes passam: `pytest -v`
- [ ] Coverage aceitável: `pytest --cov=app`
- [ ] Limpar estado anterior: `rm -rf mutants/ .mutmut.cache`
- [ ] Executar mutation testing: `python run_mutmut.py`
- [ ] Aguardar conclusão (5-15 minutos)
- [ ] Ver sobreviventes: `python -m mutmut results`
- [ ] Analisar cada survived: `python -m mutmut show app/...:NN`
- [ ] Adicionar testes para sobreviventes
- [ ] Re-executar e confirmar morte
- [ ] Gerar relatório final: `python -m mutmut html`

---

## 📚 Recursos Adicionais

**Documentação:**
- [Mutmut Oficial](https://mutmut.readthedocs.io/)
- [Wikipedia - Mutation Testing](https://en.wikipedia.org/wiki/Mutation_testing)
- [PyCQA - Code Quality in Python](https://github.com/PyCQA)

**Conceitos:**
- [Mutation Score Indicator (MSI)](https://en.wikipedia.org/wiki/Mutation_testing#Mutation_score)
- [Equivalent Mutants](https://en.wikipedia.org/wiki/Mutation_testing#Equivalent_mutants)

---

## 🎯 Resumo

| Aspecto | Status | Ação |
|--------|--------|------|
| **Configuração** | ✅ Completa | Não mude |
| **Executor** | ✅ Pronto | Use `python run_mutmut.py` |
| **Ambiente** | ⚠️ Container | Pode ter limitações |
| **Cobertura** | ✅ 53% | Aceitável para projeto |
| **Documentação** | ✅ Completa | Você está lendo |

**Resultado Final**: Projeto **pronto para mutation testing**! 🚀

