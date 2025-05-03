#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
CLI Interface: Interface de linha de comando para o Ragner Chatbot.
"""
from presentation.cli.cli_cores import Cores


class CLI:
    """
    Interface de linha de comando para o Ragner Chatbot.
    
    Esta classe é responsável pela interação direta com o usuário,
    exibindo mensagens e recebendo comandos.
    """
    
    def __init__(self, controller, presenter):
        """
        Inicializa a interface CLI.
        
        Args:
            controller: Controlador para gerenciar os casos de uso
            presenter: Presenter para exibição de mensagens
        """
        self.controller = controller
        self.presenter = presenter
    
    def iniciar(self):
        """Inicia a interface CLI do Ragner."""
        # Exibe mensagem de boas-vindas
        print(f"{Cores.VERDE}\n*** Bem-vindo ao Ragner Chatbot!{Cores.RESET}")
        print(f"{Cores.RESET}Digite {Cores.AMARELO}'menu'{Cores.RESET} para ver os comandos disponíveis ou {Cores.AMARELO}'sair'{Cores.RESET} para encerrar.")
        print(f"{Cores.RESET}Digite sua pergunta e pressione Enter para começar.")
        
        # Loop principal de interação
        continuar = True
        while continuar:
            # Solicita entrada do usuário
            try:
                entrada = input("\nVocê: ")
            except (KeyboardInterrupt, EOFError):
                print("\nEncerrando o Ragner Chatbot.")
                break
            
            # Verifica se é um comando especial
            e_comando, comando, argumento = self.controller.fazer_pergunta_usecase.analisar_comando(entrada)
            
            if e_comando:
                # Processa o comando
                continuar = self.controller.processar_comando(comando, argumento)
            else:
                # Processa como uma pergunta
                self.controller.processar_pergunta(entrada)
        
        # Encerra o programa
        print("Obrigado por usar o Ragner Chatbot!")