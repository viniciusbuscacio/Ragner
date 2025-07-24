#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
SQLite Check: Verifica se o banco de dados SQLite está acessível e funcional.
"""

import os
import sqlite3
import logging
import sys
from pathlib import Path
from domain.Log import Logger

# Importar o PathsManager
from infrastructure.utils.paths_manager import PathsManager

# Configuração de log personalizada para separar o que vai para o arquivo/banco do que é mostrado ao usuário
class UserFriendlyLogFormatter(logging.Formatter):
    def format(self, record):
        return record.getMessage()

def verificar_criar_banco(logger=None, mostrar_log_usuario=True):
    """
    Verifica se o banco de dados SQLite existe e está com a estrutura correta.
    Se não existir, cria o banco com as tabelas necessárias.
    
    Args:
        logger: Interface de Logger para registro de mensagens
        mostrar_log_usuario (bool): Se True, exibe mensagens de log para o usuário
                                   em formato simplificado
    """
    # Configurar logger personalizado se solicitado
    if mostrar_log_usuario and not logger:
        # Criar handler para console com formatação amigável
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(UserFriendlyLogFormatter())
        
        # Obter logger e configurar
        user_logger = logging.getLogger('user_friendly')
        user_logger.setLevel(logging.INFO)
        
        # Remover handlers antigos se existirem
        for handler in user_logger.handlers[:]:
            user_logger.removeHandler(handler)
        
        user_logger.addHandler(console_handler)
        
        # Não propagar para o logger raiz (que tem o formato completo)
        user_logger.propagate = False
    else:
        user_logger = logging.getLogger('null_logger')
        user_logger.addHandler(logging.NullHandler())
    
    # Obter o caminho do banco de dados do PathsManager
    paths_manager = PathsManager()
    db_path = paths_manager.database_path
    
    # Verificar se o arquivo existe
    db_existe = os.path.exists(db_path)
    
    # Conectar ao banco (isso criará o arquivo se não existir)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Definição das tabelas
    tabelas = {
        "Arquivos": """
            CREATE TABLE IF NOT EXISTS Arquivos (
                arquivo_uuid TEXT PRIMARY KEY,
                arquivo_caminho TEXT,
                arquivo_nome TEXT,
                data_modificacao REAL,
                tamanho_bytes INTEGER,
                arquivo_tipo TEXT,
                arquivo_hash TEXT,
                data_indexacao REAL
            )
        """,
        "Dados_RAW": """
            CREATE TABLE IF NOT EXISTS Dados_RAW (
                raw_uuid TEXT PRIMARY KEY,
                arquivo_uuid TEXT,
                raw_conteudo TEXT,
                data_armazenamento REAL,
                FOREIGN KEY (arquivo_uuid) REFERENCES Arquivos(arquivo_uuid)
            )
        """,
        "Chunks": """
            CREATE TABLE IF NOT EXISTS Chunks (
                chunk_uuid TEXT PRIMARY KEY,
                arquivo_uuid TEXT,
                chunk_texto TEXT,
                chunk_numero INTEGER,
                chunk_tamanho_tokens INTEGER,
                chunk_embedding TEXT,
                FOREIGN KEY (arquivo_uuid) REFERENCES Arquivos(arquivo_uuid)
            )
        """,
        "Logs": """
            CREATE TABLE IF NOT EXISTS Logs (
                log_uuid TEXT PRIMARY KEY,
                log_timestamp REAL,
                log_tipo TEXT,
                log_mensagem TEXT,
                log_usuario TEXT,
                log_detalhes TEXT
            )
        """
    }

    # Se o banco não existia, criar as tabelas
    if not db_existe:
        if logger:
            logger.registrar_info(f"Banco de dados não encontrado. Criando em: {db_path}")
        
        for nome_tabela, sql_criacao in tabelas.items():
            cursor.execute(sql_criacao)
        conn.commit()
       


    else:
        # Verificar se todas as tabelas existem com os campos corretos
        if logger:
            logger.registrar_info("Verificando banco de dados...")
            
        for nome_tabela in tabelas.keys():
            # Verificar se a tabela existe
            cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{nome_tabela}'")
            if not cursor.fetchone():
                if logger:
                    logger.registrar_info(f"Tabela {nome_tabela} não encontrada. Criando...")
                
                cursor.execute(tabelas[nome_tabela])
                conn.commit()
            else:
                # Verificar se a estrutura da tabela está correta
                cursor.execute(f"PRAGMA table_info({nome_tabela})")
                colunas_existentes = {coluna[1]: coluna[2] for coluna in cursor.fetchall()}
                
                # Extrair os nomes e tipos de colunas esperados da definição da tabela
                # Esta é uma aproximação simples - em um caso real seria melhor usar regex ou um parser SQL
                definicao = tabelas[nome_tabela]
                linhas = [linha.strip() for linha in definicao.split('\n') if ',' in linha or ')' in linha]
                colunas_esperadas = {}
                for linha in linhas:
                    if not linha or linha.startswith('CREATE') or linha.startswith('FOREIGN KEY'):
                        continue
                    partes = linha.strip().strip(',').strip(')').strip().split(' ', 1)
                    if len(partes) >= 2:
                        nome = partes[0]
                        tipo = partes[1].split(' ')[0]  # Pegar apenas o tipo, não constraints
                        colunas_esperadas[nome] = tipo
                
                # Comparar colunas existentes com esperadas
                for coluna, tipo in colunas_esperadas.items():
                    if coluna not in colunas_existentes:
                        if logger:
                            logger.registrar_erro(f"Coluna {coluna} não encontrada na tabela {nome_tabela}")
                            logger.registrar_erro(f"Coluna {coluna} ausente na tabela {nome_tabela}")
                    elif tipo.upper() != colunas_existentes[coluna].upper():
                        if logger:
                            logger.registrar_erro(f"Tipo da coluna {coluna} na tabela {nome_tabela} não corresponde.")
                            logger.registrar_erro(f"Esperado: {tipo}, Encontrado: {colunas_existentes[coluna]}")
                            logger.registrar_erro(f"Inconsistência na coluna {coluna} da tabela {nome_tabela}")
        
        if logger:
            logger.registrar_info("Verificação de tabelas concluída.")
    
    conn.close()
    return db_path

if __name__ == "__main__":
    db_path = verificar_criar_banco()
