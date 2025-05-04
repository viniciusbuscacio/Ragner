#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Caso de uso: Gerar resposta para uma pergunta com base no contexto.
"""

from domain.Resposta import Resposta
from presentation.cli.cli_logger import CLILogger

# Inicializa o logger para a interface CLI
cli_logger = CLILogger()


class GerarRespostaUseCase:
    """
    Caso de uso para gerar resposta para uma pergunta com base no contexto.
    
    Esta classe é responsável por enviar a pergunta e o contexto para o modelo de linguagem
    e processar a resposta gerada.
    """
    
    def __init__(self, language_model):
        """
        Inicializa o caso de uso.
        
        Args:
            language_model: Gateway para o modelo de linguagem
        """
        self.language_model = language_model
    
    def executar(self, pergunta, chunks_relevantes):
        """
        Gera uma resposta para a pergunta com base no contexto dos chunks relevantes.
        
        Args:
            pergunta: Objeto Pergunta
            chunks_relevantes: Lista de chunks relevantes com seus documentos
            
        Returns:
            Resposta: Objeto com a resposta gerada
        """
        try:
            # Formata o contexto para o prompt
            contexto = self._formatar_contexto(chunks_relevantes)
            
            # Identifica os documentos disponíveis para citação
            documentos_disponiveis = set()
            for item in chunks_relevantes:
                documentos_disponiveis.add(item["documento"].arquivo_nome)
            
            # Define o prompt para o sistema, incluindo os documentos disponíveis
            documentos_lista = ", ".join(documentos_disponiveis)
            system_prompt = (
                "Você é um assistente chamado Ragner, que utiliza a técnica RAG para explica conceitos com base nas informações fornecidas. "
                "Responda à pergunta do usuário usando apenas as informações dos trechos de documentos fornecidos. "
                "Se a resposta não estiver nos trechos ou se você não tiver certeza, indique isso claramente. "
                "Se uma informação vem claramente de uma fonte específica, cite-a. "
                "Se múltiplos documentos contêm a mesma informação, cite apenas a fonte mais relevante. "
                "Seja preciso e direto nas suas respostas."
            )
            
            # Gera a resposta usando o modelo de linguagem
            texto_resposta = self.language_model.gerar_resposta(
                pergunta=pergunta.texto, 
                contexto=contexto,
                system_prompt=system_prompt
            )
            
            # Cria e retorna o objeto Resposta
            resposta = Resposta(
                texto=texto_resposta,
                pergunta_id=pergunta.id,
                pergunta=pergunta
            )
            
            # Adiciona os chunks utilizados
            for item in chunks_relevantes:
                resposta.adicionar_chunk(item["chunk"])
            
            return resposta
        
        except Exception as e:
            cli_logger.registrar_info(f"Erro ao gerar resposta: {str(e)}")
            # Retorna uma resposta de erro
            return Resposta(
                texto=f"Desculpe, ocorreu um erro ao gerar a resposta: {str(e)}",
                pergunta_id=pergunta.id,
                pergunta=pergunta
            )
    
    def _formatar_contexto(self, chunks_relevantes):
        """
        Formata os chunks relevantes em um texto para o contexto do modelo.
        
        Args:
            chunks_relevantes: Lista de dicionários com chunks e documentos
            
        Returns:
            str: Texto formatado para o contexto
        """
        if not chunks_relevantes:
            return "Nenhuma informação relevante foi encontrada para esta pergunta."
        
        contexto = ""
        
        for i, item in enumerate(chunks_relevantes):
            chunk = item["chunk"]
            documento = item["documento"]
            
            contexto += f"Trecho {i+1} (de {documento.arquivo_nome}):\n{chunk.chunk_texto}\n\n"
        
        return contexto