#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
SQLiteChunkRepository: Implementação SQLite do repositório de Chunks.
"""

import json
from typing import List, Optional
import uuid

from domain.repositories.ChunkRepository import ChunkRepository
from domain.Chunk import Chunk 
from domain.Embedding import Embedding
from domain.Log import Logger

from infrastructure.database.sqlite_management import SQLiteManagement

class SQLiteChunkRepository(ChunkRepository):
    """
    Implementação do repositório de Chunks usando SQLite.
    
    Esta classe concreta implementa as operações do repositório
    de Chunks usando o SQLiteManagement como mecanismo de persistência.
    """
    
    def __init__(self, db_gateway: SQLiteManagement, logger: Logger = None):
        """
        Inicializa o repositório SQLite para Chunks.
        
        Args:
            db_gateway: Gateway para o banco de dados SQLite
            logger: Interface opcional para logging
        """
        self.db_gateway = db_gateway
        self.logger = logger
    
    def salvar_chunk(self, chunk: Chunk) -> Chunk:
        """
        Salva um chunk no repositório.
        
        Args:
            chunk: O objeto Chunk a ser salvo
            
        Returns:
            Chunk: O chunk salvo com UUID atualizado se necessário
        """
        # Se o Chunk não tem UUID, gera um novo
        if not chunk.chunk_uuid:
            chunk.chunk_uuid = str(uuid.uuid4())
        
        # Verifica se o chunk já existe
        if self.existe_chunk(chunk.chunk_uuid):
            # Atualiza o chunk existente
            self.db_gateway.atualizar_chunk_db(
                chunk_uuid=chunk.chunk_uuid,
                arquivo_uuid=chunk.arquivo_uuid,
                chunk_texto=chunk.chunk_texto,
                chunk_numero=chunk.chunk_numero,
                chunk_tamanho_tokens=chunk.chunk_tamanho_tokens
            )
        else:
            # Cria um novo chunk
            self.db_gateway.criar_chunk_db(
                chunk_uuid=chunk.chunk_uuid,
                arquivo_uuid=chunk.arquivo_uuid,
                chunk_texto=chunk.chunk_texto,
                chunk_numero=chunk.chunk_numero,
                chunk_tamanho_tokens=chunk.chunk_tamanho_tokens,
                chunk_embedding=None  # O embedding será salvo separadamente
            )
        
        return chunk
    
    def buscar_por_id(self, chunk_id: str) -> Optional[Chunk]:
        """
        Busca um chunk pelo seu ID.
        
        Args:
            chunk_id: O ID do chunk a ser buscado
            
        Returns:
            Optional[Chunk]: O chunk encontrado ou None se não existir
        """
        chunk_data = self.db_gateway.buscar_chunk_por_id_db(chunk_id)
        
        if not chunk_data:
            return None
        
        chunk = Chunk(
            chunk_uuid=chunk_data['chunk_uuid'],
            arquivo_uuid=chunk_data['arquivo_uuid'],
            chunk_texto=chunk_data['chunk_texto'],
            chunk_numero=chunk_data['chunk_numero'],
            chunk_tamanho_tokens=chunk_data['chunk_tamanho_tokens'],
            chunk_embedding=chunk_data['chunk_embedding']
        )
        
        # Se o arquivo_nome foi incluído (é um enriquecimento do context)
        if 'arquivo_nome' in chunk_data:
            chunk.arquivo_nome = chunk_data['arquivo_nome']
        
        return chunk
    
    def atualizar_embedding(self, chunk_id: str, embedding: Embedding) -> bool:
        """
        Atualiza o embedding de um chunk.
        
        Args:
            chunk_id: O ID do chunk a ser atualizado
            embedding: O embedding a ser associado ao chunk
            
        Returns:
            bool: True se a operação foi bem-sucedida
        """
        # Verifica se o chunk existe
        if not self.existe_chunk(chunk_id):
            if self.logger:
                self.logger.registrar_erro(f"Erro: Chunk {chunk_id} não encontrado no banco de dados.")
            return False
        
        # Converte o vetor para JSON para armazenamento
        vetor_serializado = json.dumps([float(x) for x in embedding.vetor])
        
        # Atualiza apenas o campo de embedding
        resultado = self.db_gateway.atualizar_chunk_db(
            chunk_uuid=chunk_id,
            chunk_embedding=vetor_serializado
        )
        
        if resultado:
            if self.logger:
                self.logger.registrar_info(f"Indexando o conteúdo dos documentos - chunk_id={chunk_id}")
            return True
        else:
            if self.logger:
                self.logger.registrar_erro(f"Aviso: Não foi possível atualizar o embedding para chunk_id={chunk_id}")
            return False
    
    def listar_por_arquivo(self, arquivo_uuid: str) -> List[Chunk]:
        """
        Lista todos os chunks de um determinado arquivo.
        
        Args:
            arquivo_uuid: O UUID do arquivo
            
        Returns:
            List[Chunk]: Lista dos chunks encontrados
        """
        chunks_data = self.db_gateway.listar_chunks_por_arquivo_db(arquivo_uuid)
        
        chunks = []
        for chunk_data in chunks_data:
            chunk = Chunk(
                chunk_uuid=chunk_data['chunk_uuid'],
                arquivo_uuid=chunk_data['arquivo_uuid'],
                chunk_texto=chunk_data['chunk_texto'],
                chunk_numero=chunk_data['chunk_numero'],
                chunk_tamanho_tokens=chunk_data['chunk_tamanho_tokens'],
                chunk_embedding=chunk_data['chunk_embedding']
            )
            chunks.append(chunk)
        
        return chunks
    
    def existe_chunk(self, chunk_id: str) -> bool:
        """
        Verifica se um chunk com o ID especificado existe.
        
        Args:
            chunk_id: O ID do chunk a verificar
            
        Returns:
            bool: True se o chunk existir, False caso contrário
        """
        return self.db_gateway.verificar_existencia_chunk_db(chunk_id)
    
    def apagar_chunk(self, chunk_id: str) -> bool:
        """
        Remove um chunk do repositório.
        
        Args:
            chunk_id: O ID do chunk a remover
            
        Returns:
            bool: True se a operação foi bem-sucedida
        """
        return self.db_gateway.apagar_chunk_db(chunk_id)
    
    def apagar_chunks_por_arquivo(self, arquivo_uuid: str) -> int:
        """
        Remove todos os chunks associados a um arquivo.
        
        Args:
            arquivo_uuid: O UUID do arquivo
            
        Returns:
            int: Número de chunks removidos
        """
        return self.db_gateway.apagar_todos_chunks_por_arquivo_db(arquivo_uuid)