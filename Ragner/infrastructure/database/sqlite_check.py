#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
SQLite Check: Verifica se o banco de dados SQLite está acessível e funcional.
"""

import os
import sqlite3
import logging
from pathlib import Path
from presentation.cli.cli_cores import Cores


# Configuração de log personalizada para separar o que vai para o arquivo/banco do que é mostrado ao usuário
class UserFriendlyLogFormatter(logging.Formatter):
    def format(self, record):
        # Formato simplificado para exibição ao usuário (sem timestamp e nível)
        return f"{record.getMessage()}"

def verificar_criar_banco(mostrar_log_usuario=True):
    """
    Verifica se o banco de dados SQLite existe e está com a estrutura correta.
    Se não existir, cria o banco com as tabelas necessárias.
    
    Args:
        mostrar_log_usuario (bool): Se True, exibe mensagens de log para o usuário
                                   em formato simplificado
    """
    # Configurar logger personalizado se solicitado
    if mostrar_log_usuario:
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
    
    # Definir o caminho do banco de dados
    db_path = Path(__file__).parent / "database.sqlite3"
    
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
                chunk_embedding BLOB,
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
        print(f"{Cores.CINZA}Banco de dados não encontrado. Criando em: {db_path}{Cores.RESET}")
        
        for nome_tabela, sql_criacao in tabelas.items():
            cursor.execute(sql_criacao)
        conn.commit()
       


    else:
        print(f"{Cores.CINZA}Banco de dados encontrado em: {db_path}{Cores.RESET}")
        print(f"{Cores.CINZA}Verificando banco de dados...{Cores.RESET}")
        
        # Verificar se todas as tabelas existem com os campos corretos
        for nome_tabela in tabelas.keys():
            # Verificar se a tabela existe
            cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{nome_tabela}'")
            if not cursor.fetchone():
                print(f"{Cores.CINZA}Tabela {nome_tabela} não encontrada. Criando...{Cores.RESET}")
                
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
                        print(f"{Cores.CINZA}Coluna {coluna} não encontrada na tabela {nome_tabela}{Cores.RESET}")
                        print(f"{Cores.CINZA}Coluna {coluna} ausente na tabela {nome_tabela}{Cores.RESET}")
                    elif tipo.upper() != colunas_existentes[coluna].upper():
                        print(f"{Cores.CINZA}Tipo da coluna {coluna} na tabela {nome_tabela} não corresponde.{Cores.RESET}")
                        print(f"{Cores.CINZA}Esperado: {tipo}, Encontrado: {colunas_existentes[coluna]}{Cores.RESET}")
                        print(f"{Cores.CINZA}Inconsistência na coluna {coluna} da tabela {nome_tabela}{Cores.RESET}")
        
        print(f"{Cores.CINZA}Verificação de tabelas concluída.{Cores.RESET}")
    
    conn.close()
    return db_path

if __name__ == "__main__":
    db_path = verificar_criar_banco()
