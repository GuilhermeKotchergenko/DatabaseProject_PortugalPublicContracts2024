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
# Mapeamento das perguntas SQL para as funções get_ex*()
SQL_QUESTIONS = {
    1: ("Pergunta 1: Liste o ID do Contrato, o Preço e o Objetivo do Contrato para todos os contratos que foram celebrados sob o procedimento de 'Consulta Prévia'.", db.get_ex1),
    2: ("Pergunta 2: Liste o ID do Contrato, o NIF do Adjudicante e o Objetivo do Contrato para todos os contratos que não possuem fundamentação registrada ", db.get_ex2),
    3: ("Pergunta 3: Liste o Id do Contrato e Tipo de Procedimento dos contratos que são do Distrito do Porto", db.get_ex3),
    4: ("Pergunta 4: Liste os nomes dos adjudicantes e quantos contratos cada um possui. Ordene a partir do que tem o maior número de contratos", db.get_ex4),
    5: ("Pergunta 5: Quais são os municípios com pelo menos 5 contratos cujo Prazo de Execução é superior a 365 dias ? Liste o nome do município e o número de contratos de longa duração.", db.get_ex5),
    6: ("Pergunta 6: Liste a designação de todos os adjudicantes que tem a palavra “Saúde” no nome. Ordene pela designação.", db.get_ex6),
    7: ("Pergunta 7: Qual o total de contratos por distrito? Liste o nome do distrito e a quantidade de contratos, ordenando da maior quantidade para a menor.", db.get_ex7),
    8: ("Pergunta 8: Quais são os 10 contratos mais caros celebrados em 2024? Ordene do maior para o menor, listando o id do contrato e seu respectivo preço.", db.get_ex8),
    9: ("Pergunta 9: Para cada CPV, apresente o preço médio dos contratos. Apresente a designacao do CPV, assim como seu preço médio.Ordene por preço, do maior para o menor.", db.get_ex9),
    10: ("Pergunta 10: Qual o preço total dos contratos por distrito?Ordene a partir do distrito com maior gasto", db.get_ex10),
    11: ("Pergunta 11: Apresente o número de contratos por tipo de procedimento. Ordene do maior para o menor", db.get_ex11),
    12: ("Pergunta 12: Para cada distrito, apresente o valor total contratado em 2024. Apresente o nome do distrito e o valor total ordenando do maior para o menor.", db.get_ex12),
    13: ("Pergunta 13: Liste os contratos cujo preço é superior ao preço médio de todos os contratos do mesmo município. Liste o id do contrato, o nome do municipio assim como seu preço.", db.get_ex13),
    14: ("Pergunta 14: Liste o id e a designação dos adjudicatários que participaram em contratos em mais de 5 distritos diferentes?", db.get_ex14),
    15: ("Pergunta 15: Para cada distrito, mostre o número total de contratos, total de adjudicantes e total de adjudicatários distintos envolvidos. Ordene a partir do distrito com maior número de contratos", db.get_ex15),
}

@app.route('/sql_question')
def sql_question():
    """Executa e exibe resultados de interrogações SQL."""
    q = request.args.get('q', type=int)
    if not q or q not in SQL_QUESTIONS:
        return render_template('sql_question.html', q=None, results=None, error="Pergunta inválida")
    
    titulo, funcao = SQL_QUESTIONS[q]
    results = None
    error = None
    
    try:
        results = funcao()
    except Exception as e:
        error = f"Erro ao executar a pergunta: {str(e)}"
    
    return render_template('sql_question.html', q=q, titulo=titulo, results=results, error=error)

if __name__ == '__main__':
    app.run(debug=True)