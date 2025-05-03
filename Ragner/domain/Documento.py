#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Documento: Representa um arquivo que foi carregado para o sistema.
"""

import os
from datetime import datetime

class Documento:
    """
    Representa um documento que foi carregado para o sistema.
    
    Um documento contém metadados como uuid, nome, caminho do arquivo, tipo,
    data de indexação, data de modificação, tamanho em bytes e hash do arquivo.
    """
    
    def __init__(self, arquivo_uuid=None, arquivo_nome="", arquivo_caminho="", 
                 arquivo_tipo="", data_indexacao=None, data_modificacao=None, 
                 tamanho_bytes=0, arquivo_hash="", chunks=None):
        """
        Inicializa um novo Documento.
        
        Args:
            arquivo_uuid: UUID único do documento no banco de dados
            arquivo_nome: Nome do arquivo
            arquivo_caminho: Caminho completo para o arquivo
            arquivo_tipo: Tipo do documento (pdf, docx, txt, etc.)
            data_indexacao: Data em que o documento foi indexado
            data_modificacao: Data em que o arquivo foi modificado pela última vez
            tamanho_bytes: Tamanho do arquivo em bytes
            arquivo_hash: Hash do conteúdo do arquivo
            chunks: Lista de chunks associados ao documento
        """
        self.arquivo_uuid = arquivo_uuid
        self.arquivo_nome = arquivo_nome
        self.arquivo_caminho = arquivo_caminho
        self.arquivo_tipo = arquivo_tipo
        self.data_indexacao = data_indexacao or datetime.now()
        self.data_modificacao = data_modificacao or datetime.now()
        self.tamanho_bytes = tamanho_bytes
        self.arquivo_hash = arquivo_hash
        self.chunks = chunks or []
    
    def __str__(self):
        """Retorna uma representação em string do documento."""
        return f"Documento(uuid={self.arquivo_uuid}, nome={self.arquivo_nome}, tipo={self.arquivo_tipo})"
    
    @classmethod
    def from_file_path(cls, file_path):
        """
        Cria uma instância de Documento a partir de um caminho de arquivo.
        
        Args:
            file_path: Caminho completo para o arquivo
            
        Returns:
            Documento: Nova instância de Documento
        """
        nome = os.path.basename(file_path)
        tipo = os.path.splitext(nome)[1].lower().replace('.', '')
        
        # Obtendo informações adicionais do arquivo
        file_stats = os.stat(file_path)
        tamanho = file_stats.st_size
        data_mod = datetime.fromtimestamp(file_stats.st_mtime)
        
        return cls(
            arquivo_nome=nome,
            arquivo_caminho=file_path,
            arquivo_tipo=tipo,
            data_modificacao=data_mod,
            tamanho_bytes=tamanho
        )
    
    def add_chunk(self, chunk):
        """
        Adiciona um chunk a este documento.
        
        Args:
            chunk: O chunk a ser adicionado
        """
        chunk.arquivo_uuid = self.arquivo_uuid
        self.chunks.append(chunk)
    
    def to_dict(self):
        """
        Converte o documento em um dicionário.
        
        Returns:
            dict: Representação em dicionário do documento
        """
        return {
            "arquivo_uuid": self.arquivo_uuid,
            "arquivo_nome": self.arquivo_nome,
            "arquivo_caminho": self.arquivo_caminho,
            "arquivo_tipo": self.arquivo_tipo,
            "data_indexacao": self.data_indexacao.timestamp() if self.data_indexacao else None,
            "data_modificacao": self.data_modificacao.timestamp() if self.data_modificacao else None,
            "tamanho_bytes": self.tamanho_bytes,
            "arquivo_hash": self.arquivo_hash
        }