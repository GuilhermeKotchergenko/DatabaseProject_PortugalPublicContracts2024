"""
Aplicação Flask para Contratos Públicos Portugal 2024.
Define as rotas e handlers da aplicação web.
"""

from flask import Flask, render_template, request, abort
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
    # Validar ID
    contract = db.get_contract_by_id(id)
    if contract:
        return render_template('contract.html', contract=contract)
    return "Contrato não encontrado", 404


@app.route('/search')
def contract_search():
    """Pesquisa de contratos com proteção contra DoS.
    
    Rate limit: 10 requests por minuto
    """
    # Validar query string
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
    # Validar ID
    entity = db.get_entity_by_id(id)
    if entity:
        contracts = db.get_contracts_by_entity(id)
        return render_template('entity.html', 
                             entity=entity, 
                             contracts=contracts)
    return "Entidade não encontrada", 404


# Routes for ADJUDICANTE table
@app.route('/ADJUDICANTE/')
def adjudicante_list():
    """Lista todos os adjudicantes."""
    adjudicantes = db.get_all_adjudicantes()
    return render_template('table-list.html', 
                         records=adjudicantes, 
                         table_name='ADJUDICANTE',
                         pk_field='NIFAdjudicante',
                         display_fields=['NIFAdjudicante', 'designacao'])


@app.route('/ADJUDICANTE/<int:k>/')
def adjudicante_detail(k):
    """Detalhes de um adjudicante específico."""
    adjudicante = db.get_adjudicante_by_id(k)
    if adjudicante:
        return render_template('table-detail.html', 
                             record=adjudicante,
                             table_name='ADJUDICANTE')
    return "Adjudicante não encontrado", 404


# Routes for ADJUDICATARIO table
@app.route('/ADJUDICATARIO/')
def adjudicatario_list():
    """Lista todos os adjudicatários."""
    adjudicatarios = db.get_all_adjudicatarios()
    return render_template('table-list.html', 
                         records=adjudicatarios, 
                         table_name='ADJUDICATARIO',
                         pk_field='ChaveAdjudicatario',
                         display_fields=['ChaveAdjudicatario', 'NIFAdjudicatario', 'designacao'])


@app.route('/ADJUDICATARIO/<int:k>/')
def adjudicatario_detail(k):
    """Detalhes de um adjudicatário específico."""
    adjudicatario = db.get_adjudicatario_by_id(k)
    if adjudicatario:
        return render_template('table-detail.html', 
                             record=adjudicatario,
                             table_name='ADJUDICATARIO')
    return "Adjudicatário não encontrado", 404


# Routes for CONTRATOS table
@app.route('/CONTRATOS/')
def contratos_list():
    """Lista todos os contratos."""
    contratos = db.get_all_contracts()
    return render_template('table-list.html', 
                         records=contratos, 
                         table_name='CONTRATOS',
                         pk_field='IdContrato',
                         display_fields=['IdContrato', 'TipoProcedimento', 'ObjetivoContrato', 'DataPublicacao', 'preco'])


@app.route('/CONTRATOS/<int:k>/')
def contratos_detail(k):
    """Detalhes de um contrato específico."""
    contrato = db.get_contract_by_id(k)
    if contrato:
        return render_template('table-detail.html', 
                             record=contrato,
                             table_name='CONTRATOS')
    return "Contrato não encontrado", 404


# Routes for PAIS table
@app.route('/PAIS/')
def pais_list():
    """Lista todos os países."""
    paises = db.get_all_paises()
    return render_template('table-list.html', 
                         records=paises, 
                         table_name='PAIS',
                         pk_field='IdPais',
                         display_fields=['IdPais', 'Designacao'])


@app.route('/PAIS/<int:k>/')
def pais_detail(k):
    """Detalhes de um país específico."""
    pais = db.get_pais_by_id(k)
    if pais:
        return render_template('table-detail.html', 
                             record=pais,
                             table_name='PAIS')
    return "País não encontrado", 404


# Routes for DISTRITO table
@app.route('/DISTRITO/')
def distrito_list():
    """Lista todos os distritos."""
    distritos = db.get_all_distritos()
    return render_template('table-list.html', 
                         records=distritos, 
                         table_name='DISTRITO',
                         pk_field='IdDistrito',
                         display_fields=['IdDistrito', 'NomeDistrito'])


@app.route('/DISTRITO/<int:k>/')
def distrito_detail(k):
    """Detalhes de um distrito específico."""
    distrito = db.get_distrito_by_id(k)
    if distrito:
        return render_template('table-detail.html', 
                             record=distrito,
                             table_name='DISTRITO')
    return "Distrito não encontrado", 404


# Routes for MUNICIPIO table
@app.route('/MUNICIPIO/')
def municipio_list():
    """Lista todos os municípios."""
    municipios = db.get_all_municipios()
    return render_template('table-list.html', 
                         records=municipios, 
                         table_name='MUNICIPIO',
                         pk_field='IdMunicipio',
                         display_fields=['IdMunicipio', 'NomeMunicipio'])


@app.route('/MUNICIPIO/<int:k>/')
def municipio_detail(k):
    """Detalhes de um município específico."""
    municipio = db.get_municipio_by_id(k)
    if municipio:
        return render_template('table-detail.html', 
                             record=municipio,
                             table_name='MUNICIPIO')
    return "Município não encontrado", 404


