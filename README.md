# 📊 Contratos Públicos Portugal 2024 - Projeto Base de Dados

Aplicação Python/Flask para modelação, armazenamento e consulta de dados de Contratos Públicos Portugueses de 2024.

## 📋 Índice

1. [Visão Geral](#visão-geral)
2. [Objetivos do Projeto](#objetivos-do-projeto)
3. [Estrutura da Base de Dados](#estrutura-da-base-de-dados)
4. [Funcionalidades](#funcionalidades)
5. [Instalação](#instalação)
6. [Uso da Aplicação](#uso-da-aplicação)
7. [Segurança](#segurança)
8. [Estrutura do Projeto](#estrutura-do-projeto)
9. [Referências](#referências)

---

## 🎯 Visão Geral

Este projeto implementa uma **aplicação de base de dados completa** para gerenciar e consultar dados de Contratos Públicos Portugueses de 2024.

**O que é este projeto?**

Uma aplicação educacional que demonstra:
- ✅ Modelação de dados (ER e Relacional)
- ✅ Implementação de base de dados SQLite
- ✅ Aplicação web Flask com endpoints REST-like
- ✅ Segurança contra SQL Injection
- ✅ Consultas dinâmicas parametrizadas
- ✅ Interface web para consultas interativas

**Autores:** Felipe Reis, Guilherme Batista, Telma Freitas

---

## 🎓 Objetivos do Projeto

### 1. Modelação de Dados

O projeto demonstra o processo completo de modelação:

**Modelo Entidade-Relacionamento (ER):**
- Identificação do universo de dados (contratos públicos portugueses)
- Definição de entidades-tipo (CONTRATOS, ADJUDICANTE, ADJUDICATARIO, etc.)
- Estabelecimento de relacionamentos entre entidades
- Representação visual através de diagrama ER

**Modelo Relacional:**
- Mapeamento correto do modelo ER para tabelas
- Normalização para 3ª Forma Normal (3NF)
- Definição de chaves primárias e externas
- Integridade referencial

### 2. Implementação de Base de Dados

**Estrutura de Dados:**
- 12 tabelas principais relacionadas
- Suporte a múltiplas chaves primárias (simples e compostas)
- Relacionamentos 1:N e N:M
- Tipos de dados apropriados para cada campo

**Dados:**
- Importação de dados de arquivo TSV (ContratosPublicos2024.tsv)
- Povoamento automático de tabelas
- Validação de integridade

### 3. Aplicação Web Interativa

**Endpoints Implementados:**
- `/` - Página inicial com estatísticas
- `/TABELA/` - Lista todos os registos de uma tabela
- `/TABELA/k/` - Detalhes de um registo específico
- `/search` - Pesquisa avançada
- Endpoints para 15 interrogações SQL específicas

**Características:**
- Interface web responsiva
- Navegação entre entidades relacionadas
- Pesquisa dinâmica
- Exportação de dados

### 4. Segurança de Base de Dados

**Proteção contra SQL Injection:**
- Parametrização de todas as queries
- Lista branca para nomes de tabelas
- Validação de entrada
- Tratamento de erros apropriado

---

## 📊 Estrutura da Base de Dados

### Tabelas Principais

| Tabela | Descrição | Registos |
|--------|-----------|----------|
| **CONTRATOS** | Contratos públicos principais | ~32,000 |
| **ADJUDICANTE** | Organizações que celebram contratos | ~6,500 |
| **ADJUDICATARIO** | Empresas/entidades adjudicadas | ~8,500 |
| **LOCALIZACAOCONTRATOS** | Localização geográfica dos contratos | ~32,000 |
| **DISTRITO** | Distritos de Portugal | 28 |
| **MUNICIPIO** | Municípios de Portugal | 308 |
| **PAIS** | Países | ~190 |
| **CPV** | Classificação de Vocabulário Comum (tipos de produto/serviço) | ~9,500 |
| **TIPOS** | Tipos de contrato | ~50 |
| **TIPODOCONTRATO** | Relacionamento entre contratos e tipos | ~32,000 |
| **CONTRATOSCPV** | Relacionamento entre contratos e CPV | ~60,000 |
| **CONTRATOSADJUDICATARIO** | Relacionamento entre contratos e adjudicatários | ~35,000 |

### Modelo Relacional

**Relacionamentos Principais:**
- CONTRATOS (1) ←→ (N) ADJUDICANTE
- CONTRATOS (1) ←→ (N) ADJUDICATARIO (através de CONTRATOSADJUDICATARIO)
- CONTRATOS (1) ←→ (N) LOCALIZACAOCONTRATOS
- LOCALIZACAOCONTRATOS (N) ←→ (1) DISTRITO
- LOCALIZACAOCONTRATOS (N) ←→ (1) MUNICIPIO
- CONTRATOS (1) ←→ (N) TIPODOCONTRATO ←→ (N) TIPOS
- CONTRATOS (1) ←→ (N) CONTRATOSCPV ←→ (N) CPV

---

## ✨ Funcionalidades

### Endpoints Principais

#### 1. Página Inicial
```
GET /
```
Exibe estatísticas globais:
- Total de contratos
- Total de entidades adjudicantes
- Links para navegar por tabelas

#### 2. Listagem de Tabelas
```
GET /TABELA/              # Substitua TABELA por: CONTRATOS, ADJUDICANTE, etc.
```
Retorna lista paginada de todos os registos com:
- Links para detalhes individuais
- Filtros básicos
- Navegação entre páginas

**Tabelas Disponíveis:**
- `/ADJUDICANTE/` - Adjudicantes
- `/ADJUDICATARIO/` - Adjudicatários
- `/CONTRATOS/` - Contratos
- `/PAIS/` - Países
- `/DISTRITO/` - Distritos
- `/MUNICIPIO/` - Municípios
- `/CPV/` - Classificações CPV
- `/TIPOS/` - Tipos de Contrato
- `/LOCALIZACAOCONTRATOS/` - Localizações
- `/CONTRATOSADJUDICATARIO/` - Relacionamentos
- `/TIPODOCONTRATO/` - Relacionamentos
- `/CONTRATOSCPV/` - Relacionamentos

#### 3. Detalhes de Registo
```
GET /TABELA/k/            # k é a chave primária
```
Exibe todos os detalhes de um registo:
- Todos os campos
- Links para registos relacionados
- Histórico de relações

#### 4. Pesquisa Avançada
```
GET /search?q=termo
```
Busca por:
- ID de contrato
- Objetivo do contrato
- Tipo de procedimento

Com proteção contra SQL Injection via parametrização.

#### 5. Interrogações Específicas
```
GET /sql_question?q=1-15
```

**15 Interrogações SQL Predefinidas:**

1. Contratos celebrados sob "Consulta Prévia"
2. Contratos sem fundamentação registada
3. Contratos do Distrito do Porto
4. Adjudicantes com mais contratos
5. Municípios com 5+ contratos de longa duração
6. Adjudicantes com "Saúde" no nome
7. Total de contratos por distrito
8. Top 10 contratos mais caros
9. Preço médio por CPV
10. Preço total de contratos por distrito
11. Contagem de tipos de procedimento
12. Valor total contratado 2024 por distrito
13. Contratos acima do preço médio municipal
14. Adjudicatários em 5+ distritos
15. Resumo completo de contratos por distrito

---

## 🛠️ Instalação

### Pré-requisitos

- **Python 3.7+**
- **pip** (gestor de pacotes Python)
- **SQLite3** (incluído no Python)

### Passo 1: Clonar Repositório

```bash
git clone https://github.com/GuilhermeKotchergenko/DatabaseProject_PortugalPublicContracts2024.git
cd DatabaseProject_PortugalPublicContracts2024
```

### Passo 2: Criar Ambiente Virtual

```bash
# Linux/Mac
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### Passo 3: Instalar Dependências

```bash
# Instalar Flask
pip install Flask
```

## 🚀 Uso da Aplicação

### Iniciar Servidor

```bash
python3 server.py
```

**Saída:**
```
2025-12-10 12:00:00,000 - INFO - Iniciando servidor...
 * Running on http://0.0.0.0:9001
```

### Aceder à Aplicação

Abra o navegador e visite: **http://localhost:9001**

### Exemplos de Utilização

#### 1. Ver Todos os Adjudicantes
```
http://localhost:9001/ADJUDICANTE/
```

#### 2. Ver Detalhes de um Adjudicante
```
http://localhost:9001/ADJUDICANTE/600043172/
```

#### 3. Pesquisar Contratos
```
http://localhost:9001/search?q=saúde
```

#### 4. Executar Interrogação SQL
```
http://localhost:9001/sql_question?q=1
```
(Listar contratos de "Consulta Prévia")

#### 5. Ver Todos os Contratos
```
http://localhost:9001/CONTRATOS/
```

---

## 🔒 Segurança

### Proteção contra SQL Injection

A aplicação implementa **múltiplas camadas de proteção** contra SQL Injection:

#### 1. Parametrização de Queries
```python
# ✅ SEGURO - Parametrizado
query = "SELECT * FROM CONTRATOS WHERE IdContrato = ?"
results = execute_query(query, (contract_id,))

# ❌ NUNCA fazer isso:
query = f"SELECT * FROM CONTRATOS WHERE IdContrato = {contract_id}"
```

#### 2. Lista Branca para Nomes de Tabelas
```python
ALLOWED_TABLES = {
    'CONTRATOS', 'ADJUDICANTE', 'ADJUDICATARIO', 
    'PAIS', 'DISTRITO', 'MUNICIPIO', ...
}

if table_name.upper() not in ALLOWED_TABLES:
    raise ValueError(f"Tabela não autorizada: {table_name}")
```

#### 3. Validação de Entrada
- Validação de tipos de dados
- Limitação de tamanho de queries
- Tratamento de exceções apropriado

---

## 📁 Estrutura do Projeto

```
DatabaseProject_PortugalPublicContracts2024/
├── 📄 README.md                                    # Este arquivo
├── 📄 SECURITY_FIXES.md                            # Documentação de segurança
├── 📄 LICENSE.txt                                  # Licença do projeto
│
├── 🐍 Python Application
│   ├── server.py                                   # Ponto de entrada (Flask server)
│   ├── app.py                                      # Definição de rotas Flask
│   └── db.py                                       # Camada de acesso a dados
│
├── 🧪 Testing
│   └── test_db_connection.py                      # Teste de conectividade
│
├── 📊 Data
│   ├── raw/
│   │   ├── ContratosPublicos2024.tsv              # Dados brutos (~32,000 registos)
│   │   └── ContratosPublicos2024.txt              # Metadados dos dados
│   └── contratos_publicos.db                      # Base de dados SQLite
│
├── 🎨 Web Interface
│   ├── templates/
│   │   ├── base.html                              # Template base
│   │   ├── index.html                             # Página inicial
│   │   ├── contract-list.html                     # Lista de contratos
│   │   ├── contract.html                          # Detalhe de contrato
│   │   ├── contract-search.html                   # Página de pesquisa
│   │   ├── entity-list.html                       # Lista de entidades
│   │   ├── entity.html                            # Detalhe de entidade
│   │   ├── table-list.html                        # Lista genérica
│   │   ├── table-detail.html                      # Detalhe genérico
│   │   └── sql_question.html                      # Resultados de queries
│   │
│   └── static/
│       └── style.css                              # Estilos CSS
│
├── 📋 Documentation
│   ├── docs/
│   │   ├── relational_model.md                    # Documentação do modelo relacional
│   │   └── schema.sql                             # Script de criação de tabelas
│   │
│   └── workspace.code-workspace                   # Configuração VS Code
│
└── ⚙️ Configuration
    ├── .gitignore                                 # Arquivos a ignorar no Git
```

---

## 📚 Componentes Principais

### `server.py` - Ponto de Entrada
```python
from app import app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9001, debug=False)
```
Inicia o servidor Flask na porta 9001.

### `app.py` - Rotas e Controladores
Define todos os endpoints HTTP:
- Rotas de página inicial
- Rotas de listagem de tabelas
- Rotas de detalhes
- Rotas de pesquisa
- Rotas de interrogações SQL

### `db.py` - Camada de Dados
Implementa:
- Conexão com SQLite
- Funções de query parametrizadas
- Tratamento de erros
- Logging de auditoria

---

## 🔍 Referências

- [SQLite3 Documentation](https://docs.python.org/3/library/sqlite3.html)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Jinja2 Templates](https://jinja.palletsprojects.com/)
- [OWASP SQL Injection Prevention](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html)
- [CERT Secure Coding](https://www.securecoding.cert.org/)

---

## 📄 Licença

Este projeto está licenciado sob a MIT License - ver arquivo [LICENSE.txt](LICENSE.txt) para detalhes.

---

## 👥 Contribuições

Contribuições são bem-vindas! Por favor:
1. Fork o repositório
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

---

**Última Atualização:** 10 de Dezembro de 2025  
**Versão:** 2.0  
**Status:** ✅ Completo e Operacional
