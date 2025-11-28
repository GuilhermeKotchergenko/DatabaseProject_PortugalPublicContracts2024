"""
Servidor Flask para Contratos Públicos Portugal 2024.
Ponto de entrada da aplicação.
"""

import logging
from app import app

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

if __name__ == '__main__':
    logging.info('Iniciando servidor...')
    app.run(host='0.0.0.0', port=9001, debug=False)
