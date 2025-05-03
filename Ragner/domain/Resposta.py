#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Resposta: Representa uma resposta gerada pelo sistema a uma pergunta do usuário.
"""

from datetime import datetime

class Resposta:
    """
    Representa uma resposta gerada pelo sistema a uma pergunta do usuário.
    
    Uma resposta contém o texto da resposta, referências aos chunks utilizados,
    a pergunta associada, e o timestamp de quando foi gerada.
    """
    
    def __init__(self, id=None, texto="", pergunta_id=None, pergunta=None, chunks_utilizados=None, timestamp=None):
        """
        Inicializa uma nova Resposta.
        
        Args:
            id: ID único da resposta no banco de dados
            texto: Texto da resposta gerada
            pergunta_id: ID da pergunta à qual esta resposta está associada
            pergunta: Objeto Pergunta associado (opcional)
            chunks_utilizados: Lista de chunks utilizados para gerar a resposta
            timestamp: Momento em que a resposta foi gerada
        """
        self.id = id
        self.texto = texto
        self.pergunta_id = pergunta_id
        self.pergunta = pergunta
        self.chunks_utilizados = chunks_utilizados or []
        self.timestamp = timestamp or datetime.now()
    
    def __str__(self):
        """Retorna uma representação em string da resposta."""
        texto_resumido = self.texto[:50] + "..." if len(self.texto) > 50 else self.texto
        return f"Resposta(id={self.id}, texto={texto_resumido}, pergunta_id={self.pergunta_id})"
    
    def adicionar_chunk(self, chunk):
        """
        Adiciona um chunk utilizado para gerar esta resposta.
        
        Args:
            chunk: O chunk a ser adicionado
        """
        self.chunks_utilizados.append(chunk)
    
    def to_dict(self):
        """
        Converte a resposta em um dicionário.
        
        Returns:
            dict: Representação em dicionário da resposta
        """
        return {
            "id": self.id,
            "texto": self.texto,
            "pergunta_id": self.pergunta_id,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
            "chunks_utilizados": [chunk.id for chunk in self.chunks_utilizados] if self.chunks_utilizados else []
        }