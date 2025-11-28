"""
Aplicação Flask para Contratos Públicos Portugal 2024.
Define as rotas e handlers da aplicação web.
"""

from flask import Flask, render_template, request
import db

app = Flask(__name__)


@app.route('/')
def index():
    """Página inicial com estatísticas."""
    total_contracts = db.get_total_contracts()
    total_entities = db.get_total_entities()
    return render_template('index.html', 
                         total_contracts=total_contracts,
                         total_entities=total_entities)


@app.route('/contracts')
def contract_list():
    """Lista de contratos."""
    contracts = db.get_all_contracts()
    return render_template('contract-list.html', contracts=contracts)


@app.route('/contract/<int:id>')
def contract(id):
    """Detalhes de um contrato específico."""
    contract = db.get_contract_by_id(id)
    if contract:
        return render_template('contract.html', contract=contract)
    return "Contrato não encontrado", 404


@app.route('/search')
def contract_search():
    """Pesquisa de contratos."""
    query = request.args.get('q', '')
    contracts = []
    if query:
        contracts = db.search_contracts(query)
    return render_template('contract-search.html', 
                         contracts=contracts, 
                         query=query)


@app.route('/entities')
def entity_list():
    """Lista de entidades."""
    entities = db.get_all_entities()
    return render_template('entity-list.html', entities=entities)


@app.route('/entity/<int:id>')
def entity(id):
    """Detalhes de uma entidade específica."""
    entity = db.get_entity_by_id(id)
    if entity:
        contracts = db.get_contracts_by_entity(id)
        return render_template('entity.html', 
                             entity=entity, 
                             contracts=contracts)
    return "Entidade não encontrada", 404
