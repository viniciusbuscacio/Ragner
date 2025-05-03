#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Embedding: Representa um vetor de embedding para um chunk de texto.
"""

import numpy as np

class Embedding:
    """
    Representa um vetor de embedding para um chunk de texto.
    
    Um embedding é uma representação vetorial de um texto que captura
    seu significado semântico em um espaço de alta dimensionalidade.
    """
    
    def __init__(self, id=None, chunk_id=None, vetor=None, modelo="text-embedding-3-small"):
        """
        Inicializa um novo Embedding.
        
        Args:
            id: ID único do embedding no banco de dados
            chunk_id: ID do chunk ao qual este embedding pertence
            vetor: Array numpy contendo o vetor de embedding
            modelo: Nome do modelo usado para gerar o embedding
        """
        self.id = id
        self.chunk_id = chunk_id
        self.vetor = vetor if vetor is not None else np.array([])
        self.modelo = modelo
        self.dimensao = len(self.vetor) if vetor is not None else 0
    
    def __str__(self):
        """Retorna uma representação em string do embedding."""
        return f"Embedding(id={self.id}, chunk_id={self.chunk_id}, dimensao={self.dimensao})"
    
    def to_dict(self):
        """
        Converte o embedding em um dicionário.
        
        Returns:
            dict: Representação em dicionário do embedding
        """
        return {
            "id": self.id,
            "chunk_id": self.chunk_id,
            "vetor": self.vetor.tolist() if hasattr(self.vetor, 'tolist') else self.vetor,
            "modelo": self.modelo,
            "dimensao": self.dimensao
        }
    
    @classmethod
    def from_list(cls, vector_list, chunk_id=None, modelo="text-embedding-3-small"):
        """
        Cria um Embedding a partir de uma lista de números.
        
        Args:
            vector_list: Lista de números representando o vetor
            chunk_id: ID do chunk associado
            modelo: Nome do modelo usado para gerar o embedding
            
        Returns:
            Embedding: Nova instância de Embedding
        """
        return cls(
            chunk_id=chunk_id,
            vetor=np.array(vector_list),
            modelo=modelo
        )