"""
Módulo de conexão e operações com a base de dados.
Contratos Públicos Portugal 2024
"""

import sqlite3
import logging
import os

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Caminho absoluto para a base de dados
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, 'contratos_publicos.db')


def get_connection():
    """Estabelece conexão com a base de dados SQLite."""
    try:
        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row
        logging.info(f'Conectado à base de dados {DATABASE}')
        return conn
    except sqlite3.Error as e:
        logging.error(f'Erro ao conectar à base de dados: {e}')
        raise


def init_db():
    """Garante que a base de dados existe.

    As tabelas são assumidas como já criadas externamente (script SQL).
    """
    conn = get_connection()
    close_connection(conn)
    logging.info('Base de dados disponível')


def close_connection(conn):
    """Fecha a conexão com a base de dados."""
    if conn:
        conn.close()
        logging.info('Conexão fechada')


def execute_query(query, params=None):
    """Executa uma query SELECT e retorna os resultados."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        results = cursor.fetchall()
        return results
    except sqlite3.Error as e:
        logging.error(f'Erro ao executar query: {e}')
        raise
    finally:
        close_connection(conn)


def execute_update(query, params=None):
    """Executa uma query INSERT, UPDATE ou DELETE."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        conn.commit()
        return cursor.rowcount
    except sqlite3.Error as e:
        logging.error(f'Erro ao executar update: {e}')
        conn.rollback()
        raise
    finally:
        close_connection(conn)


# Funções específicas para Contratos
def get_all_contracts(limit=100):
    """Retorna todos os contratos (com limite)."""
    query = "SELECT * FROM CONTRATOS LIMIT ?"
    return execute_query(query, (limit,))


def get_contract_by_id(contract_id):
    """Retorna um contrato pelo ID."""
    query = "SELECT * FROM CONTRATOS WHERE IdContrato = ?"
    results = execute_query(query, (contract_id,))
    return results[0] if results else None


def search_contracts(search_term):
    """Pesquisa contratos por objetivo do contrato ou tipo de procedimento."""
    query = """
        SELECT * FROM CONTRATOS 
        WHERE ObjetivoContrato LIKE ? OR TipoProcedimento LIKE ?
    """
    term = f'%{search_term}%'
    return execute_query(query, (term, term))


# Funções específicas para Entidades
def get_all_entities(limit=100):
    """Retorna todas as entidades adjudicantes (com limite)."""
    query = "SELECT * FROM ADJUDICANTE LIMIT ?"
    return execute_query(query, (limit,))


def get_entity_by_id(entity_id):
    """Retorna uma entidade pelo NIF do adjudicante."""
    query = "SELECT * FROM ADJUDICANTE WHERE NIFAdjudicante = ?"
    results = execute_query(query, (entity_id,))
    return results[0] if results else None


def get_contracts_by_entity(entity_id):
    """Retorna contratos associados a um adjudicante (NIFAdjudicante)."""
    query = "SELECT * FROM CONTRATOS WHERE NIFAdjudicante = ?"
    return execute_query(query, (entity_id,))


# Funções de estatísticas
def get_total_contracts():
    """Retorna o número total de contratos."""
    try:
        query = "SELECT COUNT(*) as total FROM CONTRATOS"
        result = execute_query(query)
        return result[0]['total'] if result else 0
    except Exception:
        return 0


def get_total_entities():
    """Retorna o número total de entidades adjudicantes."""
    try:
        query = "SELECT COUNT(*) as total FROM ADJUDICANTE"
        result = execute_query(query)
        return result[0]['total'] if result else 0
    except Exception:
        return 0

def get_ex1():
    try:
        query= "select IdContrato, Preco, ObjetivoContrato from contratos where TipoProcedimento = 'Consulta Prévia';"
        result = execute_query(query)     
        return result  # Retornar todos os resultados, não result[0]['1º exercicio']
    except Exception:
        return []

def get_ex2():
    try:
        query= "SELECT IdContrato, NIFAdjudicante, ObjetivoContrato FROM contratos WHERE Fundamentacao IS NULL OR Fundamentacao = '';"
        result = execute_query(query)     
        return result
    except Exception:
        return []

def get_ex3():
    try:
        query= "select idContrato, TipoProcedimento from contratos natural join localizacaocontratos where idDistrito=3;"
        result = execute_query(query)     
        return result
    except Exception:
        return []

def get_ex4():
    try:
        query= "select a.designacao, count(c.IdContrato) as quantidade from contratos c inner join adjudicante a on a.NIFAdjudicante = c.NIFAdjudicante group by c.NIFAdjudicante order by quantidade DESC;"
        result = execute_query(query)     
        return result
    except Exception:
        return []

