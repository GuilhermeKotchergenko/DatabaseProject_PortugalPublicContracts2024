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
    """Inicializa a base de dados com as tabelas necessárias."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Criar tabela de entidades
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS entidades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            nif TEXT,
            tipo TEXT
        )
    ''')
    
    # Criar tabela de contratos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contratos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            objeto TEXT,
            entidade_adjudicante TEXT,
            entidade_adjudicataria TEXT,
            valor REAL,
            data_publicacao TEXT,
            tipo_procedimento TEXT,
            entidade_id INTEGER,
            FOREIGN KEY (entidade_id) REFERENCES entidades(id)
        )
    ''')
    
    conn.commit()
    close_connection(conn)
    logging.info('Base de dados inicializada com sucesso')


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
    query = "SELECT * FROM contratos LIMIT ?"
    return execute_query(query, (limit,))


def get_contract_by_id(contract_id):
    """Retorna um contrato pelo ID."""
    query = "SELECT * FROM contratos WHERE id = ?"
    results = execute_query(query, (contract_id,))
    return results[0] if results else None


def search_contracts(search_term):
    """Pesquisa contratos por objeto ou entidade."""
    query = """
        SELECT * FROM contratos 
        WHERE objeto LIKE ? OR entidade_adjudicante LIKE ?
    """
    term = f'%{search_term}%'
    return execute_query(query, (term, term))


# Funções específicas para Entidades
def get_all_entities(limit=100):
    """Retorna todas as entidades (com limite)."""
    query = "SELECT * FROM entidades LIMIT ?"
    return execute_query(query, (limit,))


def get_entity_by_id(entity_id):
    """Retorna uma entidade pelo ID."""
    query = "SELECT * FROM entidades WHERE id = ?"
    results = execute_query(query, (entity_id,))
    return results[0] if results else None


def get_contracts_by_entity(entity_id):
    """Retorna contratos associados a uma entidade."""
    query = "SELECT * FROM contratos WHERE entidade_id = ?"
    return execute_query(query, (entity_id,))


# Funções de estatísticas
def get_total_contracts():
    """Retorna o número total de contratos."""
    try:
        query = "SELECT COUNT(*) as total FROM contratos"
        result = execute_query(query)
        return result[0]['total'] if result else 0
    except:
        return 0


def get_total_entities():
    """Retorna o número total de entidades."""
    try:
        query = "SELECT COUNT(*) as total FROM entidades"
        result = execute_query(query)
        return result[0]['total'] if result else 0
    except:
        return 0


# Inicializar a base de dados ao importar o módulo
init_db()
