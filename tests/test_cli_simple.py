#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Testes simplificados para o Ragner Chatbot.
"""

import unittest
from unittest.mock import MagicMock, patch
import sys
import os

class TestRagnerSimple(unittest.TestCase):
    """
    Testes simples para verificar a estrutura básica do projeto Ragner.
    """
    
    def setUp(self):
        """
        Configuração para os testes.
        """
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    def test_estrutura_projeto(self):
        """
        Verifica se os diretórios e arquivos principais do projeto existem.
        """
        # Verifica se os diretórios principais existem
        diretorios = [
            os.path.join(self.base_dir, "Ragner"),
            os.path.join(self.base_dir, "Ragner", "domain"),
            os.path.join(self.base_dir, "Ragner", "presentation"),
            os.path.join(self.base_dir, "Ragner", "usecases"),
            os.path.join(self.base_dir, "Ragner", "infrastructure")
        ]
        
        for diretorio in diretorios:
            self.assertTrue(os.path.exists(diretorio), f"Diretório {diretorio} não encontrado")
            self.assertTrue(os.path.isdir(diretorio), f"{diretorio} não é um diretório")
        
        # Verifica se os arquivos principais existem
        arquivos = [
            os.path.join(self.base_dir, "Ragner", "Ragner.py"),
            os.path.join(self.base_dir, "Ragner", "presentation", "cli", "cli_interface.py"),
            os.path.join(self.base_dir, "Ragner", "presentation", "cli", "controllers.py")
        ]
        
        for arquivo in arquivos:
            self.assertTrue(os.path.exists(arquivo), f"Arquivo {arquivo} não encontrado")
            self.assertTrue(os.path.isfile(arquivo), f"{arquivo} não é um arquivo")
    
    def test_verificar_arquivos_domain(self):
        """
        Verifica a existência dos arquivos principais no domínio.
        """
        arquivos_domain = [
            "Chunk.py",
            "Documento.py",
            "Embedding.py",
            "Pergunta.py",
            "Resposta.py",
            "DadosRaw.py",  # Adicionado
            "Log.py"        # Adicionado
        ]
        
        for arquivo in arquivos_domain:
            caminho = os.path.join(self.base_dir, "Ragner", "domain", arquivo)
            self.assertTrue(os.path.exists(caminho), f"Arquivo {arquivo} não encontrado no domínio")
            self.assertTrue(os.path.isfile(caminho), f"{caminho} não é um arquivo")
    
    def test_verificar_repositories_domain(self):
        """
        Verifica a existência da pasta repositories e seus arquivos no domínio.
        """
        # Verifica se a pasta repositories existe
        caminho_repositories = os.path.join(self.base_dir, "Ragner", "domain", "repositories")
        self.assertTrue(os.path.exists(caminho_repositories), "Pasta repositories não encontrada no domínio")
        self.assertTrue(os.path.isdir(caminho_repositories), f"{caminho_repositories} não é um diretório")
        
        # Verifica se contém o arquivo ChunkRepository.py
        caminho_arquivo = os.path.join(caminho_repositories, "ChunkRepository.py")
        self.assertTrue(os.path.exists(caminho_arquivo), "Arquivo ChunkRepository.py não encontrado")
        self.assertTrue(os.path.isfile(caminho_arquivo), f"{caminho_arquivo} não é um arquivo")
    
    def test_verificar_arquivos_usecases(self):
        """
        Verifica a existência dos arquivos principais de casos de uso.
        """
        arquivos_usecases = [
            "buscar_contexto_usecase.py",
            "configurar_api_key_usecase.py",
            "fazer_pergunta_usecase.py",
            "gerar_resposta_usecase.py",
            "indexar_documentos_usecase.py",
            "tutorial_usecase.py"  # Adicionado
        ]
        
        for arquivo in arquivos_usecases:
            caminho = os.path.join(self.base_dir, "Ragner", "usecases", arquivo)
            self.assertTrue(os.path.exists(caminho), f"Arquivo {arquivo} não encontrado nos casos de uso")
            self.assertTrue(os.path.isfile(caminho), f"{caminho} não é um arquivo")
    
    def test_verificar_pastas_infrastructure(self):
        """
        Verifica a existência das pastas principais de infraestrutura.
        """
        pastas_infrastructure = [
            "database",
            "file_loaders",
            "language_model",
            "vector_store"
        ]
        
        for pasta in pastas_infrastructure:
            caminho = os.path.join(self.base_dir, "Ragner", "infrastructure", pasta)
            self.assertTrue(os.path.exists(caminho), f"Pasta {pasta} não encontrada na infraestrutura")
            self.assertTrue(os.path.isdir(caminho), f"{caminho} não é um diretório")


if __name__ == '__main__':
    unittest.main()