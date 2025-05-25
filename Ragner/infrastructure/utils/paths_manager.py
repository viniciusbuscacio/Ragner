#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Gerenciador de caminhos da aplicação.
Este módulo centraliza a lógica de gerenciamento de caminhos da aplicação,
garantindo que todos os arquivos sejam armazenados no mesmo local do executável.
"""

import os
import sys

class PathsManager:
    """
    Gerencia os caminhos da aplicação.
    
    Esta classe fornece métodos para obter os caminhos das pastas
    da aplicação, garantindo que todos os arquivos sejam armazenados
    no mesmo local do executável.
    """
    
    _instance = None
    _base_dir = None
    _documentos_dir = None
    _database_dir = None
    _faiss_index_dir = None
    
    def __new__(cls):
        """
        Implementa o padrão Singleton para garantir uma única instância.
        """
        if cls._instance is None:
            cls._instance = super(PathsManager, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        """
        Inicializa os caminhos da aplicação.
        """
        # Define o nome da aplicação - usando uma constante para garantir consistência
        APP_NAME = "Ragner"
        
        # Determinar o diretório base da aplicação
        if getattr(sys, 'frozen', False):
            # Se estamos em um executável PyInstaller
            # Para aplicações instaladas, usamos AppData\Local\APP_NAME
            self._base_dir = os.path.join(os.environ.get('LOCALAPPDATA', os.path.expanduser('~')), APP_NAME)
        else:
            # Se estamos em desenvolvimento
            current_dir = os.path.dirname(os.path.abspath(__file__))
            # Volta três níveis para chegar ao diretório raiz do projeto
            self._base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(current_dir))))
        
        # Definir os caminhos das pastas da aplicação
        self._documentos_dir = os.path.join(self._base_dir, "documentos")
        self._database_dir = os.path.join(self._base_dir, "database")
        self._faiss_index_dir = os.path.join(self._base_dir, "faiss_index")
        
        # Garantir que todas as pastas existam
        self._ensure_directories_exist()
    
    def _ensure_directories_exist(self):
        """
        Garante que todas as pastas da aplicação existam.
        """
        directories = [
            self._base_dir,  # Garante que o diretório base existe primeiro
            self._documentos_dir,
            self._database_dir,
            self._faiss_index_dir
        ]
        
        for directory in directories:
            if not os.path.exists(directory):
                os.makedirs(directory)
    
    @property
    def base_dir(self):
        """Retorna o diretório base da aplicação."""
        return self._base_dir
    
    @property
    def documentos_dir(self):
        """Retorna o diretório de documentos."""
        return self._documentos_dir
    
    @property
    def database_dir(self):
        """Retorna o diretório do banco de dados."""
        return self._database_dir
    
    @property
    def database_path(self):
        """Retorna o caminho completo para o arquivo do banco de dados."""
        return os.path.join(self._database_dir, "database.sqlite3")
    
    @property
    def faiss_index_dir(self):
        """Retorna o diretório do índice FAISS."""
        return self._faiss_index_dir
    
    @property
    def faiss_index_path(self):
        """Retorna o caminho completo para o arquivo do índice FAISS."""
        return os.path.join(self._faiss_index_dir, "faiss_index.bin")
    
    @property
    def id_mapping_path(self):
        """Retorna o caminho completo para o arquivo de mapeamento de IDs."""
        return os.path.join(self._faiss_index_dir, "id_mapping.pkl")