# Routes for CPV table
@app.route('/CPV/')
def cpv_list():
    """Lista todos os CPVs."""
    cpvs = db.get_all_cpvs()
    return render_template('table-list.html', 
                         records=cpvs, 
                         table_name='CPV',
                         pk_field='CodCpv',
                         display_fields=['CodCpv', 'designacao'])


@app.route('/CPV/<string:k>/')
def cpv_detail(k):
    """Detalhes de um CPV específico."""
    cpv = db.get_cpv_by_id(k)
    if cpv:
        return render_template('table-detail.html', 
                             record=cpv,
                             table_name='CPV')
    return "CPV não encontrado", 404


# Routes for TIPOS table
@app.route('/TIPOS/')
def tipos_list():
    """Lista todos os tipos."""
    tipos = db.get_all_tipos()
    return render_template('table-list.html', 
                         records=tipos, 
                         table_name='TIPOS',
                         pk_field='ChaveTipo',
                         display_fields=['ChaveTipo', 'Tipo'])


@app.route('/TIPOS/<int:k>/')
def tipos_detail(k):
    """Detalhes de um tipo específico."""
    tipo = db.get_tipo_by_id(k)
    if tipo:
        return render_template('table-detail.html', 
                             record=tipo,
                             table_name='TIPOS')
    return "Tipo não encontrado", 404


# Routes for LOCALIZACAOCONTRATOS table
@app.route('/LOCALIZACAOCONTRATOS/')
def localizacao_list():
    """Lista todas as localizações de contratos."""
    localizacoes = db.get_all_localizacoes()
    return render_template('table-list.html', 
                         records=localizacoes, 
                         table_name='LOCALIZACAOCONTRATOS',
                         pk_field='ChaveLocalizacao',
                         display_fields=['ChaveLocalizacao', 'IdContrato', 'IdPais', 'IdDistrito', 'IdMunicipio'])


@app.route('/LOCALIZACAOCONTRATOS/<int:k>/')
def localizacao_detail(k):
    """Detalhes de uma localização específica."""
    localizacao = db.get_localizacao_by_id(k)
    if localizacao:
        return render_template('table-detail.html', 
                             record=localizacao,
                             table_name='LOCALIZACAOCONTRATOS')
    return "Localização não encontrada", 404


# Routes for CONTRATOSADJUDICATARIO table
@app.route('/CONTRATOSADJUDICATARIO/')
def contratos_adjudicatario_list():
    """Lista todos os contratos-adjudicatário."""
    contratos_adj = db.get_all_contratos_adjudicatario()
    return render_template('table-list.html', 
                         records=contratos_adj, 
                         table_name='CONTRATOSADJUDICATARIO',
                         pk_field='composite',
                         display_fields=['IdContrato', 'ChaveAdjudicatario'])


@app.route('/CONTRATOSADJUDICATARIO/<int:id_contrato>/<int:chave_adjudicatario>/')
def contratos_adjudicatario_detail(id_contrato, chave_adjudicatario):
    """Detalhes de um contrato-adjudicatário específico."""
    contrato_adj = db.get_contrato_adjudicatario_by_id(id_contrato, chave_adjudicatario)
    if contrato_adj:
        return render_template('table-detail.html', 
                             record=contrato_adj,
                             table_name='CONTRATOSADJUDICATARIO')
    return "Relação Contrato-Adjudicatário não encontrada", 404


# Routes for TIPODOCONTRATO table
@app.route('/TIPODOCONTRATO/')
def tipo_contrato_list():
    """Lista todos os tipo-contrato."""
    tipos_contrato = db.get_all_tipo_contrato()
    return render_template('table-list.html', 
                         records=tipos_contrato, 
                         table_name='TIPODOCONTRATO',
                         pk_field='composite',
                         display_fields=['IdContrato', 'ChaveTipo'])


@app.route('/TIPODOCONTRATO/<int:id_contrato>/<int:chave_tipo>/')
def tipo_contrato_detail(id_contrato, chave_tipo):
    """Detalhes de um tipo-contrato específico."""
    tipo_contrato = db.get_tipo_contrato_by_id(id_contrato, chave_tipo)
    if tipo_contrato:
        return render_template('table-detail.html', 
                             record=tipo_contrato,
                             table_name='TIPODOCONTRATO')
    return "Relação Tipo-Contrato não encontrada", 404


# Routes for CONTRATOSCPV table
@app.route('/CONTRATOSCPV/')
def contratos_cpv_list():
    """Lista todos os contratos-CPV."""
    contratos_cpv = db.get_all_contratos_cpv()
    return render_template('table-list.html', 
                         records=contratos_cpv, 
                         table_name='CONTRATOSCPV',
                         pk_field='composite',
                         display_fields=['IdContrato', 'CodCpv'])


@app.route('/CONTRATOSCPV/<int:id_contrato>/<string:cod_cpv>/')
def contratos_cpv_detail(id_contrato, cod_cpv):
    """Detalhes de um contrato-CPV específico."""
    contrato_cpv = db.get_contrato_cpv_by_id(id_contrato, cod_cpv)
    if contrato_cpv:
        return render_template('table-detail.html', 
                             record=contrato_cpv,
                             table_name='CONTRATOSCPV')
    return "Relação Contrato-CPV não encontrada", 404


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