"""
Módulo de conexão e operações com a base de dados.
Contratos Públicos Portugal 2024

Segurança:
- Todas as queries utilizam parametrização com placeholders (?)
- Nomes de tabelas são validados contra lista branca para prevenir SQL injection
- Identificadores não podem ser parametrizados em SQLite, logo usa-se validação
- Valores dos usuários são sempre parametrizados, nunca interpolados
"""

import sqlite3
import logging
import os


# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

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
    """Pesquisa contratos por ID, objetivo do contrato ou tipo de procedimento."""
    query = """
        SELECT * FROM CONTRATOS 
        WHERE IdContrato LIKE ? OR ObjetivoContrato LIKE ? OR TipoProcedimento LIKE ?
    """
    term = f'%{search_term}%'
    return execute_query(query, (term, term, term))


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
        # Parametrizado: usar LOWER() para case-insensitive e parametrizar o termo
        query= "SELECT designacao FROM adjudicante WHERE LOWER(designacao) LIKE LOWER(?) ORDER BY designacao"
        result = execute_query(query, ('%Saúde%',))     
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


# Generic functions for all tables
def get_all_from_table(table_name, limit=100):
    """Retorna todos os registros de uma tabela (com limite).
    
    A função valida o nome da tabela para prevenir SQL injection,
    já que identificadores não podem ser parametrizados em SQLite.
    """
    # Lista branca de tabelas permitidas
    ALLOWED_TABLES = {
        'CONTRATOS', 'ADJUDICANTE', 'ADJUDICATARIO', 'PAIS', 'DISTRITO',
        'MUNICIPIO', 'CPV', 'TIPOS', 'LOCALIZACAOCONTRATOS',
        'CONTRATOSADJUDICATARIO', 'TIPODOCONTRATO', 'CONTRATOSCPV'
    }
    
    # Validar se a tabela está na lista branca
    if table_name.upper() not in ALLOWED_TABLES:
        raise ValueError(f"Tabela não autorizada: {table_name}")
    
    # Usar o nome da tabela validado
    query = f"SELECT * FROM {table_name.upper()} LIMIT ?"
    return execute_query(query, (limit,))


# ADJUDICANTE functions
def get_all_adjudicantes(limit=100):
    """Retorna todos os adjudicantes (com limite)."""
    query = "SELECT * FROM ADJUDICANTE LIMIT ?"
    return execute_query(query, (limit,))


def get_adjudicante_by_id(nif):
    """Retorna um adjudicante pelo NIF."""
    query = "SELECT * FROM ADJUDICANTE WHERE NIFAdjudicante = ?"
    results = execute_query(query, (nif,))
    return results[0] if results else None


# ADJUDICATARIO functions
def get_all_adjudicatarios(limit=100):
    """Retorna todos os adjudicatários (com limite)."""
    query = "SELECT * FROM ADJUDICATARIO LIMIT ?"
    return execute_query(query, (limit,))


def get_adjudicatario_by_id(chave):
    """Retorna um adjudicatário pela chave."""
    query = "SELECT * FROM ADJUDICATARIO WHERE ChaveAdjudicatario = ?"
    results = execute_query(query, (chave,))
    return results[0] if results else None


# PAIS functions
def get_all_paises(limit=100):
    """Retorna todos os países (com limite)."""
    query = "SELECT * FROM PAIS LIMIT ?"
    return execute_query(query, (limit,))


def get_pais_by_id(id_pais):
    """Retorna um país pelo ID."""
    query = "SELECT * FROM PAIS WHERE IdPais = ?"
    results = execute_query(query, (id_pais,))
    return results[0] if results else None


# DISTRITO functions
def get_all_distritos(limit=100):
    """Retorna todos os distritos (com limite)."""
    query = "SELECT * FROM DISTRITO LIMIT ?"
    return execute_query(query, (limit,))


def get_distrito_by_id(id_distrito):
    """Retorna um distrito pelo ID."""
    query = "SELECT * FROM DISTRITO WHERE IdDistrito = ?"
    results = execute_query(query, (id_distrito,))
    return results[0] if results else None


