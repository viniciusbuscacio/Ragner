#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
DOCX Loader: Carrega e processa arquivos DOCX.
"""

import os
from docx import Document as DocxDocument
from domain.Documento import Documento
from domain.Chunk import Chunk
from presentation.cli.cli_cores import Cores

class DocxLoader:
    """
    Carrega e processa arquivos DOCX.
    
    Esta classe é responsável por extrair o texto de arquivos DOCX
    e dividi-lo em chunks para processamento posterior.
    """
    
    def __init__(self, tamanho_chunk=1000, sobreposicao=200):
        """
        Inicializa o loader de DOCX.
        
        Args:
            tamanho_chunk: Tamanho aproximado de cada chunk em caracteres
            sobreposicao: Número de caracteres de sobreposição entre chunks
        """
        self.tamanho_chunk = tamanho_chunk
        self.sobreposicao = sobreposicao
    
    def carregar(self, caminho_arquivo):
        """
        Carrega e processa um arquivo DOCX.
        
        Args:
            caminho_arquivo: Caminho para o arquivo DOCX
            
        Returns:
            list: Lista de textos dos chunks extraídos do DOCX
            
        Raises:
            Exception: Se ocorrer um erro ao processar o arquivo
        """
        try:
            # Extrai o texto do DOCX
            texto_completo = self._extrair_texto(caminho_arquivo)
            
            # Divide o texto em chunks
            chunks = self._dividir_em_chunks(texto_completo)
            
            print(f"{Cores.CINZA}DOCX carregado: {os.path.basename(caminho_arquivo)}, {len(chunks)} chunks extraídos{Cores.RESET}")
                
            return chunks
        
        except Exception as e:
            print(f"Erro ao carregar DOCX {caminho_arquivo}: {str(e)}")
            import traceback
            print(traceback.format_exc())
            raise
    
    def _extrair_texto(self, caminho_arquivo):
        """
        Extrai o texto completo de um arquivo DOCX.
        
        Args:
            caminho_arquivo: Caminho para o arquivo DOCX
            
        Returns:
            str: Texto extraído do DOCX
        """
        texto = ""
        
        try:
            doc = DocxDocument(caminho_arquivo)
            
            # Extrai texto de parágrafos
            for paragrafo in doc.paragraphs:
                if paragrafo.text:
                    texto += paragrafo.text + "\n\n"
            
            # Extrai texto de tabelas
            for tabela in doc.tables:
                for linha in tabela.rows:
                    linha_texto = []
                    for celula in linha.cells:
                        if celula.text:
                            linha_texto.append(celula.text)
                    if linha_texto:
                        texto += " | ".join(linha_texto) + "\n"
                texto += "\n"
        
        except Exception as e:
            print(f"Erro ao extrair texto do DOCX {caminho_arquivo}: {str(e)}")
            raise
        
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
        
        try:
            for paragrafo in paragrafos:
                # Se o parágrafo for muito grande, divide-o
                if len(paragrafo) > self.tamanho_chunk:
                    # Adiciona o chunk atual se não estiver vazio
                    if chunk_atual:
                        chunks.append(chunk_atual)
                        chunk_atual = ""
                    
                    # Divide o parágrafo grande em chunks menores
                    j = 0
                    contador_seguranca = 0  # Contador de segurança para prevenir loop infinito
                    max_iteracoes = 1000    # Número máximo de iterações permitidas

                    while j < len(paragrafo) and contador_seguranca < max_iteracoes:
                        fim = min(j + self.tamanho_chunk, len(paragrafo))
                        chunk_part = paragrafo[j:fim]
                        chunks.append(chunk_part)
                        
                        # Verificação crucial para evitar loop infinito
                        j_anterior = j
                        j = fim - self.sobreposicao
                        
                        if j <= j_anterior:  # Se não avançamos, forçamos o avanço
                            j = j_anterior + max(1, fim//10)  # Avançar pelo menos 1 caractere ou 10% do tamanho
                        
                        contador_seguranca += 1
                    
                    if contador_seguranca >= max_iteracoes:
                        # Adicionar o resto do parágrafo como um único chunk
                        chunks.append(paragrafo[j:])
                
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
            
        except Exception as e:
            print(f"Erro na divisão em chunks: {str(e)}")
            # Em caso de erro, retorna o texto completo como um único chunk
            chunks = [texto]
        
        return chunks