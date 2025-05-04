#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Testes unitários para o caso de uso TutorialUseCase.
"""

import unittest
import os
import sys
from unittest.mock import MagicMock, patch

# Adiciona o diretório raiz ao caminho para poder importar os módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Ragner.usecases.tutorial_usecase import TutorialUseCase

class TestTutorialUseCase(unittest.TestCase):
    """
    Classe de testes para o TutorialUseCase.
    """
    
    def setUp(self):
        """
        Configuração inicial para os testes.
        """
        # Mock do presenter para verificar chamadas de método
        self.mock_presenter = MagicMock()
        
        # Mocks dos outros componentes necessários
        self.mock_db_gateway = MagicMock()
        self.mock_doc_indexador = MagicMock()
        self.mock_chat_controller = MagicMock()
        
        # Cria uma instância do caso de uso para testes
        self.tutorial_usecase = TutorialUseCase(
            presenter=self.mock_presenter,
            db_gateway=self.mock_db_gateway,
            doc_indexador=self.mock_doc_indexador,
            chat_controller=self.mock_chat_controller
        )
    
    @patch('keyboard.read_event')
    def test_aguardar_tecla_continue(self, mock_read_event):
        """
        Testa o método _aguardar_tecla quando o usuário quer continuar.
        """
        # Configura o mock para simular pressionar uma tecla qualquer (não ESC)
        mock_event = MagicMock()
        mock_event.name = 'enter'
        mock_read_event.return_value = mock_event
        
        # Também é necessário simular o comportamento de keyboard.is_pressed
        with patch('keyboard.is_pressed', return_value=False):
            result = self.tutorial_usecase._aguardar_tecla("Mensagem de teste")
        
        # Verifica se a função retornou True (continuar)
        self.assertTrue(result)
        # Verifica se o presenter foi chamado com a mensagem correta
        self.mock_presenter.exibir_texto_aguardar.assert_called_with("Mensagem de teste")
    
    @patch('keyboard.read_event')
    def test_aguardar_tecla_esc(self, mock_read_event):
        """
        Testa o método _aguardar_tecla quando o usuário pressiona ESC para sair.
        """
        # Configura o mock para simular pressionar ESC
        mock_event = MagicMock()
        mock_event.name = 'esc'
        mock_read_event.return_value = mock_event
        
        # Também é necessário simular o comportamento de keyboard.is_pressed
        with patch('keyboard.is_pressed', return_value=False):
            result = self.tutorial_usecase._aguardar_tecla()
        
        # Verifica se a função retornou False (sair)
        self.assertFalse(result)
    
    def test_exibir_boas_vindas(self):
        """
        Testa o método _exibir_boas_vindas.
        """
        # Executa o método
        self.tutorial_usecase._exibir_boas_vindas()
        
        # Verifica se os métodos do presenter foram chamados corretamente
        self.mock_presenter.limpar_tela.assert_called_once()
        self.mock_presenter.exibir_titulo_tutorial.assert_called_once()
        self.mock_presenter.exibir_saudacao.assert_called_once()
        # Verifica pelo menos duas chamadas para exibir_texto_tutorial
        self.assertTrue(self.mock_presenter.exibir_texto_tutorial.call_count >= 2)
    
    def test_exibir_chave_api(self):
        """
        Testa o método _exibir_chave_api.
        """
        # Executa o método
        self.tutorial_usecase._exibir_chave_api()
        
        # Verifica se os métodos do presenter foram chamados corretamente
        self.mock_presenter.exibir_titulo_tutorial.assert_called_once()
        # Verifica pelo menos três chamadas para exibir_texto_tutorial
        self.assertTrue(self.mock_presenter.exibir_texto_tutorial.call_count >= 3)
    
    @patch('keyboard.read_event')
    def test_executar_tutorial_completo(self, mock_read_event):
        """
        Testa a execução completa do tutorial.
        """
        # Configura o mock para simular pressionar uma tecla qualquer (não ESC)
        mock_event = MagicMock()
        mock_event.name = 'enter'
        mock_read_event.return_value = mock_event
        
        # Cria mocks para os métodos do tutorial
        self.tutorial_usecase._exibir_boas_vindas = MagicMock()
        self.tutorial_usecase._exibir_chave_api = MagicMock()
        self.tutorial_usecase._exibir_processo_indexacao = MagicMock()
        self.tutorial_usecase._exibir_busca_vetorial = MagicMock()
        self.tutorial_usecase._exibir_perguntas_respostas = MagicMock()
        self.tutorial_usecase._exibir_exploracao = MagicMock()
        
        # Mock para keyboard.is_pressed
        with patch('keyboard.is_pressed', return_value=False):
            # Executa o tutorial
            self.tutorial_usecase.executar_tutorial()
        
        # Verifica se cada método do tutorial foi chamado exatamente uma vez
        self.tutorial_usecase._exibir_boas_vindas.assert_called_once()
        self.tutorial_usecase._exibir_chave_api.assert_called_once()
        self.tutorial_usecase._exibir_processo_indexacao.assert_called_once()
        self.tutorial_usecase._exibir_busca_vetorial.assert_called_once()
        self.tutorial_usecase._exibir_perguntas_respostas.assert_called_once()
        self.tutorial_usecase._exibir_exploracao.assert_called_once()
    
    @patch('keyboard.read_event')
    def test_executar_tutorial_com_saida_antecipada(self, mock_read_event):
        """
        Testa o tutorial quando o usuário sai antes de completar.
        """
        # Configura o mock para simular pressionar ESC
        mock_event = MagicMock()
        mock_event.name = 'esc'
        mock_read_event.return_value = mock_event
        
        # Cria mock para o primeiro método do tutorial
        self.tutorial_usecase._exibir_boas_vindas = MagicMock()
        
        # Mock para keyboard.is_pressed
        with patch('keyboard.is_pressed', return_value=False):
            # Executa o tutorial
            self.tutorial_usecase.executar_tutorial()
        
        # Verifica se apenas o primeiro método foi chamado
        self.tutorial_usecase._exibir_boas_vindas.assert_called_once()
        
    @patch('keyboard.read_event')
    def test_executar_tutorial_com_erro(self, mock_read_event):
        """
        Testa o tutorial quando ocorre um erro durante a execução.
        """
        # Configura o mock para simular pressionar uma tecla qualquer
        mock_event = MagicMock()
        mock_event.name = 'enter'
        mock_read_event.return_value = mock_event
        
        # Mock para keyboard.is_pressed
        with patch('keyboard.is_pressed', return_value=False):
            # Configura o primeiro método para lançar uma exceção
            with patch.object(self.tutorial_usecase, '_exibir_boas_vindas', 
                             side_effect=Exception("Erro de teste")):
                # Executa o tutorial
                self.tutorial_usecase.executar_tutorial()
        
        # Verifica se o erro foi tratado corretamente
        self.mock_presenter.exibir_mensagem_erro.assert_called_once()
        self.mock_presenter.exibir_mensagem_sistema.assert_called_once()


if __name__ == '__main__':
    unittest.main()