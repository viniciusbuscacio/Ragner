#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
PDF Loader: Carrega e processa arquivos PDF.
"""

import os
import PyPDF2
from domain.Documento import Documento
from domain.Chunk import Chunk
from presentation.cli.cli_cores import Cores

class PDFLoader:
    """
    Carrega e processa arquivos PDF.
    
    Esta classe é responsável por extrair o texto de arquivos PDF
    e dividi-lo em chunks para processamento posterior.
    """
    
    def __init__(self, tamanho_chunk=1000, sobreposicao=200):
        """
        Inicializa o loader de PDF.
        
        Args:
            tamanho_chunk: Tamanho aproximado de cada chunk em caracteres
            sobreposicao: Número de caracteres de sobreposição entre chunks
        """
        self.tamanho_chunk = tamanho_chunk
        self.sobreposicao = sobreposicao
    
    def carregar(self, caminho_arquivo):
        """
        Carrega e processa um arquivo PDF.
        
        Args:
            caminho_arquivo: Caminho para o arquivo PDF
            
        Returns:
            list: Lista de textos dos chunks extraídos do PDF
            
        Raises:
            Exception: Se ocorrer um erro ao processar o arquivo
        """
        try:
            # Extrai o texto do PDF
            texto_completo = self._extrair_texto(caminho_arquivo)
            
            # Divide o texto em chunks
            chunks = self._dividir_em_chunks(texto_completo)
            
            print(f"{Cores.CINZA}PDF carregado: {os.path.basename(caminho_arquivo)}, {len(chunks)} chunks extraídos{Cores.RESET}")
            return chunks
        
        except Exception as e:
            print(f"Erro ao carregar PDF {caminho_arquivo}: {str(e)}")
            raise
    
    def _extrair_texto(self, caminho_arquivo):
        """
        Extrai o texto completo de um arquivo PDF.
        
        Args:
            caminho_arquivo: Caminho para o arquivo PDF
            
        Returns:
            str: Texto extraído do PDF
        """
        texto = ""
        
        with open(caminho_arquivo, 'rb') as arquivo:
            leitor = PyPDF2.PdfReader(arquivo)
            
            # Percorre todas as páginas e extrai o texto
            for pagina in leitor.pages:
                texto_pagina = pagina.extract_text()
                if texto_pagina:
                    texto += texto_pagina + "\n\n"
        
        return texto
    
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