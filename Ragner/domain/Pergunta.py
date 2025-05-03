#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Pergunta: Representa uma pergunta feita pelo usuário ao sistema.
"""

from datetime import datetime

class Pergunta:
    """
    Representa uma pergunta feita pelo usuário ao sistema.
    
    Uma pergunta contém o texto da pergunta, timestamp de quando foi feita,
    e pode ter um embedding associado para busca semântica.
    """
    
    def __init__(self, id=None, texto="", timestamp=None, embedding=None):
        """
        Inicializa uma nova Pergunta.
        
        Args:
            id: ID único da pergunta no banco de dados
            texto: Texto da pergunta
            timestamp: Momento em que a pergunta foi feita
            embedding: Representação vetorial da pergunta (opcional)
        """
        self.id = id
        self.texto = texto
        self.timestamp = timestamp or datetime.now()
        self.embedding = embedding
    
    def __str__(self):
        """Retorna uma representação em string da pergunta."""
        return f"Pergunta(id={self.id}, texto={self.texto})"
    
    def to_dict(self):
        """
        Converte a pergunta em um dicionário.
        
        Returns:
            dict: Representação em dicionário da pergunta
        """
        return {
            "id": self.id,
            "texto": self.texto,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None
        }