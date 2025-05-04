#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Testes unitários para o controlador do chat do Ragner Chatbot.
"""

import unittest
from unittest.mock import MagicMock, patch
import sys
import os

# Adiciona o diretório pai ao path para permitir importação dos módulos do Ragner
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Ragner.presentation.cli.controllers import ChatController


class TestChatController(unittest.TestCase):
    """
    Classe de testes unitários para o controlador do chat.
    """
    
    def setUp(self):
        """
        Configura o ambiente para os testes.
        """
        # Cria mocks para os casos de uso necessários
        self.mock_configurar_api_key_usecase = MagicMock()
        self.mock_indexar_documentos_usecase = MagicMock()
        self.mock_buscar_contexto_usecase = MagicMock()
        self.mock_fazer_pergunta_usecase = MagicMock()
        self.mock_gerar_resposta_usecase = MagicMock()
        self.mock_presenter = MagicMock()
        
        # Inicializa o controlador com os mocks
        self.controller = ChatController(
            configurar_api_key_usecase=self.mock_configurar_api_key_usecase,
            indexar_documentos_usecase=self.mock_indexar_documentos_usecase,
            buscar_contexto_usecase=self.mock_buscar_contexto_usecase,
            fazer_pergunta_usecase=self.mock_fazer_pergunta_usecase,
            gerar_resposta_usecase=self.mock_gerar_resposta_usecase,
            presenter=self.mock_presenter
        )
        
        # Mock para o método _obter_pasta_documentos
        self.controller._obter_pasta_documentos = MagicMock(return_value='/caminho/simulado/documentos')
    
    def test_inicializacao(self):
        """
        Testa se o controlador é inicializado corretamente.
        """
        self.assertEqual(self.controller.configurar_api_key_usecase, self.mock_configurar_api_key_usecase)
        self.assertEqual(self.controller.indexar_documentos_usecase, self.mock_indexar_documentos_usecase)
        self.assertEqual(self.controller.buscar_contexto_usecase, self.mock_buscar_contexto_usecase)
        self.assertEqual(self.controller.fazer_pergunta_usecase, self.mock_fazer_pergunta_usecase)
        self.assertEqual(self.controller.gerar_resposta_usecase, self.mock_gerar_resposta_usecase)
        self.assertEqual(self.controller.presenter, self.mock_presenter)
        self.assertEqual(self.controller.pasta_documentos, '/caminho/simulado/documentos')
    
    def test_processar_comando_menu(self):
        """
        Testa o processamento do comando 'menu'.
        """
        # Executa o método a ser testado
        resultado = self.controller.processar_comando('menu')
        
        # Verifica se o método do presenter foi chamado
        self.mock_presenter.exibir_menu.assert_called_once()
        
        # Verifica se o método retorna True (continuar execução)
        self.assertTrue(resultado)
    
    def test_processar_comando_sair(self):
        """
        Testa o processamento do comando 'sair'.
        """
        # Executa o método a ser testado
        resultado = self.controller.processar_comando('sair')
        
        # Verifica se o método retorna False (encerrar execução)
        self.assertFalse(resultado)
    
    @patch('os.listdir')
    def test_verificar_e_indexar_documentos_sem_arquivos(self, mock_listdir):
        """
        Testa o método verificar_e_indexar_documentos quando não há arquivos.
        """
        # Configura o mock para retornar uma lista vazia
        mock_listdir.return_value = []
        
        # Executa o método a ser testado
        self.controller.verificar_e_indexar_documentos()
        
        # Verifica se as mensagens corretas foram exibidas
        self.mock_presenter.exibir_mensagem_info.assert_any_call(
            f"Não foram encontrados documentos na pasta {self.controller.pasta_documentos}"
        )
        
        # Verifica que o caso de uso de indexação não foi chamado
        self.mock_indexar_documentos_usecase.indexar_pasta.assert_not_called()
    
    @patch('os.listdir')
    def test_verificar_e_indexar_documentos_com_arquivos(self, mock_listdir):
        """
        Testa o método verificar_e_indexar_documentos quando há arquivos.
        """
        # Configura o mock para retornar uma lista com arquivos
        mock_listdir.return_value = ['documento1.pdf', 'documento2.txt']
        
        # Configura o mock para o caso de uso de indexação
        self.mock_indexar_documentos_usecase.indexar_pasta.return_value = (2, 10)  # 2 docs, 10 chunks
        
        # Executa o método a ser testado
        self.controller.verificar_e_indexar_documentos()
        
        # Verifica se o caso de uso de indexação foi chamado com o caminho correto
        self.mock_indexar_documentos_usecase.indexar_pasta.assert_called_once_with(self.controller.pasta_documentos)
        
        # Verifica se a mensagem de sucesso foi exibida
        self.mock_presenter.exibir_mensagem_sucesso.assert_called()
    
    def test_processar_pergunta(self):
        """
        Testa o método processar_pergunta.
        """
        # Mocks para os componentes necessários
        pergunta_texto = "Como funciona o RAG?"
        mock_pergunta = MagicMock()
        mock_embedding = [0.1, 0.2, 0.3]  # Simulação de um embedding
        mock_chunks = [MagicMock(), MagicMock()]  # Lista de chunks simulados
        mock_resposta = MagicMock()
        
        # Configura os mocks para simular o fluxo completo
        self.mock_configurar_api_key_usecase.openai_gateway = MagicMock()
        self.mock_fazer_pergunta_usecase.executar.return_value = (mock_pergunta, mock_embedding)
        self.mock_buscar_contexto_usecase.vector_store.buscar_chunks_similares.return_value = (['1', '2'], [0.8, 0.9])
        self.mock_buscar_contexto_usecase.executar.return_value = mock_chunks
        self.mock_gerar_resposta_usecase.executar.return_value = mock_resposta
        
        # Executa o método a ser testado
        self.controller.processar_pergunta(pergunta_texto)
        
        # Verifica se todos os métodos necessários foram chamados
        self.mock_presenter.exibir_pergunta.assert_called_once_with(pergunta_texto)
        self.mock_fazer_pergunta_usecase.executar.assert_called_once()
        self.mock_buscar_contexto_usecase.executar.assert_called_once_with(mock_embedding)
        self.mock_gerar_resposta_usecase.executar.assert_called_once_with(mock_pergunta, mock_chunks)
        self.mock_presenter.exibir_resposta.assert_called_once_with(mock_resposta)


if __name__ == '__main__':
    unittest.main()