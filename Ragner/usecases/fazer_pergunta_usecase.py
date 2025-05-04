#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Caso de uso: Processar uma pergunta do usuário.
"""

from domain.Pergunta import Pergunta
from presentation.cli.cli_logger import CLILogger

# Inicializa o logger para a interface CLI
cli_logger = CLILogger()


class FazerPerguntaUseCase:
    """
    Caso de uso para processar uma pergunta do usuário.
    
    Esta classe é responsável por processar a pergunta do usuário,
    criar um objeto Pergunta e prepará-lo para busca de contexto e geração de resposta.
    """
    
    def __init__(self):
        """
        Inicializa o caso de uso.
        """
        pass
    
    def executar(self, texto_pergunta, language_model):
        """
        Processa uma pergunta do usuário.
        
        Args:
            texto_pergunta: Texto da pergunta
            language_model: Gateway para o modelo de linguagem
            
        Returns:
            tuple: (Objeto Pergunta, embedding da pergunta)
        """
        # Cria o objeto Pergunta
        pergunta = Pergunta(texto=texto_pergunta)
        
        # Gera o embedding da pergunta
        try:
            embedding = language_model.gerar_embedding(texto_pergunta)
            pergunta.embedding = embedding
            return pergunta, embedding
        
        except Exception as e:
            cli_logger.registrar_info(f"Erro ao gerar embedding para pergunta: {str(e)}")
            return pergunta, None
    
    def analisar_comando(self, texto):
        """
        Analisa se o texto é um comando especial.
        
        Args:
            texto: Texto da entrada do usuário
            
        Returns:
            tuple: (bool é_comando, str comando, str argumento)
        """
        texto = texto.strip().lower()
        
        # Comandos sem argumentos
        comandos_simples = [
            "sobre", "tutorial", "status", "status_tabela_arquivos", 
            "status_tabela_chunks", "status_faiss", "menu", "sair",
            "recarregar_arquivos_da_pasta", "apagar_tudo", "configurar_api_key",
            "reconstruir_indice_faiss", "teste_vetor"
        ]
        
        for comando in comandos_simples:
            if texto == comando:
                return True, comando, None
        
        # Comandos com argumentos
        if texto.startswith("indice "):
            partes = texto.split(" ", 1)
            if len(partes) > 1:
                return True, "indice", partes[1]
        
        # Verificar se é o comando teste_vetor com argumento
        if texto.startswith("teste_vetor "):
            partes = texto.split(" ", 1)
            if len(partes) > 1:
                return True, "teste_vetor", partes[1]
        
        # Não é um comando
        return False, None, None