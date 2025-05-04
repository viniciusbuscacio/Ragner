#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Mensagem de saída para o usuário
# Aqui, vamos criar mensagens de saída aleatórias para o usuário

import random
from Ragner.presentation.cli.cli_cores import Cores
from Ragner.presentation.cli.cli_logger import CLILogger

# Inicializa o logger para a interface CLI
cli_logger = CLILogger()

class MensagemSaida:
    """
    Classe para gerar e exibir mensagens de saída para o usuário.
    Quando instanciada, seleciona e exibe automaticamente uma mensagem de despedida aleatória.
    """

    def __init__(self):
        """
        Inicializa a classe e exibe automaticamente uma mensagem de despedida.
        """
        self.mensagens = [
            "Tchau!",
            "Até logo!",
            "Valeu!",
            "Até a próxima!",
            "Bye!",
            "Fui!",
            "Partiu!",
            "Au revoir!",
            "Adiós!",
            "Sayonara!",
            "Ciao!",
            "Arrivederci!",
            "Adieu!",
            "Até breve!",
            "Até logo mais!",
            "Até mais!",
            "Nos vemos!",
            "Catch you later!",
            "Take care!",
            "Goodbye!",
            "Farewell!",
            "See you soon!",
            "See you later!",
            "See you next time!",
            "See you around!",
            "See ya!",
            "Até mais ver!",
            "Desconectando...",
            "Modo offline ativado!",
            "Ragner se retira para os seus aposentos digitais.",
            "Que a força esteja com você (e seus dados!).",
            "Deslogando em 3... 2... 1...",
            "A gente se vê por aí (ou por aqui de novo!).",
            "Ragner out!",
            "Missão cumprida (pelo menos por agora!).",
            "Se cuida!",
            "E que os bons bits te acompanhem!",
            "Até a próxima aventura!",
        ]
        
        # Exibe automaticamente uma mensagem de despedida
        self._exibir_mensagem()
    
    def get_mensagem(self):
        """
        Retorna uma mensagem de despedida aleatória.
        
        Returns:
            str: Mensagem de despedida selecionada aleatoriamente
        """
        return random.choice(self.mensagens)
    
    def _exibir_mensagem(self):
        """
        Exibe uma mensagem de despedida com formatação colorida.
        """
        mensagem = self.get_mensagem()
        cli_logger.registrar_info(f"\n{Cores.AMARELO}{mensagem}{Cores.RESET}")