def get_ex5():
    try:
        query= "select m.NomeMunicipio, COUNT(c.IdContrato) as ContratosLongaDuracao from municipio m inner join localizacaocontratos l on m.IdMunicipio = l.IdMunicipio inner join contratos c on l.IdContrato = c.IdContrato where c.PrazoExecucao > 365 group by m.NomeMunicipio having COUNT(c.IdContrato) >= 5 order by ContratosLongaDuracao DESC;"
        result = execute_query(query)     
        return result
    except Exception:
        return []

def get_ex6():
    try:
        query= "select designacao from adjudicante where designacao like '%Saúde%' or Designacao like '%saúde%' order by designacao;"
        result = execute_query(query)     
        return result
    except Exception:
        return []
    
def get_ex7():
    try:
        query= "select d.NomeDistrito, count(IdContrato) as quantidade from localizacaocontratos l natural join distrito d group by l.idDistrito order by quantidade DESC;"
        result = execute_query(query)     
        return result
    except Exception:
        return []
    
def get_ex8():
    try:
        query= "select IdContrato, Preco from contratos order by Preco DESC limit 10;"
        result = execute_query(query)     
        return result
    except Exception:
        return []

def get_ex9():
    try:
        query= "select c.Designacao,avg(t.Preco) as PrecoMedio from CPV c inner join CONTRATOSCPV cc on c.CodCpv = cc.CodCpv inner join CONTRATOS t ON cc.IdContrato = t.IdContrato GROUP BY c.Designacao ORDER BY PrecoMedio DESC;"
        result = execute_query(query)     
        return result
    except Exception:
        return []

def get_ex10():
    try:
        query= "select NomeDistrito, sum(Preco) as Preço_Total from contratos natural join localizacaocontratos natural join distrito group by idDistrito order by Preço_Total DESC;"
        result = execute_query(query)     
        return result
    except Exception:
        return []

def get_ex11():
    try:
        query= "select TipoProcedimento, count(IdContrato) as qtd from contratos group by TipoProcedimento order by qtd DESC"
        result = execute_query(query)     
        return result
    except Exception:
        return []

def get_ex12():
    try:
        query= "select d.NomeDistrito, sum(c.Preco) as ValorTotal from contratos c inner join localizacaocontratos l on c.IdContrato = l.IdContrato inner join distrito d on l.IdDistrito = d.IdDistrito where substr(c.DataCelebracaoContrato, 7, 4) = '2024' group by d.NomeDistrito order by ValorTotal DESC;"
        result = execute_query(query)     
        return result
    except Exception:
        return []

def get_ex13():
    try:
        query= "SELECT c.IdContrato, m.NomeMunicipio, c.Preco FROM Contratos c JOIN LocalizacaoContratos l ON c.IdContrato = l.IdContrato JOIN (SELECT l2.IdMunicipio, AVG(c2.Preco) AS PrecoMedio FROM LocalizacaoContratos l2 JOIN Contratos c2 ON c2.IdContrato = l2.IdContrato GROUP BY l2.IdMunicipio) pm ON pm.IdMunicipio = l.IdMunicipio JOIN Municipio m ON m.IdMunicipio = l.IdMunicipio WHERE c.Preco > pm.PrecoMedio ORDER BY m.NomeMunicipio, c.Preco DESC; "
        result = execute_query(query)     
        return result
    except Exception:
        return []

def get_ex14():
    try:
        query= "select ca.chaveadjudicatario, a.designacao from contratosadjudicatario ca inner join adjudicatario a on a.chaveadjudicatario = ca.chaveadjudicatario inner join localizacaocontratos l on l.idcontrato = ca.idcontrato inner join distrito d on d.iddistrito = l.iddistrito group by ca.chaveadjudicatario, a.designacao having count(distinct d.IdDistrito) > 5; "
        result = execute_query(query)     
        return result
    except Exception:
        return []

def get_ex15():
    try:
        query= "select d.nomedistrito, count(distinct c.idcontrato) as totalcontratos, count(distinct c.nifadjudicante) as totaladjudicantes, count(distinct ca.chaveadjudicatario) as totaladjudicatarios from distrito d inner join localizacaocontratos l on l.iddistrito = d.iddistrito inner join contratos c on c.idcontrato = l.idcontrato left join contratosadjudicatario ca on ca.idcontrato = c.idcontrato group by d.nomedistrito order by totalcontratos desc; "
        result = execute_query(query)     
        return result
    except Exception:
        return []


# Inicializar a base de dados ao importar o módulo
init_db()
