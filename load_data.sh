#!/bin/bash

# Verifica se o ambiente virtual está ativado
if [[ -z "$VIRTUAL_ENV" ]]; then
    echo "Ativando ambiente virtual..."
    if [ -d ".venv" ]; then
        source .venv/bin/activate
    else
        echo "Ambiente virtual não encontrado. Criando..."
        python3 -m venv .venv
        source .venv/bin/activate
    fi
fi

# Instala dependências necessárias
echo "Instalando dependências..."
pip install faker requests

# Cria diretório de scripts se não existir
mkdir -p scripts

# Executa o script de carga
echo "Executando script de carga de dados..."
python scripts/load_data.py

# Desativa o ambiente virtual
deactivate