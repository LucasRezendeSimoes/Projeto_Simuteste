# Guia de Mutation Testing - Sistema de Agendamento

## 📊 O que é Mutation Testing?

Mutation Testing é uma técnica de teste que avalia a qualidade dos testes introduzindo pequenas mudanças (mutações) no código e verificando se os testes conseguem detectá-las.

## 🔧 Configuração Mutmut

O projeto está configurado em `setup.cfg`:

```ini
[mutmut]
paths_to_mutate=app
tests_dir=tests
max_workers=1
tests_dir_name=tests
```

## 🚀 Como Executar

### Via terminal (recomendado)
```bash
python -m mutmut run
```

### Ver resultados
```bash
python -m mutmut results
python -m mutmut results --show-times
```

### Gerar relatório HTML
```bash
python -m mutmut html
```

## 📈 Interpretação de Resultados

### Status dos Mutantes

1. **Killed** ✅
   - O mutante foi detectado pelos testes
   - Indica teste de boa qualidade

2. **Survived** ❌
   - O mutante não foi detectado
   - Indica falta de cobertura ou teste fraco

3. **Suspicious** ⚠️
   - O resultado foi suspeitosamente próximo ao esperado
   - Requer investigação

## 📊 Métricas Esperadas

- **Taxa de Mortalidade**: Percentual de mutantes mortos (killed)
- **Objetivo**: >80% de mortalidade

## 🎯 Melhorias Recomendadas

1. **Aumentar cobertura de API** (0%)
   - Adicionar testes de integração
   - Testar endpoints com `TestClient` do FastAPI

2. **Testar mais cenários em Services** (69%)
   - Testes de limite (boundary tests)
   - Testes de exceção
   - Testes de integração completa

3. **Aumentar cobertura de Repositories** (44%)
   - Testes com banco de dados real
   - Testes de filtros e ordenações complexas

## 📝 Notas Importantes

- **Mutant Database**: `.mutmut.db` - Armazena resultados de execuções anteriores
- **Pasta de Mutantes**: `mutants/` - Contém código mutado temporariamente
- **Tempo de Execução**: Pode levar alguns minutos dependendo do tamanho do código

## ⚠️ Troubleshooting

### Erro: "context has already been set"
Este é um problema conhecido com `multiprocessing`. Soluções:

1. Usar `max_workers=1` na configuração:
```ini
[mutmut]
max_workers=1
```

2. Executar em um novo processo:
```bash
python -c "from mutmut.__main__ import main; main()" run
```

3. Limpar estado anterior:
```bash
rm -rf .mutmut.db mutants/
python -m mutmut run
```

## 📚 Referências

- [Documentação Mutmut](https://mutmut.readthedocs.io/)
- [Mutation Testing - Wikipédia](https://en.wikipedia.org/wiki/Mutation_testing)

---

## ✅ Checklist para Entrega

- [x] Mutation testing configurado
- [x] Setup.cfg criado
- [x] Instruções documentadas
- [x] Exemplo de execução
- [ ] Relatório de mutantes gerado (executar em local)

**Status**: Pronto para usar em ambiente local! 🚀
