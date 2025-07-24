#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
SQLite Management: Fornece acesso ao banco de dados SQLite para persistência.
"""

import os
import sqlite3
from datetime import datetime
from domain.Log import Logger
import sys
from pathlib import Path

# Import PathsManager
from infrastructure.utils.paths_manager import PathsManager

class SQLiteManagement:
    """
    Fornece acesso ao banco de dados SQLite para persistência de dados.

    Esta classe gerencia a conexão com o banco de dados SQLite e fornece
    métodos para operações básicas de CRUD em entidades do domínio.
    """

    def __init__(self, db_path=None, logger=None):
        """
        Inicializa o gateway do SQLite.

        Args:
            db_path: Caminho para o arquivo do banco de dados
            logger: Interface opcional para logging
        """
        if db_path is None:
            # Obtém o caminho do banco de dados do PathsManager
            paths_manager = PathsManager()
            db_path = paths_manager.database_path
            if logger:
                logger.registrar_info(f"Usando banco de dados: {db_path}")

        self.db_path = db_path
        self.conn = None
        self.logger = logger

    def get_connection(self):
        """
        Obtém uma conexão com o banco de dados.

        Returns:
            sqlite3.Connection: Conexão com o banco de dados
        """
        if self.conn is None:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row

        return self.conn

    def close_connection(self):
        """Fecha a conexão com o banco de dados se estiver aberta."""
        if self.conn is not None:
            self.conn.close()
            self.conn = None

    # --- CRUD para Tabela Arquivos ---

    def criar_arquivo_db(self, arquivo_uuid, arquivo_caminho, arquivo_nome, data_modificacao, tamanho_bytes, arquivo_tipo, arquivo_hash, data_indexacao):
        """
        Cria um novo registro na tabela Arquivos.
        
        Args:
            arquivo_uuid: UUID único do arquivo
            arquivo_caminho: Caminho completo do arquivo
            arquivo_nome: Nome do arquivo
            data_modificacao: Data de modificação do arquivo
            tamanho_bytes: Tamanho em bytes do arquivo
            arquivo_tipo: Tipo do arquivo (extensão)
            arquivo_hash: Hash xxHash64 do conteúdo do arquivo
            data_indexacao: Data em que o arquivo foi indexado
            
        Returns:
            arquivo_uuid: UUID do arquivo criado, ou None em caso de erro
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
            INSERT INTO Arquivos (arquivo_uuid, arquivo_caminho, arquivo_nome, data_modificacao, tamanho_bytes, arquivo_tipo, arquivo_hash, data_indexacao)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (arquivo_uuid, arquivo_caminho, arquivo_nome, data_modificacao, tamanho_bytes, arquivo_tipo, arquivo_hash, data_indexacao))
            conn.commit()
            return arquivo_uuid
        except sqlite3.Error as e:
            if self.logger:
                self.logger.registrar_erro(f"Erro técnico ao criar arquivo no banco: {e}")
            conn.rollback()
            return None

    def ler_arquivo_db(self, arquivo_uuid):
        """
        Lê um registro da tabela Arquivos pelo UUID.
        
        Args:
            arquivo_uuid: UUID do arquivo a ser lido
            
        Returns:
            dict: Dados do arquivo como dicionário ou None se não encontrado
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Arquivos WHERE arquivo_uuid = ?', (arquivo_uuid,))
        row = cursor.fetchone()
        if row:
            return dict(row)
        return None

    def atualizar_arquivo_db(self, arquivo_uuid, arquivo_caminho=None, arquivo_nome=None, data_modificacao=None, tamanho_bytes=None, arquivo_tipo=None, arquivo_hash=None, data_indexacao=None):
        """
        Atualiza um registro na tabela Arquivos pelo UUID.
        
        Args:
            arquivo_uuid: UUID do arquivo a ser atualizado
            arquivo_caminho: Novo caminho do arquivo (opcional)
            arquivo_nome: Novo nome do arquivo (opcional)
            data_modificacao: Nova data de modificação (opcional)
            tamanho_bytes: Novo tamanho em bytes (opcional)
            arquivo_tipo: Novo tipo de arquivo (opcional)
            arquivo_hash: Novo hash do arquivo (opcional)
            data_indexacao: Nova data de indexação (opcional)
            
        Returns:
            bool: True se a atualização foi bem-sucedida, False caso contrário
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        updates = {}
        if arquivo_caminho is not None:
            updates['arquivo_caminho'] = arquivo_caminho
        if arquivo_nome is not None:
            updates['arquivo_nome'] = arquivo_nome
        if data_modificacao is not None:
            updates['data_modificacao'] = data_modificacao
        if tamanho_bytes is not None:
            updates['tamanho_bytes'] = tamanho_bytes
        if arquivo_tipo is not None:
            updates['arquivo_tipo'] = arquivo_tipo
        if arquivo_hash is not None:
            updates['arquivo_hash'] = arquivo_hash
        if data_indexacao is not None:
            updates['data_indexacao'] = data_indexacao

        if not updates:
            return True  # Nada para atualizar

        set_clause = ', '.join(f'{key} = ?' for key in updates)
        values = list(updates.values())
        values.append(arquivo_uuid)

        try:
            cursor.execute(f'UPDATE Arquivos SET {set_clause} WHERE arquivo_uuid = ?', tuple(values))
            conn.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            if self.logger:
                self.logger.registrar_erro(f"Erro técnico ao atualizar arquivo no banco: {e}")
            conn.rollback()
            return False

    def apagar_arquivo_db(self, arquivo_uuid):
        """
        Apaga um registro da tabela Arquivos pelo UUID.
        
        Args:
            arquivo_uuid: UUID do arquivo a ser apagado
            
        Returns:
            bool: True se o arquivo foi apagado, False caso contrário
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('DELETE FROM Arquivos WHERE arquivo_uuid = ?', (arquivo_uuid,))
            conn.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            if self.logger:
                self.logger.registrar_erro(f"Erro técnico ao apagar arquivo do banco: {e}")
            conn.rollback()
            return False

    def listar_arquivos_db(self):
        """
        Lista todos os registros da tabela Arquivos.
        
        Returns:
            list: Lista de dicionários com os dados dos arquivos
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Arquivos')
        rows = cursor.fetchall()
        return [dict(row) for row in rows]

    # --- CRUD para Tabela Dados_RAW ---

    def criar_dados_raw_db(self, raw_uuid, arquivo_uuid, raw_conteudo, data_armazenamento):
        """
        Cria um novo registro na tabela Dados_RAW.
        
        Args:
            raw_uuid: UUID único para os dados raw
            arquivo_uuid: UUID do arquivo associado
            raw_conteudo: Conteúdo bruto do arquivo
            data_armazenamento: Data de armazenamento
            
        Returns:
            raw_uuid: UUID dos dados raw criados, ou None em caso de erro
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
            INSERT INTO Dados_RAW (raw_uuid, arquivo_uuid, raw_conteudo, data_armazenamento)
            VALUES (?, ?, ?, ?)
            ''', (raw_uuid, arquivo_uuid, raw_conteudo, data_armazenamento))
            conn.commit()
            return raw_uuid
        except sqlite3.Error as e:
            if self.logger:
                self.logger.registrar_erro(f"Erro técnico ao criar dados raw no banco: {e}")
            conn.rollback()
            return None

    def ler_dados_raw_db(self, raw_uuid):
        """
        Lê um registro da tabela Dados_RAW pelo UUID.
        
        Args:
            raw_uuid: UUID dos dados raw a ser lido
            
        Returns:
            dict: Dados raw como dicionário ou None se não encontrado
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Dados_RAW WHERE raw_uuid = ?', (raw_uuid,))
        row = cursor.fetchone()
        if row:
            return dict(row)
        return None

    def atualizar_dados_raw_db(self, raw_uuid, arquivo_uuid=None, raw_conteudo=None, data_armazenamento=None):
        """
        Atualiza um registro na tabela Dados_RAW pelo UUID.
        
        Args:
            raw_uuid: UUID dos dados raw a ser atualizado
            arquivo_uuid: Novo UUID do arquivo associado (opcional)
            raw_conteudo: Novo conteúdo bruto (opcional)
            data_armazenamento: Nova data de armazenamento (opcional)
            
        Returns:
            bool: True se a atualização foi bem-sucedida, False caso contrário
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        updates = {}
        if arquivo_uuid is not None:
            updates['arquivo_uuid'] = arquivo_uuid
        if raw_conteudo is not None:
            updates['raw_conteudo'] = raw_conteudo
        if data_armazenamento is not None:
            updates['data_armazenamento'] = data_armazenamento

        if not updates:
            return True

        set_clause = ', '.join(f'{key} = ?' for key in updates)
        values = list(updates.values())
        values.append(raw_uuid)

        try:
            cursor.execute(f'UPDATE Dados_RAW SET {set_clause} WHERE raw_uuid = ?', tuple(values))
            conn.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            if self.logger:
                self.logger.registrar_erro(f"Erro técnico ao atualizar dados raw no banco: {e}")
            conn.rollback()
            return False

    def apagar_dados_raw_db(self, raw_uuid):
        """
        Apaga um registro da tabela Dados_RAW pelo UUID.
        
        Args:
            raw_uuid: UUID dos dados raw a ser apagado
            
        Returns:
            bool: True se os dados foram apagados, False caso contrário
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('DELETE FROM Dados_RAW WHERE raw_uuid = ?', (raw_uuid,))
            conn.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            if self.logger:
                self.logger.registrar_erro(f"Erro técnico ao apagar dados raw do banco: {e}")
            conn.rollback()
            return False

    def listar_dados_raw_db(self):
        """
        Lista todos os registros da tabela Dados_RAW.
        
        Returns:
            list: Lista de dicionários com os dados raw
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Dados_RAW')
        rows = cursor.fetchall()
        return [dict(row) for row in rows]

    # --- CRUD para Tabela Chunks ---

    def criar_chunk_db(self, chunk_uuid, arquivo_uuid, chunk_texto, chunk_numero, chunk_tamanho_tokens, chunk_embedding):
        """
        Cria um novo registro na tabela Chunks.
        
        Args:
            chunk_uuid: UUID único para o chunk
            arquivo_uuid: UUID do arquivo associado
            chunk_texto: Texto do chunk
            chunk_numero: Número sequencial do chunk no documento
            chunk_tamanho_tokens: Tamanho estimado em tokens
            chunk_embedding: Embedding serializado (pode ser None)
            
        Returns:
            chunk_uuid: UUID do chunk criado, ou None em caso de erro
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
            INSERT INTO Chunks (chunk_uuid, arquivo_uuid, chunk_texto, chunk_numero, chunk_tamanho_tokens, chunk_embedding)
            VALUES (?, ?, ?, ?, ?, ?)
            ''', (chunk_uuid, arquivo_uuid, chunk_texto, chunk_numero, chunk_tamanho_tokens, chunk_embedding))
            conn.commit()
            return chunk_uuid
        except sqlite3.Error as e:
            if self.logger:
                self.logger.registrar_erro(f"Erro técnico ao criar chunk no banco: {e}")
            conn.rollback()
            return None

    def verificar_existencia_chunk_db(self, chunk_uuid):
        """
        Verifica se um chunk com o UUID especificado existe.
        
        Args:
            chunk_uuid: UUID do chunk a verificar
            
        Returns:
            bool: True se o chunk existe, False caso contrário
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT 1 FROM Chunks WHERE chunk_uuid = ?', (chunk_uuid,))
        return cursor.fetchone() is not None

    def ler_chunk_db(self, chunk_uuid):
        """
        Lê um registro da tabela Chunks pelo UUID.
        
        Args:
            chunk_uuid: UUID do chunk a ser lido
            
        Returns:
            dict: Dados do chunk como dicionário ou None se não encontrado
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Chunks WHERE chunk_uuid = ?', (chunk_uuid,))
        row = cursor.fetchone()
        if row:
            return dict(row)
        return None

    def atualizar_chunk_db(self, chunk_uuid, arquivo_uuid=None, chunk_texto=None, chunk_numero=None, chunk_tamanho_tokens=None, chunk_embedding=None):
        """
        Atualiza um registro na tabela Chunks pelo UUID.
        
        Args:
            chunk_uuid: UUID do chunk a ser atualizado
            arquivo_uuid: Novo UUID do arquivo associado (opcional)
            chunk_texto: Novo texto do chunk (opcional)
            chunk_numero: Novo número do chunk (opcional)
            chunk_tamanho_tokens: Novo tamanho em tokens (opcional)
            chunk_embedding: Novo embedding serializado (opcional)
            
        Returns:
            bool: True se a atualização foi bem-sucedida, False caso contrário
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        updates = {}
        if arquivo_uuid is not None:
            updates['arquivo_uuid'] = arquivo_uuid
        if chunk_texto is not None:
            updates['chunk_texto'] = chunk_texto
        if chunk_numero is not None:
            updates['chunk_numero'] = chunk_numero
        if chunk_tamanho_tokens is not None:
            updates['chunk_tamanho_tokens'] = chunk_tamanho_tokens
        if chunk_embedding is not None:
            updates['chunk_embedding'] = chunk_embedding

        if not updates:
            return True

        set_clause = ', '.join(f'{key} = ?' for key in updates)
        values = list(updates.values())
        values.append(chunk_uuid)

        try:
            cursor.execute(f'UPDATE Chunks SET {set_clause} WHERE chunk_uuid = ?', tuple(values))
            conn.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            if self.logger:
                self.logger.registrar_erro(f"Erro técnico ao atualizar chunk no banco: {e}")
            conn.rollback()
            return False

    def apagar_chunk_db(self, chunk_uuid):
        """
        Apaga um registro da tabela Chunks pelo UUID.
        
        Args:
            chunk_uuid: UUID do chunk a ser apagado
            
        Returns:
            bool: True se o chunk foi apagado, False caso contrário
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('DELETE FROM Chunks WHERE chunk_uuid = ?', (chunk_uuid,))
            conn.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            if self.logger:
                self.logger.registrar_erro(f"Erro técnico ao apagar chunk do banco: {e}")
            conn.rollback()
            return False

    def listar_chunks_db(self):
        """
        Lista todos os registros da tabela Chunks.
        
        Returns:
            list: Lista de dicionários com os dados dos chunks
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Chunks')
        rows = cursor.fetchall()
        return [dict(row) for row in rows]

    def listar_chunks_por_arquivo_db(self, arquivo_uuid):
        """
        Lista todos os chunks de um determinado arquivo.
        
        Args:
            arquivo_uuid: UUID do arquivo a filtrar
            
        Returns:
            list: Lista de dicionários com os dados dos chunks
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Chunks WHERE arquivo_uuid = ?', (arquivo_uuid,))
        rows = cursor.fetchall()
        return [dict(row) for row in rows]

    def buscar_chunk_por_id_db(self, chunk_id):
        """
        Busca um chunk pelo seu ID.
        
        Args:
            chunk_id: ID do chunk a ser buscado
            
        Returns:
            dict: Dados do chunk ou None se não encontrado
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('SELECT * FROM Chunks WHERE chunk_uuid = ?', (chunk_id,))
            row = cursor.fetchone()
            
            if not row:
                return None
            
            return dict(row)
            
        except sqlite3.Error as e:
            if self.logger:
                self.logger.registrar_erro(f"Erro técnico ao buscar chunk por ID: {str(e)}")
            return None

    # --- Métodos para operações em lote ---

    def apagar_todos_chunks_por_arquivo_db(self, arquivo_uuid):
        """
        Remove todos os chunks associados a um arquivo.
        
        Args:
            arquivo_uuid: UUID do arquivo
            
        Returns:
            int: Número de chunks removidos
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('DELETE FROM Chunks WHERE arquivo_uuid = ?', (arquivo_uuid,))
            removed = cursor.rowcount
            conn.commit()
            return removed
        except sqlite3.Error as e:
            if self.logger:
                self.logger.registrar_erro(f"Erro técnico ao apagar chunks por arquivo: {e}")
            conn.rollback()
            return 0

    def apagar_dados_raw_por_arquivo_db(self, arquivo_uuid):
        """
        Remove todos os dados raw associados a um arquivo.
        
        Args:
            arquivo_uuid: UUID do arquivo
            
        Returns:
            int: Número de registros removidos
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('DELETE FROM Dados_RAW WHERE arquivo_uuid = ?', (arquivo_uuid,))
            removed = cursor.rowcount
            conn.commit()
            return removed
        except sqlite3.Error as e:
            if self.logger:
                self.logger.registrar_erro(f"Erro técnico ao apagar dados raw por arquivo: {e}")
            conn.rollback()
            return 0

    def apagar_tudo_db(self):
        """
        Apaga todos os dados do banco de dados.
        
        Returns:
            bool: True se a operação foi bem-sucedida
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            # Apaga todos os registros das tabelas principais
            cursor.execute('DELETE FROM Chunks')
            cursor.execute('DELETE FROM Dados_RAW')
            cursor.execute('DELETE FROM Arquivos')
            conn.commit()
            return True
        except sqlite3.Error as e:
            if self.logger:
                self.logger.registrar_erro(f"Erro técnico ao apagar todos os dados: {e}")
            conn.rollback()
            return False
    

    def executar_transacao_db(self, funcao_transacao):
        """
        Executa uma função dentro de uma transação.
        
        Args:
            funcao_transacao: Função que recebe a conexão e cursor como parâmetros
            
        Returns:
            Any: O resultado da função ou None em caso de erro
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            conn.execute('BEGIN TRANSACTION')
            result = funcao_transacao(conn, cursor)
            conn.commit()
            return result
        except Exception as e:
            conn.rollback()
            if self.logger:
                self.logger.registrar_erro(f"Erro técnico na transação: {e}")
            return None

    # --- CRUD para Tabela Logs ---

    def criar_log_db(self, log_uuid, log_timestamp, log_tipo, log_mensagem, log_usuario=None, log_detalhes=None):
        """
        Cria um novo registro na tabela Logs.
        
        Args:
            log_uuid: UUID único para o log
            log_timestamp: Timestamp do log
            log_tipo: Tipo do log
            log_mensagem: Mensagem do log
            log_usuario: Usuário que gerou o log (opcional)
            log_detalhes: Detalhes adicionais (opcional)
            
        Returns:
            log_uuid: UUID do log criado, ou None em caso de erro
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
            INSERT INTO Logs (log_uuid, log_timestamp, log_tipo, log_mensagem, log_usuario, log_detalhes)
            VALUES (?, ?, ?, ?, ?, ?)
            ''', (log_uuid, log_timestamp, log_tipo, log_mensagem, log_usuario, log_detalhes))
            conn.commit()
            return log_uuid
        except sqlite3.Error as e:
            if self.logger:
                self.logger.registrar_erro(f"Erro técnico ao criar log no banco: {e}")
            conn.rollback()
            return None

    def ler_log_db(self, log_uuid):
        """
        Lê um registro da tabela Logs pelo UUID.
        
        Args:
            log_uuid: UUID do log a ser lido
            
        Returns:
            dict: Dados do log como dicionário ou None se não encontrado
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Logs WHERE log_uuid = ?', (log_uuid,))
        row = cursor.fetchone()
        if row:
            return dict(row)
        return None

    def listar_logs_db(self, limite=100, tipo=None):
        """
        Lista registros da tabela Logs, opcionalmente filtrados por tipo.
        
        Args:
            limite: Número máximo de logs a retornar
            tipo: Tipo de log para filtrar (opcional)
            
        Returns:
            list: Lista de dicionários com os dados dos logs
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if tipo:
            cursor.execute('SELECT * FROM Logs WHERE log_tipo = ? ORDER BY log_timestamp DESC LIMIT ?', (tipo, limite))
        else:
            cursor.execute('SELECT * FROM Logs ORDER BY log_timestamp DESC LIMIT ?', (limite,))
            
        rows = cursor.fetchall()
        return [dict(row) for row in rows]

    # --- Métodos de contagem para status ---
    
    def contar_documentos(self):
        """
        Conta o número total de documentos na tabela Arquivos.
        
        Returns:
            int: Número total de documentos
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('SELECT COUNT(*) as total FROM Arquivos')
            result = cursor.fetchone()
            return result['total'] if result else 0
        except sqlite3.Error as e:
            if self.logger:
                self.logger.registrar_erro(f"Erro ao contar documentos: {str(e)}")
            return 0
    
    def listar_documentos(self):
        """
        Lista todos os documentos da tabela Arquivos.
        Um alias para listar_arquivos_db() para manter consistência na nomenclatura.
        
        Returns:
            list: Lista de dicionários com os dados dos arquivos
        """
        return self.listar_arquivos_db()
    
    def contar_chunks(self):
        """
        Conta o número total de chunks na tabela Chunks.
        
        Returns:
            int: Número total de chunks
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('SELECT COUNT(*) as total FROM Chunks')
            result = cursor.fetchone()
            return result['total'] if result else 0
        except sqlite3.Error as e:
            if self.logger:
                self.logger.registrar_erro(f"Erro ao contar chunks: {str(e)}")
            return 0