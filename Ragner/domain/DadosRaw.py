#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
DadosRaw: Representa os dados brutos de um arquivo armazenado no sistema.
"""

from datetime import datetime

class DadosRaw:
    """
    Representa os dados brutos de um arquivo armazenado no sistema.
    
    Esta classe armazena o conteúdo binário de um documento indexado,
    mantendo-o associado ao documento original através do arquivo_uuid.
    """
    
    def __init__(self, raw_uuid=None, arquivo_uuid=None, raw_conteudo=None, data_armazenamento=None):
        """
        Inicializa um novo objeto DadosRaw.
        
        Args:
            raw_uuid: UUID único dos dados brutos no banco de dados
            arquivo_uuid: UUID do arquivo ao qual estes dados pertencem
            raw_conteudo: Conteúdo binário do arquivo
            data_armazenamento: Data em que os dados foram armazenados
        """
        self.raw_uuid = raw_uuid
        self.arquivo_uuid = arquivo_uuid
        self.raw_conteudo = raw_conteudo
        self.data_armazenamento = data_armazenamento or datetime.now()
    
    def __str__(self):
        """Retorna uma representação em string dos dados brutos."""
        return f"DadosRaw(uuid={self.raw_uuid}, arquivo_uuid={self.arquivo_uuid}, tamanho={len(self.raw_conteudo) if self.raw_conteudo else 0} bytes)"
    
    def to_dict(self):
        """
        Converte os dados brutos em um dicionário.
        
        Returns:
            dict: Representação em dicionário dos dados brutos
        """
        return {
            "raw_uuid": self.raw_uuid,
            "arquivo_uuid": self.arquivo_uuid,
            "data_armazenamento": self.data_armazenamento.timestamp() if self.data_armazenamento else None
        }