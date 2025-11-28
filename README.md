# Contratos Públicos Portugal 2024

Aplicação Python demonstrando o acesso à base de dados de Contratos Públicos Portugueses de 2024.

## Sumário

**Autoria:** Projeto de Base de Dados - FCUP

Aplicação Python/Flask para consulta e pesquisa de contratos públicos portugueses.

## Referências

- [sqlite3](https://docs.python.org/3/library/sqlite3.html)
- [Flask](https://flask.palletsprojects.com/)
- [Jinja templates](https://jinja.palletsprojects.com/)

## Estrutura do Projeto

```
DatabaseProject_PortugalPublicContracts2024/
├── data/
│   └── raw/
│       └── ContratosPublicos2024.tsv
├── static/
│   └── style.css
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── contract-list.html
│   ├── contract.html
│   ├── contract-search.html
│   ├── entity-list.html
│   └── entity.html
├── app.py
├── db.py
├── server.py
├── test_db_connection.py
├── .gitignore
├── LICENSE.txt
└── README.md
```

## Instalação de Dependências

### Python 3 e pip

Deve ter o Python 3 e o gestor de pacotes pip instalado:

```bash
sudo apt-get install python3 python3-pip
```

### Ambiente Virtual

Criar
```bash
python3 -m venv venv
```

Ativar (Linux/macOS)
```bash
source venv/bin/activate
```

Ativar (PowerShell)
```bash
venv\Scripts\Activate
```

### Bibliotecas Python

```bash
pip install --user Flask
```

## Execução

Inicie a aplicação executando `python3 server.py` e interaja com a mesma abrindo uma janela no seu browser com o endereço [http://localhost:9001/](http://localhost:9001/)

```bash
$ python3 server.py
2024-XX-XX XX:XX:XX - INFO - Iniciando servidor...
 * Serving Flask app "app" (lazy loading)
 * Running on http://0.0.0.0:9001/ (Press CTRL+C to quit)
```

## Funcionalidades

- **Página Inicial:** Estatísticas gerais dos contratos
- **Lista de Contratos:** Visualização de todos os contratos
- **Detalhes do Contrato:** Informações completas de cada contrato
- **Pesquisa:** Busca por objeto ou entidade
- **Lista de Entidades:** Visualização das entidades adjudicantes/adjudicatárias
- **Detalhes da Entidade:** Informações e contratos associados

## Dados

Os dados originais dos contratos públicos encontram-se na pasta `data/raw/`.
