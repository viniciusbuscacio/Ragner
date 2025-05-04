#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Caso de uso: Configurar a chave de API da OpenAI.
"""

import os
import subprocess
from presentation.cli.cli_cores import Cores
from presentation.cli.cli_logger import CLILogger

# Inicializa o logger para a interface CLI
cli_logger = CLILogger()


class ConfigurarApiKeyUseCase:
    """
    Caso de uso para configurar a chave de API da OpenAI.
    
    Esta classe é responsável por configurar e verificar a chave de API da OpenAI.
    """
    
    def __init__(self, openai_gateway):
        """
        Inicializa o caso de uso.
        
        Args:
            openai_gateway: Gateway para comunicação com a API da OpenAI
        """
        self.openai_gateway = openai_gateway
    
    def executar(self, api_key):
        """
        Configura a chave de API da OpenAI temporariamente para a sessão atual.
        Também configura como variável de ambiente para a sessão atual e
        permanentemente no ambiente do Windows para uso futuro.
        
        Args:
            api_key: Chave de API da OpenAI
            
        Returns:
            bool: True se a configuração foi bem-sucedida, False caso contrário
        """
        # Configura a chave de API para a sessão atual
        self.openai_gateway.configurar_api_key(api_key)
        
        # Verifica se a chave é válida
        chave_valida = self.openai_gateway.verificar_api_key()
        
        # Se a chave for válida, configura a variável de ambiente
        if chave_valida:
            # Define a variável de ambiente para a sessão atual
            os.environ["OPENAI_API_KEY"] = api_key
            
            # Salva permanentemente como variável de ambiente do usuário no Windows
            try:
                # Usa SetX para definir uma variável de ambiente de usuário no Windows
                subprocess.run(
                    ['setx', 'OPENAI_API_KEY', api_key], 
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    check=True,
                    text=True
                )
                cli_logger.registrar_info(f"{Cores.CINZA}Chave de API salva permanentemente nas variáveis de ambiente do usuário.{Cores.RESET}")
            except subprocess.CalledProcessError as e:
                cli_logger.registrar_info(f"Erro ao salvar a chave de API nas variáveis de ambiente: {e}")
            except Exception as e:
                cli_logger.registrar_info(f"Erro inesperado ao salvar a chave de API: {e}")
            
        return chave_valida
    
    def obter_api_key_configurada(self):
        """
        Verifica se a chave de API está configurada.
        Primeiro verifica se já está configurada no objeto gateway,
        depois verifica nas variáveis de ambiente.
        
        Returns:
            bool: True se a chave está configurada, False caso contrário
        """
        # Se já estiver configurada no gateway, retorna True
        if self.openai_gateway.api_key is not None and self.openai_gateway.api_key != "":
            return True
        
        # Se não estiver configurada, tenta obter das variáveis de ambiente
        api_key = os.environ.get("OPENAI_API_KEY")
        if api_key:
            self.openai_gateway.configurar_api_key(api_key)
            return True
            
        return False
    
    def apagar_api_key(self):
        """
        Remove a chave de API da OpenAI das variáveis de ambiente.
        Também limpa a chave do gateway.
        
        Returns:
            bool: True se a operação foi bem-sucedida
        """
        try:
            # Remove a variável de ambiente da sessão atual
            if "OPENAI_API_KEY" in os.environ:
                del os.environ["OPENAI_API_KEY"]
            
            # Remove a variável de ambiente permanente usando o comando setx com string vazia
            subprocess.run(
                ['setx', 'OPENAI_API_KEY', ''], 
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True,
                text=True
            )
            
            # Limpa a chave no gateway
            self.openai_gateway.configurar_api_key("")
            
            cli_logger.registrar_info(f"{Cores.CINZA}Chave de API removida com sucesso das variáveis de ambiente.{Cores.RESET}")
            return True
        except Exception as e:
            cli_logger.registrar_info(f"Erro ao remover a chave de API: {e}")
            return False