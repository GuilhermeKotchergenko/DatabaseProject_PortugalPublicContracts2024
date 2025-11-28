"""
Script para testar a conexão com a base de dados.
"""

import db


def test_connection():
    """Testa a conexão com a base de dados."""
    try:
        conn = db.get_connection()
        print("✓ Conexão estabelecida com sucesso!")
        
        # Testar query simples
        cursor = conn.cursor()
        cursor.execute("SELECT sqlite_version()")
        version = cursor.fetchone()[0]
        print(f"✓ Versão SQLite: {version}")
        
        db.close_connection(conn)
        print("✓ Conexão fechada com sucesso!")
        
        return True
    except Exception as e:
        print(f"✗ Erro: {e}")
        return False


if __name__ == '__main__':
    test_connection()
