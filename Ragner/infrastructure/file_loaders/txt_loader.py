#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
TXT Loader: Carrega e processa arquivos TXT.
"""

import os
from domain.Documento import Documento
from domain.Chunk import Chunk
from presentation.cli.cli_cores import Cores

class TxtLoader:
    """
    Carrega e processa arquivos TXT.
    
    Esta classe é responsável por extrair o texto de arquivos TXT
    e dividi-lo em chunks para processamento posterior.
    """
    
    def __init__(self, tamanho_chunk=1000, sobreposicao=200):
        """
        Inicializa o loader de TXT.
        
        Args:
            tamanho_chunk: Tamanho aproximado de cada chunk em caracteres
            sobreposicao: Número de caracteres de sobreposição entre chunks
        """
        self.tamanho_chunk = tamanho_chunk
        self.sobreposicao = sobreposicao
    
    def carregar(self, caminho_arquivo):
        """
        Carrega e processa um arquivo TXT.
        
        Args:
            caminho_arquivo: Caminho para o arquivo TXT
            
        Returns:
            list: Lista de textos de chunks
            
        Raises:
            Exception: Se ocorrer um erro ao processar o arquivo
        """
        try:
            # Lê o conteúdo do arquivo
            with open(caminho_arquivo, 'r', encoding='utf-8', errors='ignore') as arquivo:
                texto_completo = arquivo.read()
            
            # Divide o texto em chunks
            chunks_texto = self._dividir_em_chunks(texto_completo)
            
            print(f"{Cores.CINZA}TXT carregado: {os.path.basename(caminho_arquivo)}, {len(chunks_texto)} chunks criados{Cores.RESET}")
            return chunks_texto
        
        except Exception as e:
            print(f"Erro ao carregar TXT {caminho_arquivo}: {str(e)}")
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