# Projeto da matéria de simulação e teste de software

## Participantes:
### Alan Daiki Suga
RA: 22.125.094-7

### Lucas Rezende Simões
RA: 24.122.028-4

### Rodrigo Simões Ruy
RA: 24.122.092-0

### Rômulo C O Canavesso
RA: 24.122.093-8

# Instruções

## Avisos
### O programa precisa ser rodado em linux ou no codespace por causa da biblioteca mutmut.

## Instalação

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/LucasRezendeSimoes/Projeto_Simuteste.git
   ```

2. **Crie um ambiente virtual (recomendado):**
   ```bash
   python -m venv venv
   
   source venv/bin/activate
   ```

3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```


## Como realizar os testes
### 1. Executar testes
pytest tests/test_complete.py -v

### 2. Ver cobertura
pytest --cov=app --cov-report=html

### 3. Abrir relatório
open htmlcov/index.html

### 4. Mutation testing
python -m mutmut run
