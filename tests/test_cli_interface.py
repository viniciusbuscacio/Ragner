#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Testes unitários para a interface CLI do Ragner Chatbot.
"""

import unittest
from unittest.mock import MagicMock, patch
import sys
import os

# Adiciona o diretório pai ao path para permitir importação dos módulos do Ragner
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importação da classe CLI e dependências
from Ragner.presentation.cli.cli_interface import CLI
from Ragner.presentation.cli.cli_cores import Cores
from Ragner.presentation.cli.cli_logger import CLILogger


class TestCLIInterface(unittest.TestCase):
    """
    Classe de testes unitários para a interface CLI do Ragner Chatbot.
    """
    
    def setUp(self):
        """
        Configura o ambiente para os testes.
        """
        # Cria mocks para os componentes necessários
        self.mock_controller = MagicMock()
        self.mock_presenter = MagicMock()
        self.mock_logger = MagicMock(spec=CLILogger)
        
        # Inicializa a interface CLI com os mocks
        self.cli = CLI(
            controller=self.mock_controller,
            presenter=self.mock_presenter,
            logger=self.mock_logger
        )
    
    def test_inicializacao(self):
        """
        Testa se a interface CLI é inicializada corretamente.
        """
        # Verifica se os atributos foram configurados corretamente
        self.assertEqual(self.cli.controller, self.mock_controller)
        self.assertEqual(self.cli.presenter, self.mock_presenter)
        self.assertEqual(self.cli.logger, self.mock_logger)
    
    @patch('builtins.input', side_effect=['menu', 'sair'])
    @patch('Ragner.presentation.cli.cli_interface.MensagemSaida')
    def test_iniciar_fluxo_basico(self, mock_mensagem_saida, mock_input):
        """
        Testa o fluxo básico da CLI com comandos menu e sair.
        """
        # Configura o mock para analisar_comando
        self.mock_controller.fazer_pergunta_usecase.analisar_comando.side_effect = [
            (True, 'menu', None),  # Primeiro comando: menu
            (True, 'sair', None)   # Segundo comando: sair
        ]
        
        # Configura o mock do controller para retornar True para menu e False para sair
        self.mock_controller.processar_comando.side_effect = [True, False]
        
        # Iniciar a CLI
        self.cli.iniciar()
        
        # Verifica se as mensagens de boas-vindas foram registradas
        self.mock_logger.registrar_info.assert_any_call(
            f"{Cores.VERDE}\n*** Bem-vindo ao Ragner Chatbot!{Cores.RESET}"
        )
        
        # Verifica se o método processar_comando do controller foi chamado com os argumentos corretos
        self.mock_controller.processar_comando.assert_any_call('menu', None)
        self.mock_controller.processar_comando.assert_any_call('sair', None)
        
        # Verifica se MensagemSaida foi chamada
        mock_mensagem_saida.assert_called_once()
    
    @patch('builtins.input', return_value='Como funciona o RAG?')
    def test_processamento_pergunta(self, mock_input):
        """
        Testa o processamento de uma pergunta.
        """
        # Configura o mock para analisar_comando para retornar uma pergunta e depois um comando de saída
        self.mock_controller.fazer_pergunta_usecase.analisar_comando.side_effect = [
            (False, None, None),    # Não é comando, é uma pergunta
            (True, 'sair', None)    # Comando sair para encerrar o loop
        ]
        
        # Configura o mock do controller para retornar False no comando de saída
        self.mock_controller.processar_comando.return_value = False
        
        # Configura o mock para input para retornar a pergunta e depois o comando de saída
        with patch('builtins.input', side_effect=['Como funciona o RAG?', 'sair']):
            self.cli.iniciar()
        
        # Verifica se o método processar_pergunta foi chamado com a pergunta correta
        self.mock_controller.processar_pergunta.assert_called_once_with('Como funciona o RAG?')
    
    @patch('builtins.input')
    def test_tratamento_interrupcao_teclado(self, mock_input):
        """
        Testa se a CLI trata corretamente uma interrupção de teclado (Ctrl+C).
        """
        # Configura o mock para input para lançar uma exceção KeyboardInterrupt
        mock_input.side_effect = KeyboardInterrupt()
        
        # Iniciar a CLI - não deve lançar exceção
        self.cli.iniciar()
        
        # Verifica se uma mensagem de encerramento foi registrada
        self.mock_logger.registrar_info.assert_any_call("\nEncerrando o Ragner Chatbot.")


if __name__ == '__main__':
    unittest.main()