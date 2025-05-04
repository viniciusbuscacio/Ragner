#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Testes unitários para a classe DadosRaw.
"""

import unittest
import os
import sys
from datetime import datetime

# Adiciona o diretório raiz ao caminho para poder importar os módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Ragner.domain.DadosRaw import DadosRaw

class TestDadosRaw(unittest.TestCase):
    """
    Classe de testes para DadosRaw.
    """
    
    def setUp(self):
        """
        Configuração inicial para os testes.
        """
        self.raw_uuid = "test-uuid-123"
        self.arquivo_uuid = "arquivo-uuid-456"
        self.raw_conteudo = b"conteudo de teste em bytes"
        self.test_data = datetime.now()
        
    def test_criar_dados_raw(self):
        """
        Testa a criação de um objeto DadosRaw.
        """
        dados_raw = DadosRaw(
            raw_uuid=self.raw_uuid, 
            arquivo_uuid=self.arquivo_uuid, 
            raw_conteudo=self.raw_conteudo, 
            data_armazenamento=self.test_data
        )
        
        self.assertEqual(dados_raw.raw_uuid, self.raw_uuid)
        self.assertEqual(dados_raw.arquivo_uuid, self.arquivo_uuid)
        self.assertEqual(dados_raw.raw_conteudo, self.raw_conteudo)
        self.assertEqual(dados_raw.data_armazenamento, self.test_data)
    
    def test_criar_dados_raw_sem_data(self):
        """
        Testa a criação de um objeto DadosRaw sem fornecer data de armazenamento.
        """
        dados_raw = DadosRaw(
            raw_uuid=self.raw_uuid, 
            arquivo_uuid=self.arquivo_uuid, 
            raw_conteudo=self.raw_conteudo
        )
        
        self.assertEqual(dados_raw.raw_uuid, self.raw_uuid)
        self.assertEqual(dados_raw.arquivo_uuid, self.arquivo_uuid)
        self.assertEqual(dados_raw.raw_conteudo, self.raw_conteudo)
        self.assertIsNotNone(dados_raw.data_armazenamento)
        self.assertIsInstance(dados_raw.data_armazenamento, datetime)
    
    def test_str_representation(self):
        """
        Testa a representação em string do objeto DadosRaw.
        """
        dados_raw = DadosRaw(
            raw_uuid=self.raw_uuid, 
            arquivo_uuid=self.arquivo_uuid, 
            raw_conteudo=self.raw_conteudo
        )
        
        str_rep = str(dados_raw)
        self.assertIn(self.raw_uuid, str_rep)
        self.assertIn(self.arquivo_uuid, str_rep)
        self.assertIn(str(len(self.raw_conteudo)), str_rep)
    
    def test_to_dict(self):
        """
        Testa a conversão do objeto DadosRaw para dicionário.
        """
        dados_raw = DadosRaw(
            raw_uuid=self.raw_uuid, 
            arquivo_uuid=self.arquivo_uuid, 
            raw_conteudo=self.raw_conteudo,
            data_armazenamento=self.test_data
        )
        
        dict_rep = dados_raw.to_dict()
        self.assertEqual(dict_rep["raw_uuid"], self.raw_uuid)
        self.assertEqual(dict_rep["arquivo_uuid"], self.arquivo_uuid)
        self.assertEqual(dict_rep["data_armazenamento"], self.test_data.timestamp())


if __name__ == '__main__':
    unittest.main()