# MUNICIPIO functions
def get_all_municipios(limit=100):
    """Retorna todos os municípios (com limite)."""
    query = "SELECT * FROM MUNICIPIO LIMIT ?"
    return execute_query(query, (limit,))


def get_municipio_by_id(id_municipio):
    """Retorna um município pelo ID."""
    query = "SELECT * FROM MUNICIPIO WHERE IdMunicipio = ?"
    results = execute_query(query, (id_municipio,))
    return results[0] if results else None


# CPV functions
def get_all_cpvs(limit=100):
    """Retorna todos os CPVs (com limite)."""
    query = "SELECT * FROM CPV LIMIT ?"
    return execute_query(query, (limit,))


def get_cpv_by_id(cod_cpv):
    """Retorna um CPV pelo código."""
    query = "SELECT * FROM CPV WHERE CodCpv = ?"
    results = execute_query(query, (cod_cpv,))
    return results[0] if results else None


# TIPOS functions
def get_all_tipos(limit=100):
    """Retorna todos os tipos (com limite)."""
    query = "SELECT * FROM TIPOS LIMIT ?"
    return execute_query(query, (limit,))


def get_tipo_by_id(chave_tipo):
    """Retorna um tipo pela chave."""
    query = "SELECT * FROM TIPOS WHERE ChaveTipo = ?"
    results = execute_query(query, (chave_tipo,))
    return results[0] if results else None


# LOCALIZACAOCONTRATOS functions
def get_all_localizacoes(limit=100):
    """Retorna todas as localizações de contratos (com limite)."""
    query = "SELECT * FROM LOCALIZACAOCONTRATOS LIMIT ?"
    return execute_query(query, (limit,))


def get_localizacao_by_id(chave_localizacao):
    """Retorna uma localização pela chave."""
    query = "SELECT * FROM LOCALIZACAOCONTRATOS WHERE ChaveLocalizacao = ?"
    results = execute_query(query, (chave_localizacao,))
    return results[0] if results else None


# CONTRATOSADJUDICATARIO functions
def get_all_contratos_adjudicatario(limit=100):
    """Retorna todos os contratos-adjudicatário (com limite)."""
    query = "SELECT * FROM CONTRATOSADJUDICATARIO LIMIT ?"
    return execute_query(query, (limit,))


def get_contrato_adjudicatario_by_id(id_contrato, chave_adjudicatario):
    """Retorna um contrato-adjudicatário pelas chaves compostas."""
    query = "SELECT * FROM CONTRATOSADJUDICATARIO WHERE IdContrato = ? AND ChaveAdjudicatario = ?"
    results = execute_query(query, (id_contrato, chave_adjudicatario))
    return results[0] if results else None


# TIPODOCONTRATO functions
def get_all_tipo_contrato(limit=100):
    """Retorna todos os tipo-contrato (com limite)."""
    query = "SELECT * FROM TIPODOCONTRATO LIMIT ?"
    return execute_query(query, (limit,))


def get_tipo_contrato_by_id(id_contrato, chave_tipo):
    """Retorna um tipo-contrato pelas chaves compostas."""
    query = "SELECT * FROM TIPODOCONTRATO WHERE IdContrato = ? AND ChaveTipo = ?"
    results = execute_query(query, (id_contrato, chave_tipo))
    return results[0] if results else None


# CONTRATOSCPV functions
def get_all_contratos_cpv(limit=100):
    """Retorna todos os contratos-CPV (com limite)."""
    query = "SELECT * FROM CONTRATOSCPV LIMIT ?"
    return execute_query(query, (limit,))


def get_contrato_cpv_by_id(id_contrato, cod_cpv):
    """Retorna um contrato-CPV pelas chaves compostas."""
    query = "SELECT * FROM CONTRATOSCPV WHERE IdContrato = ? AND CodCpv = ?"
    results = execute_query(query, (id_contrato, cod_cpv))
    return results[0] if results else None


# Inicializar a base de dados ao importar o módulo
init_db()
