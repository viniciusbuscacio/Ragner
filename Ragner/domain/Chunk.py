#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Chunk: Representa um pedaço de texto extraído de um documento.
"""

class Chunk:
    """
    Representa um pedaço de texto extraído de um documento.
    
    Um chunk é uma unidade de texto que foi extraída de um documento para
    processamento pelo sistema RAG. Cada chunk contém um texto, um UUID único,
    um UUID do documento de origem, e pode ter um embedding associado.
    """
    
    def __init__(self, chunk_uuid=None, arquivo_uuid=None, chunk_texto="", 
                 chunk_numero=0, chunk_tamanho_tokens=0, chunk_embedding=None):
        """
        Inicializa um novo Chunk.
        
        Args:
            chunk_uuid: UUID único do chunk no banco de dados
            arquivo_uuid: UUID do arquivo ao qual este chunk pertence
            chunk_texto: Conteúdo textual do chunk
            chunk_numero: Posição deste chunk no documento original
            chunk_tamanho_tokens: Número de tokens que este chunk contém
            chunk_embedding: Representação vetorial do chunk (opcional)
        """
        self.chunk_uuid = chunk_uuid
        self.arquivo_uuid = arquivo_uuid
        self.chunk_texto = chunk_texto
        self.chunk_numero = chunk_numero
        self.chunk_tamanho_tokens = chunk_tamanho_tokens
        self.chunk_embedding = chunk_embedding
    
    def __str__(self):
        """Retorna uma representação em string do chunk."""
        return f"Chunk(uuid={self.chunk_uuid}, texto={self.chunk_texto[:50]}..., arquivo_uuid={self.arquivo_uuid})"
    
    def to_dict(self):
        """
        Converte o chunk em um dicionário.
        
        Returns:
            dict: Representação em dicionário do chunk
        """
        return {
            "chunk_uuid": self.chunk_uuid,
            "arquivo_uuid": self.arquivo_uuid,
            "chunk_texto": self.chunk_texto,
            "chunk_numero": self.chunk_numero,
            "chunk_tamanho_tokens": self.chunk_tamanho_tokens
        }