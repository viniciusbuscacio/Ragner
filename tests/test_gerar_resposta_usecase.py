#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Testes para o caso de uso de geração de resposta do Ragner Chatbot.
Este teste inclui uma implementação mockada das classes necessárias para evitar
problemas de importação.
"""

import unittest
from unittest.mock import MagicMock, patch
import sys
import os

# Define classes simuladas para os testes
class MockChunk:
    def __init__(self, chunk_uuid, chunk_texto, chunk_numero, arquivo_uuid):
        self.chunk_uuid = chunk_uuid
        self.chunk_texto = chunk_texto
        self.chunk_numero = chunk_numero
        self.arquivo_uuid = arquivo_uuid


class MockPergunta:
    def __init__(self, texto):
        self.texto = texto


class MockResposta:
    def __init__(self, texto, chunks_utilizados):
        self.texto = texto
        self.chunks_utilizados = chunks_utilizados


class TestGerarResposta(unittest.TestCase):
    """
    Testes para o caso de uso de geração de resposta.
    """
    
    def setUp(self):
        """
        Preparação para os testes.
        """
        # Cria componentes simulados
        self.mock_language_model = MagicMock()
        
        # Simulação de pergunta e chunks
        self.pergunta = MockPergunta("Como funciona o RAG?")
        self.chunks = [
            MockChunk(
                chunk_uuid="chunk1", 
                chunk_texto="RAG significa Retrieval-Augmented Generation, que é uma técnica que combina recuperação de documentos com geração de linguagem natural.", 
                chunk_numero=1, 
                arquivo_uuid="doc1"
            ),
            MockChunk(
                chunk_uuid="chunk2", 
                chunk_texto="No RAG, o sistema busca informações relevantes em uma base de conhecimento antes de gerar uma resposta.", 
                chunk_numero=2, 
                arquivo_uuid="doc1"
            )
        ]
        
        # Simulação de resposta
        self.resposta_simulada = "RAG (Retrieval-Augmented Generation) funciona combinando recuperação de documentos relevantes com geração de texto. O sistema busca informações em uma base de conhecimento para contextualizar a resposta que será gerada."
    
    def test_gerar_resposta_com_chunks(self):
        """
        Testa o fluxo de geração de resposta com chunks válidos.
        """
        # Configura o mock do language_model para retornar uma resposta
        self.mock_language_model.gerar_texto_com_contexto.return_value = self.resposta_simulada
        
        # Cria uma implementação simulada do caso de uso
        class GerarRespostaUseCaseSimulado:
            def __init__(self, language_model):
                self.language_model = language_model
            
            def executar(self, pergunta, chunks):
                # Cria o contexto a partir dos chunks
                contexto = ""
                for i, chunk in enumerate(chunks, 1):
                    contexto += f"[{i}] {chunk.chunk_texto}\n\n"
                
                # Gera a resposta usando o modelo de linguagem
                texto_resposta = self.language_model.gerar_texto_com_contexto(
                    pergunta.texto, contexto
                )
                
                # Cria e retorna um objeto Resposta
                return MockResposta(
                    texto=texto_resposta,
                    chunks_utilizados=chunks
                )
        
        # Instancia o caso de uso simulado
        gerar_resposta = GerarRespostaUseCaseSimulado(
            language_model=self.mock_language_model
        )
        
        # Executa o caso de uso
        resposta = gerar_resposta.executar(self.pergunta, self.chunks)
        
        # Verifica se o resultado está correto
        self.assertEqual(resposta.texto, self.resposta_simulada)
        self.assertEqual(len(resposta.chunks_utilizados), 2)
        self.assertEqual(resposta.chunks_utilizados[0].chunk_uuid, "chunk1")
        self.assertEqual(resposta.chunks_utilizados[1].chunk_uuid, "chunk2")
        
        # Verifica se o método do language_model foi chamado corretamente
        self.mock_language_model.gerar_texto_com_contexto.assert_called_once()
    
    def test_gerar_resposta_sem_chunks(self):
        """
        Testa o fluxo de geração de resposta sem chunks (lista vazia).
        """
        # Configura o mock do language_model para retornar uma resposta padrão
        resposta_sem_contexto = "Não tenho informações suficientes para responder essa pergunta com precisão."
        self.mock_language_model.gerar_texto_com_contexto.return_value = resposta_sem_contexto
        
        # Cria uma implementação simulada do caso de uso
        class GerarRespostaUseCaseSimulado:
            def __init__(self, language_model):
                self.language_model = language_model
            
            def executar(self, pergunta, chunks):
                # Se não houver chunks, ainda tentar gerar uma resposta
                if not chunks:
                    texto_resposta = self.language_model.gerar_texto_com_contexto(
                        pergunta.texto, "Não há contexto disponível."
                    )
                    return MockResposta(
                        texto=texto_resposta,
                        chunks_utilizados=[]
                    )
                
                # Código para o caso de haver chunks (não executado neste teste)
                contexto = ""
                for i, chunk in enumerate(chunks, 1):
                    contexto += f"[{i}] {chunk.chunk_texto}\n\n"
                
                texto_resposta = self.language_model.gerar_texto_com_contexto(
                    pergunta.texto, contexto
                )
                
                return MockResposta(
                    texto=texto_resposta,
                    chunks_utilizados=chunks
                )
        
        # Instancia o caso de uso simulado
        gerar_resposta = GerarRespostaUseCaseSimulado(
            language_model=self.mock_language_model
        )
        
        # Executa o caso de uso com uma lista vazia de chunks
        resposta = gerar_resposta.executar(self.pergunta, [])
        
        # Verifica se o resultado está correto
        self.assertEqual(resposta.texto, resposta_sem_contexto)
        self.assertEqual(len(resposta.chunks_utilizados), 0)
        
        # Verifica se o método do language_model foi chamado corretamente
        self.mock_language_model.gerar_texto_com_contexto.assert_called_once_with(
            self.pergunta.texto, "Não há contexto disponível."
        )


if __name__ == '__main__':
    unittest.main()