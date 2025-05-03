#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ChunkRepository: Interface para operações relacionadas a Chunks.
"""

import abc
from typing import List, Optional, Dict, Any, Union
from domain.Chunk import Chunk
from domain.Embedding import Embedding


class ChunkRepository(abc.ABC):
    """
    Interface para persistência de Chunks.
    
    Esta interface define os contratos que qualquer implementação
    de repositório de Chunks deve seguir.
    """
    
    @abc.abstractmethod
    def salvar_chunk(self, chunk: Chunk) -> Chunk:
        """
        Salva um chunk no repositório.
        
        Args:
            chunk: O objeto Chunk a ser salvo
            
        Returns:
            Chunk: O chunk salvo com UUID atualizado se necessário
        """
        pass
    
    @abc.abstractmethod
    def buscar_por_id(self, chunk_id: str) -> Optional[Chunk]:
        """
        Busca um chunk pelo seu ID.
        
        Args:
            chunk_id: O ID do chunk a ser buscado
            
        Returns:
            Optional[Chunk]: O chunk encontrado ou None se não existir
        """
        pass
    
    @abc.abstractmethod
    def atualizar_embedding(self, chunk_id: str, embedding: Embedding) -> bool:
        """
        Atualiza o embedding de um chunk.
        
        Args:
            chunk_id: O ID do chunk a ser atualizado
            embedding: O embedding a ser associado ao chunk
            
        Returns:
            bool: True se a operação foi bem-sucedida
        """
        pass
    
    @abc.abstractmethod
    def listar_por_arquivo(self, arquivo_uuid: str) -> List[Chunk]:
        """
        Lista todos os chunks de um determinado arquivo.
        
        Args:
            arquivo_uuid: O UUID do arquivo
            
        Returns:
            List[Chunk]: Lista dos chunks encontrados
        """
        pass
    
    @abc.abstractmethod
    def existe_chunk(self, chunk_id: str) -> bool:
        """
        Verifica se um chunk com o ID especificado existe.
        
        Args:
            chunk_id: O ID do chunk a verificar
            
        Returns:
            bool: True se o chunk existir, False caso contrário
        """
        pass
    
    @abc.abstractmethod
    def apagar_chunk(self, chunk_id: str) -> bool:
        """
        Remove um chunk do repositório.
        
        Args:
            chunk_id: O ID do chunk a remover
            
        Returns:
            bool: True se a operação foi bem-sucedida
        """
        pass
    
    @abc.abstractmethod
    def apagar_chunks_por_arquivo(self, arquivo_uuid: str) -> int:
        """
        Remove todos os chunks associados a um arquivo.
        
        Args:
            arquivo_uuid: O UUID do arquivo
            
        Returns:
            int: Número de chunks removidos
        """
        pass