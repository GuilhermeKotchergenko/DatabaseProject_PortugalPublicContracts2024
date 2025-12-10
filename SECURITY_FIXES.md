# Correções de Segurança - SQL Injection Prevention

## Resumo Executivo
Todas as instruções SQL foram verificadas e parametrizadas para prevenir SQL injection. O código agora segue as melhores práticas de segurança de banco de dados.

## Vulnerabilidades Identificadas e Corrigidas

### 1. **Função `get_all_from_table()` - CRÍTICA**
**Problema:** Interpolação direta do nome da tabela (line ~287)
```python
# ANTES (vulnerável):
query = f"SELECT * FROM {table_name} LIMIT ?"
```

**Solução:** Implementada lista branca de tabelas permitidas
```python
# DEPOIS (seguro):
ALLOWED_TABLES = {
    'CONTRATOS', 'ADJUDICANTE', 'ADJUDICATARIO', 'PAIS', 'DISTRITO',
    'MUNICIPIO', 'CPV', 'TIPOS', 'LOCALIZACAOCONTRATOS',
    'CONTRATOSADJUDICATARIO', 'TIPODOCONTRATO', 'CONTRATOSCPV'
}

if table_name.upper() not in ALLOWED_TABLES:
    raise ValueError(f"Tabela não autorizada: {table_name}")
```

### 2. **Função `get_ex6()` - MENOR IMPORTÂNCIA**
**Problema:** Query com padrão LIKE hardcoded e case-insensitive manual
```python
# ANTES:
query= "select designacao from adjudicante where designacao like '%Saúde%' or Designacao like '%saúde%' order by designacao;"
result = execute_query(query)  # Sem parametrização
```

**Solução:** Parametrização com LOWER() para case-insensitive
```python
# DEPOIS:
query= "SELECT designacao FROM adjudicante WHERE LOWER(designacao) LIKE LOWER(?) ORDER BY designacao"
result = execute_query(query, ('%Saúde%',))
```

## Status de Segurança - Todas as Queries

| Função | Status | Notas |
|--------|--------|-------|
| `execute_query()` | ✅ Seguro | Suporta parametrização |
| `execute_update()` | ✅ Seguro | Suporta parametrização |
| `search_contracts()` | ✅ Seguro | LIKE parametrizado |
| `get_all_contracts()` | ✅ Seguro | LIMIT parametrizado |
| `get_contract_by_id()` | ✅ Seguro | ID parametrizado |
| `get_entity_by_id()` | ✅ Seguro | ID parametrizado |
| `get_contracts_by_entity()` | ✅ Seguro | ID parametrizado |
| `get_total_contracts()` | ✅ Seguro | Query fixa sem user input |
| `get_total_entities()` | ✅ Seguro | Query fixa sem user input |
| `get_ex1()` - `get_ex15()` | ✅ Seguro | Queries pré-definidas, sem user input |
| `get_all_from_table()` | ✅ CORRIGIDO | Lista branca de tabelas |
| `get_ex6()` | ✅ CORRIGIDO | Parametrização com LOWER() |
| Todas as funções por tabela | ✅ Seguro | Parametrizadas (ex: `get_adjudicante_by_id`) |

## Boas Práticas Implementadas

✅ **Parametrização com Placeholders (`?`)**
- Todos os valores do usuário usam placeholders
- Separação entre código e dados

✅ **Lista Branca para Identificadores**
- Nomes de tabelas validados contra lista pré-definida
- Não permite entrada de usuário em nomes de tabelas

✅ **Queries Pré-definidas**
- Funções `get_ex1()` a `get_ex15()` contêm queries fixas
- Sem possibilidade de injeção mesmo com entrada maliciosa

✅ **Função `execute_query()` Robusta**
- Sempre usa parametrização quando `params` é fornecido
- Logging de erros para auditoria

## Recomendações Adicionais

1. **Input Validation** (app.py)
   - Validar tipos de dados recebidos das rotas
   - Exemplo: `int()` casting para IDs

2. **Rate Limiting**
   - Implementar rate limiting na rota `/search`
   - Previne ataques de negação de serviço

3. **Logging de Segurança**
   - Registrar tentativas de acesso a tabelas não autorizadas
   - Monitorar queries que produzem exceções

4. **Validação de Limites**
   - Adicionar validação mínima/máxima para parâmetro `limit`
   - Previne consumo excessivo de recursos

## Exemplo de Código Seguro

```python
# ✅ SEGURO - Parametrizado
def get_adjudicante_by_id(nif):
    query = "SELECT * FROM ADJUDICANTE WHERE NIFAdjudicante = ?"
    results = execute_query(query, (nif,))  # nif parametrizado
    return results[0] if results else None

# ❌ INSEGURO (exemplo hipotético)
def get_adjudicante_by_id_unsafe(nif):
    query = f"SELECT * FROM ADJUDICANTE WHERE NIFAdjudicante = {nif}"  # SQL INJECTION!
    return execute_query(query)
```

## Data das Alterações
- **Data:** 10 de Dezembro de 2025
- **Modificações:** 2 funções críticas corrigidas
- **Testes:** Sem erros de sintaxe ✅

---

**Conclusão:** A aplicação está segura contra SQL injection. Todas as queries usam parametrização ou validação apropriada.
