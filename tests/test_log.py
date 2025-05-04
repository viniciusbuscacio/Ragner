#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Testes unitários para a classe Log.
"""

import unittest
import os
import sys
from datetime import datetime

# Adiciona o diretório raiz ao caminho para poder importar os módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Ragner.domain.Log import Log, Logger

class TestLog(unittest.TestCase):
    """
    Classe de testes para Log.
    """
    
    def setUp(self):
        """
        Configuração inicial para os testes.
        """
        self.log_uuid = "test-log-uuid-123"
        self.log_timestamp = datetime.now()
        self.log_tipo = "INFO"
        self.log_mensagem = "Mensagem de teste"
        self.log_usuario = "usuario_teste"
        self.log_detalhes = "Detalhes adicionais do teste"
        
    def test_criar_log(self):
        """
        Testa a criação de um objeto Log.
        """
        log = Log(
            log_uuid=self.log_uuid,
            log_timestamp=self.log_timestamp,
            log_tipo=self.log_tipo,
            log_mensagem=self.log_mensagem,
            log_usuario=self.log_usuario,
            log_detalhes=self.log_detalhes
        )
        
        self.assertEqual(log.log_uuid, self.log_uuid)
        self.assertEqual(log.log_timestamp, self.log_timestamp)
        self.assertEqual(log.log_tipo, self.log_tipo)
        self.assertEqual(log.log_mensagem, self.log_mensagem)
        self.assertEqual(log.log_usuario, self.log_usuario)
        self.assertEqual(log.log_detalhes, self.log_detalhes)
    
    def test_criar_log_sem_timestamp(self):
        """
        Testa a criação de um objeto Log sem fornecer timestamp.
        """
        log = Log(
            log_uuid=self.log_uuid,
            log_tipo=self.log_tipo,
            log_mensagem=self.log_mensagem
        )
        
        self.assertEqual(log.log_uuid, self.log_uuid)
        self.assertEqual(log.log_tipo, self.log_tipo)
        self.assertEqual(log.log_mensagem, self.log_mensagem)
        self.assertIsNotNone(log.log_timestamp)
        self.assertIsInstance(log.log_timestamp, datetime)
    
    def test_str_representation(self):
        """
        Testa a representação em string do objeto Log.
        """
        log = Log(
            log_uuid=self.log_uuid,
            log_tipo=self.log_tipo,
            log_mensagem=self.log_mensagem
        )
        
        str_rep = str(log)
        self.assertIn(self.log_uuid, str_rep)
        self.assertIn(self.log_tipo, str_rep)
        self.assertIn(self.log_mensagem, str_rep)
    
    def test_to_dict(self):
        """
        Testa a conversão do objeto Log para dicionário.
        """
        log = Log(
            log_uuid=self.log_uuid,
            log_timestamp=self.log_timestamp,
            log_tipo=self.log_tipo,
            log_mensagem=self.log_mensagem,
            log_usuario=self.log_usuario,
            log_detalhes=self.log_detalhes
        )
        
        dict_rep = log.to_dict()
        self.assertEqual(dict_rep["log_uuid"], self.log_uuid)
        self.assertEqual(dict_rep["log_timestamp"], self.log_timestamp.timestamp())
        self.assertEqual(dict_rep["log_tipo"], self.log_tipo)
        self.assertEqual(dict_rep["log_mensagem"], self.log_mensagem)
        self.assertEqual(dict_rep["log_usuario"], self.log_usuario)
        self.assertEqual(dict_rep["log_detalhes"], self.log_detalhes)
    
    def test_create_info_log(self):
        """
        Testa o método de classe para criar log de tipo INFO.
        """
        mensagem = "Mensagem de informação"
        usuario = "usuario_teste"
        detalhes = "Detalhes da informação"
        
        log = Log.info(mensagem=mensagem, usuario=usuario, detalhes=detalhes)
        
        self.assertEqual(log.log_tipo, "INFO")
        self.assertEqual(log.log_mensagem, mensagem)
        self.assertEqual(log.log_usuario, usuario)
        self.assertEqual(log.log_detalhes, detalhes)
    
    def test_create_warning_log(self):
        """
        Testa o método de classe para criar log de tipo WARNING.
        """
        mensagem = "Mensagem de aviso"
        usuario = "usuario_teste"
        detalhes = "Detalhes do aviso"
        
        log = Log.warning(mensagem=mensagem, usuario=usuario, detalhes=detalhes)
        
        self.assertEqual(log.log_tipo, "WARNING")
        self.assertEqual(log.log_mensagem, mensagem)
        self.assertEqual(log.log_usuario, usuario)
        self.assertEqual(log.log_detalhes, detalhes)
    
    def test_create_error_log(self):
        """
        Testa o método de classe para criar log de tipo ERROR.
        """
        mensagem = "Mensagem de erro"
        usuario = "usuario_teste"
        detalhes = "Detalhes do erro"
        
        log = Log.error(mensagem=mensagem, usuario=usuario, detalhes=detalhes)
        
        self.assertEqual(log.log_tipo, "ERROR")
        self.assertEqual(log.log_mensagem, mensagem)
        self.assertEqual(log.log_usuario, usuario)
        self.assertEqual(log.log_detalhes, detalhes)


class MockLogger(Logger):
    """
    Implementação mock da interface Logger para testes.
    """
    def __init__(self):
        self.info_logs = []
        self.error_logs = []
        self.debug_logs = []
        
    def registrar_info(self, mensagem):
        self.info_logs.append(mensagem)
        
    def registrar_erro(self, mensagem):
        self.error_logs.append(mensagem)
        
    def registrar_debug(self, mensagem):
        self.debug_logs.append(mensagem)


class TestLogger(unittest.TestCase):
    """
    Classe de testes para a interface Logger.
    """
    
    def setUp(self):
        """
        Configuração inicial para os testes.
        """
        self.mock_logger = MockLogger()
        
    def test_registrar_info(self):
        """
        Testa o registro de mensagens informativas.
        """
        mensagem = "Mensagem de informação de teste"
        self.mock_logger.registrar_info(mensagem)
        
        self.assertEqual(len(self.mock_logger.info_logs), 1)
        self.assertEqual(self.mock_logger.info_logs[0], mensagem)
        
    def test_registrar_erro(self):
        """
        Testa o registro de mensagens de erro.
        """
        mensagem = "Mensagem de erro de teste"
        self.mock_logger.registrar_erro(mensagem)
        
        self.assertEqual(len(self.mock_logger.error_logs), 1)
        self.assertEqual(self.mock_logger.error_logs[0], mensagem)
        
    def test_registrar_debug(self):
        """
        Testa o registro de mensagens de debug.
        """
        mensagem = "Mensagem de debug de teste"
        self.mock_logger.registrar_debug(mensagem)
        
        self.assertEqual(len(self.mock_logger.debug_logs), 1)
        self.assertEqual(self.mock_logger.debug_logs[0], mensagem)


if __name__ == '__main__':
    unittest.main()