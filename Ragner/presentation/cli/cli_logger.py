#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
CLI Logger: Implementação do logger para a interface de linha de comando.
"""

from domain.Log import Logger
from presentation.cli.cli_cores import Cores

class CLILogger(Logger):
    """
    Implementação de Logger para CLI.
    
    Esta classe implementa a interface Logger do domínio utilizando 
    recursos de apresentação (cores no terminal) na saída.
    """
    
    def registrar_info(self, mensagem=""):
        """
        Registra e exibe uma mensagem informativa no terminal.
        
        Args:
            mensagem: Texto da mensagem a ser registrada
        """
        print(f"{Cores.CINZA}{mensagem}{Cores.RESET}")
    
    def registrar_erro(self, mensagem):
        """
        Registra e exibe uma mensagem de erro no terminal.
        
        Args:
            mensagem: Texto da mensagem de erro a ser registrada
        """
        print(f"{Cores.VERMELHO}[Erro] {mensagem}{Cores.RESET}")
    
    def registrar_debug(self, mensagem):
        """
        Registra e exibe uma mensagem de depuração no terminal.
        
        Args:
            mensagem: Texto da mensagem de depuração a ser registrada
        """
        print(f"{Cores.AZUL}[Debug] {mensagem}{Cores.RESET}")