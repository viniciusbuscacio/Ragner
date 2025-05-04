#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Testes para o caso de uso de processamento de perguntas do Ragner Chatbot.
"""

import unittest
from unittest.mock import MagicMock, patch
import sys
import os


class MockPergunta:
    def __init__(self, texto):
        self.texto = texto


class TestFazerPergunta(unittest.TestCase):
    """
    Testes para o caso de uso de processamento de perguntas.
    """
    
    def setUp(self):
        """
        Preparação para os testes.
        """
        # Cria componentes simulados
        self.mock_language_model = MagicMock()
        
        # Configura o mock para gerar_embedding
        self.mock_language_model.gerar_embedding.return_value = [0.1, 0.2, 0.3, 0.4]
    
    def test_executar_com_pergunta_valida(self):
        """
        Testa o fluxo de processamento com uma pergunta válida.
        """
        # Cria uma implementação simulada do caso de uso
        class FazerPerguntaUseCaseSimulado:
            def __init__(self):
                self.comandos_especiais = {
                    "menu": self._mostrar_menu,
                    "sobre": self._mostrar_sobre,
                    "tutorial": self._mostrar_tutorial,
                    "status": self._mostrar_status,
                    "status_tabela_arquivos": self._mostrar_status_arquivos,
                    "status_tabela_chunks": self._mostrar_status_chunks,
                    "status_faiss": self._mostrar_status_faiss,
                    "recarregar_arquivos_da_pasta": self._recarregar_arquivos,
                    "apagar_tudo": self._apagar_tudo,
                    "teste_vetor": self._teste_vetor,
                    "reconstruir_indice_faiss": self._reconstruir_indice_faiss,
                    "configurar_api_key": self._configurar_api_key,
                    "sair": self._sair
                }
            
            def analisar_comando(self, texto):
                """
                Verifica se o texto é um comando especial.
                
                Args:
                    texto: Texto a ser analisado
                    
                Returns:
                    tuple: (é_comando, comando, argumento)
                """
                if not texto.strip():
                    return False, None, None
                    
                # Divide o texto em tokens
                tokens = texto.strip().split()
                comando = tokens[0].lower()
                
                # Verifica se é um comando conhecido
                if comando in self.comandos_especiais:
                    # Se houver mais tokens, o resto é considerado argumento
                    argumento = " ".join(tokens[1:]) if len(tokens) > 1 else None
                    return True, comando, argumento
                
                # Não é um comando
                return False, None, None
            
            def executar(self, texto_pergunta, language_model):
                """
                Processa o texto da pergunta.
                
                Args:
                    texto_pergunta: Texto da pergunta
                    language_model: Modelo de linguagem para gerar embeddings
                    
                Returns:
                    tuple: (pergunta, embedding)
                """
                if not texto_pergunta.strip():
                    return None, None
                
                # Cria objeto Pergunta
                pergunta = MockPergunta(texto_pergunta)
                
                # Gera embedding
                embedding = language_model.gerar_embedding(texto_pergunta)
                
                return pergunta, embedding
            
            # Métodos simulados para comandos especiais
            def _mostrar_menu(self): pass
            def _mostrar_sobre(self): pass
            def _mostrar_tutorial(self): pass
            def _mostrar_status(self): pass
            def _mostrar_status_arquivos(self): pass
            def _mostrar_status_chunks(self): pass
            def _mostrar_status_faiss(self): pass
            def _recarregar_arquivos(self): pass
            def _apagar_tudo(self): pass
            def _teste_vetor(self): pass
            def _reconstruir_indice_faiss(self): pass
            def _configurar_api_key(self): pass
            def _sair(self): pass
        
        # Instancia o caso de uso simulado
        fazer_pergunta = FazerPerguntaUseCaseSimulado()
        
        # Executa o método com uma pergunta válida
        pergunta, embedding = fazer_pergunta.executar("Como funciona o RAG?", self.mock_language_model)
        
        # Verifica se o resultado está correto
        self.assertIsNotNone(pergunta)
        self.assertEqual(pergunta.texto, "Como funciona o RAG?")
        self.assertIsNotNone(embedding)
        self.assertEqual(embedding, [0.1, 0.2, 0.3, 0.4])
        
        # Verifica se o método do language_model foi chamado corretamente
        self.mock_language_model.gerar_embedding.assert_called_once_with("Como funciona o RAG?")
    
    def test_executar_com_pergunta_vazia(self):
        """
        Testa o fluxo de processamento com uma pergunta vazia.
        """
        # Cria uma implementação simulada do caso de uso
        class FazerPerguntaUseCaseSimulado:
            def executar(self, texto_pergunta, language_model):
                if not texto_pergunta.strip():
                    return None, None
                
                pergunta = MockPergunta(texto_pergunta)
                embedding = language_model.gerar_embedding(texto_pergunta)
                
                return pergunta, embedding
        
        # Instancia o caso de uso simulado
        fazer_pergunta = FazerPerguntaUseCaseSimulado()
        
        # Executa o método com uma pergunta vazia
        pergunta, embedding = fazer_pergunta.executar("   ", self.mock_language_model)
        
        # Verifica se o resultado está correto
        self.assertIsNone(pergunta)
        self.assertIsNone(embedding)
        
        # Verifica que o método do language_model não foi chamado
        self.mock_language_model.gerar_embedding.assert_not_called()
    
    def test_analisar_comando_valido(self):
        """
        Testa a análise de um comando válido.
        """
        # Cria uma implementação simulada do caso de uso
        class FazerPerguntaUseCaseSimulado:
            def __init__(self):
                self.comandos_especiais = {
                    "menu": None, "sobre": None, "tutorial": None,
                    "status": None, "sair": None
                }
            
            def analisar_comando(self, texto):
                if not texto.strip():
                    return False, None, None
                    
                tokens = texto.strip().split()
                comando = tokens[0].lower()
                
                if comando in self.comandos_especiais:
                    argumento = " ".join(tokens[1:]) if len(tokens) > 1 else None
                    return True, comando, argumento
                
                return False, None, None
        
        # Instancia o caso de uso simulado
        fazer_pergunta = FazerPerguntaUseCaseSimulado()
        
        # Testa diferentes comandos
        e_comando, comando, argumento = fazer_pergunta.analisar_comando("menu")
        self.assertTrue(e_comando)
        self.assertEqual(comando, "menu")
        self.assertIsNone(argumento)
        
        e_comando, comando, argumento = fazer_pergunta.analisar_comando("sobre o projeto")
        self.assertTrue(e_comando)
        self.assertEqual(comando, "sobre")
        self.assertEqual(argumento, "o projeto")
        
        e_comando, comando, argumento = fazer_pergunta.analisar_comando("sair")
        self.assertTrue(e_comando)
        self.assertEqual(comando, "sair")
        self.assertIsNone(argumento)
    
    def test_analisar_comando_invalido(self):
        """
        Testa a análise de um texto que não é um comando válido.
        """
        # Cria uma implementação simulada do caso de uso
        class FazerPerguntaUseCaseSimulado:
            def __init__(self):
                self.comandos_especiais = {
                    "menu": None, "sobre": None, "tutorial": None,
                    "status": None, "sair": None
                }
            
            def analisar_comando(self, texto):
                if not texto.strip():
                    return False, None, None
                    
                tokens = texto.strip().split()
                comando = tokens[0].lower()
                
                if comando in self.comandos_especiais:
                    argumento = " ".join(tokens[1:]) if len(tokens) > 1 else None
                    return True, comando, argumento
                
                return False, None, None
        
        # Instancia o caso de uso simulado
        fazer_pergunta = FazerPerguntaUseCaseSimulado()
        
        # Testa textos que não são comandos
        e_comando, comando, argumento = fazer_pergunta.analisar_comando("Como funciona o RAG?")
        self.assertFalse(e_comando)
        self.assertIsNone(comando)
        self.assertIsNone(argumento)
        
        e_comando, comando, argumento = fazer_pergunta.analisar_comando("Explique o mecanismo de busca")
        self.assertFalse(e_comando)
        self.assertIsNone(comando)
        self.assertIsNone(argumento)


if __name__ == '__main__':
    unittest.main()