#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Log: Representa um registro de log no sistema.
"""

from datetime import datetime

class Log:
    """
    Representa um registro de log no sistema.
    
    Esta classe armazena informações sobre eventos ocorridos no sistema,
    incluindo timestamp, tipo, mensagem, usuário e detalhes.
    """
    
    def __init__(self, log_uuid=None, log_timestamp=None, log_tipo="", 
                 log_mensagem="", log_usuario="", log_detalhes=""):
        """
        Inicializa um novo objeto Log.
        
        Args:
            log_uuid: UUID único do log no banco de dados
            log_timestamp: Timestamp de quando o log foi gerado
            log_tipo: Tipo de log (INFO, WARNING, ERROR, etc.)
            log_mensagem: Mensagem principal do log
            log_usuario: Usuário que gerou o log
            log_detalhes: Detalhes adicionais do log
        """
        self.log_uuid = log_uuid
        self.log_timestamp = log_timestamp or datetime.now()
        self.log_tipo = log_tipo
        self.log_mensagem = log_mensagem
        self.log_usuario = log_usuario
        self.log_detalhes = log_detalhes
    
    def __str__(self):
        """Retorna uma representação em string do log."""
        return f"Log(uuid={self.log_uuid}, tipo={self.log_tipo}, mensagem={self.log_mensagem})"
    
    @classmethod
    def info(cls, mensagem, usuario="sistema", detalhes=""):
        """
        Cria um log de tipo INFO.
        
        Args:
            mensagem: Mensagem principal do log
            usuario: Usuário associado ao log
            detalhes: Detalhes adicionais
            
        Returns:
            Log: Nova instância de Log do tipo INFO
        """
        return cls(log_tipo="INFO", log_mensagem=mensagem, 
                   log_usuario=usuario, log_detalhes=detalhes)
    
    @classmethod
    def warning(cls, mensagem, usuario="sistema", detalhes=""):
        """
        Cria um log de tipo WARNING.
        
        Args:
            mensagem: Mensagem principal do log
            usuario: Usuário associado ao log
            detalhes: Detalhes adicionais
            
        Returns:
            Log: Nova instância de Log do tipo WARNING
        """
        return cls(log_tipo="WARNING", log_mensagem=mensagem, 
                   log_usuario=usuario, log_detalhes=detalhes)
    
    @classmethod
    def error(cls, mensagem, usuario="sistema", detalhes=""):
        """
        Cria um log de tipo ERROR.
        
        Args:
            mensagem: Mensagem principal do log
            usuario: Usuário associado ao log
            detalhes: Detalhes adicionais
            
        Returns:
            Log: Nova instância de Log do tipo ERROR
        """
        return cls(log_tipo="ERROR", log_mensagem=mensagem, 
                   log_usuario=usuario, log_detalhes=detalhes)
    
    def to_dict(self):
        """
        Converte o log em um dicionário.
        
        Returns:
            dict: Representação em dicionário do log
        """
        return {
            "log_uuid": self.log_uuid,
            "log_timestamp": self.log_timestamp.timestamp() if self.log_timestamp else None,
            "log_tipo": self.log_tipo,
            "log_mensagem": self.log_mensagem,
            "log_usuario": self.log_usuario,
            "log_detalhes": self.log_detalhes
        }