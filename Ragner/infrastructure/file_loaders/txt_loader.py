#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
TXT Loader: Carrega e processa arquivos de texto.
"""

import os

class TXTLoader:
    """
    Carrega e processa arquivos de texto.
    
    Esta classe é responsável por extrair o conteúdo de arquivos TXT
    e dividi-lo em chunks para processamento posterior.
    """
    
    def __init__(self, tamanho_chunk=1000, sobreposicao=200, logger=None):
        """
        Inicializa o loader de texto.
        
        Args:
            tamanho_chunk: Tamanho aproximado de cada chunk em caracteres
            sobreposicao: Número de caracteres de sobreposição entre chunks
            logger: Interface opcional para registrar mensagens e eventos
        """
        self.tamanho_chunk = tamanho_chunk
        self.sobreposicao = sobreposicao
        self.logger = logger
    
    def carregar(self, caminho_arquivo):
        """
        Carrega e processa um arquivo de texto.
        
        Args:
            caminho_arquivo: Caminho para o arquivo de texto
            
        Returns:
            list: Lista de textos dos chunks extraídos do arquivo
            
        Raises:
            Exception: Se ocorrer um erro ao processar o arquivo
        """
        try:
            # Lê o texto do arquivo
            with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
                texto_completo = arquivo.read()
            
            # Divide o texto em chunks
            chunks = self._dividir_em_chunks(texto_completo)
            
            # Notifica sobre o processamento do arquivo usando o logger se disponível
            # Log removido para evitar duplicação no terminal
            return chunks
        
        except Exception as e:
            if self.logger:
                self.logger.registrar_erro(f"Erro ao carregar arquivo TXT {caminho_arquivo}: {str(e)}")
            raise
    
    def _dividir_em_chunks(self, texto):
        """
        Divide o texto em chunks de tamanho aproximado.
        
        Args:
            texto: Texto completo a ser dividido
            
        Returns:
            list: Lista de chunks de texto
        """
        chunks = []
        
        # Se o texto for menor que o tamanho do chunk, retorna como um único chunk
        if len(texto) <= self.tamanho_chunk:
            chunks.append(texto)
            return chunks
        
        # Divide o texto em parágrafos
        paragrafos = texto.split('\n')
        chunk_atual = ""
        
        for paragrafo in paragrafos:
            # Se o parágrafo for muito grande, divide-o
            if len(paragrafo) > self.tamanho_chunk:
                # Adiciona o chunk atual se não estiver vazio
                if chunk_atual:
                    chunks.append(chunk_atual)
                    chunk_atual = ""
                
                # Divide o parágrafo grande em chunks menores
                i = 0
                while i < len(paragrafo):
                    fim = min(i + self.tamanho_chunk, len(paragrafo))
                    chunks.append(paragrafo[i:fim])
                    i = fim - self.sobreposicao
                    if i < 0:
                        i = 0
            
            # Se adicionar o parágrafo ao chunk atual exceder o tamanho máximo
            elif len(chunk_atual) + len(paragrafo) + 1 > self.tamanho_chunk:
                # Adiciona o chunk atual e começa um novo
                chunks.append(chunk_atual)
                chunk_atual = paragrafo
            
            # Caso contrário, adiciona o parágrafo ao chunk atual
            else:
                if chunk_atual:
                    chunk_atual += "\n"
                chunk_atual += paragrafo
        
        # Adiciona o último chunk se não estiver vazio
        if chunk_atual:
            chunks.append(chunk_atual)
        
        return chunks