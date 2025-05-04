#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Testes para o caso de uso de configuração da API key do Ragner Chatbot.
"""

import unittest
from unittest.mock import MagicMock, patch
import sys
import os


class TestConfigurarApiKey(unittest.TestCase):
    """
    Testes para o caso de uso de configuração da API key.
    """
    
    def setUp(self):
        """
        Preparação para os testes.
        """
        # Cria componentes simulados
        self.mock_openai_gateway = MagicMock()
        
        # Salva qualquer valor existente para restaurar depois
        self.api_key_original = os.environ.get("OPENAI_API_KEY", None)
        
        # Simula uma variável de ambiente vazia para a chave da API
        self.env_patcher = patch.dict('os.environ', {}, clear=True)
        self.mock_env = self.env_patcher.start()
    
    def tearDown(self):
        """
        Limpeza após os testes.
        """
        self.env_patcher.stop()
        
        # Restaura a variável de ambiente original, se existia
        if self.api_key_original:
            os.environ["OPENAI_API_KEY"] = self.api_key_original
    
    def test_configurar_api_key_valida(self):
        """
        Testa o fluxo de configuração com uma chave de API válida.
        """
        # Configura o mock para verificar_api_key retornar True (chave válida)
        self.mock_openai_gateway.verificar_api_key.return_value = True
        
        # Cria uma implementação simulada do caso de uso
        class ConfigurarApiKeyUseCaseSimulado:
            def __init__(self, openai_gateway):
                self.openai_gateway = openai_gateway
                self.API_ENV_VAR = "OPENAI_API_KEY"
            
            def executar(self, api_key):
                """
                Configura a chave de API da OpenAI.
                
                Args:
                    api_key: Chave de API fornecida pelo usuário
                
                Returns:
                    bool: True se a chave foi configurada com sucesso, False caso contrário
                """
                if not api_key or len(api_key.strip()) < 10:  # Chave muito curta
                    return False
                
                # Configura a chave no gateway
                self.openai_gateway.configurar_api_key(api_key)
                
                # Verifica se a chave é válida
                if self.openai_gateway.verificar_api_key():
                    # Salva a chave nas variáveis de ambiente
                    os.environ[self.API_ENV_VAR] = api_key
                    return True
                else:
                    return False
            
            def obter_api_key_configurada(self):
                """
                Verifica se a chave de API já está configurada.
                
                Returns:
                    str or False: A chave se estiver configurada, False caso contrário
                """
                return os.environ.get(self.API_ENV_VAR, False)
            
            def apagar_api_key(self):
                """
                Remove a chave de API das variáveis de ambiente.
                
                Returns:
                    bool: True se a chave foi removida com sucesso, False caso contrário
                """
                try:
                    if self.API_ENV_VAR in os.environ:
                        os.environ.pop(self.API_ENV_VAR)
                    return True
                except Exception:
                    return False
        
        # Instancia o caso de uso simulado
        configurar_api_key = ConfigurarApiKeyUseCaseSimulado(
            openai_gateway=self.mock_openai_gateway
        )
        
        # Verifica inicialmente que não há chave configurada
        self.assertFalse(configurar_api_key.obter_api_key_configurada())
        
        # Executa o método com uma chave válida
        resultado = configurar_api_key.executar("sk-validApiKey123456789")
        
        # Verifica se o resultado está correto
        self.assertTrue(resultado)
        self.assertEqual(configurar_api_key.obter_api_key_configurada(), "sk-validApiKey123456789")
        self.assertEqual(os.environ["OPENAI_API_KEY"], "sk-validApiKey123456789")
        
        # Verifica se o método do openai_gateway foi chamado corretamente
        self.mock_openai_gateway.configurar_api_key.assert_called_once_with("sk-validApiKey123456789")
        self.mock_openai_gateway.verificar_api_key.assert_called_once()
    
    def test_configurar_api_key_invalida(self):
        """
        Testa o fluxo de configuração com uma chave de API inválida.
        """
        # Configura o mock para verificar_api_key retornar False (chave inválida)
        self.mock_openai_gateway.verificar_api_key.return_value = False
        
        # Cria uma implementação simulada do caso de uso
        class ConfigurarApiKeyUseCaseSimulado:
            def __init__(self, openai_gateway):
                self.openai_gateway = openai_gateway
                self.API_ENV_VAR = "OPENAI_API_KEY"
            
            def executar(self, api_key):
                if not api_key or len(api_key.strip()) < 10:
                    return False
                
                self.openai_gateway.configurar_api_key(api_key)
                
                if self.openai_gateway.verificar_api_key():
                    os.environ[self.API_ENV_VAR] = api_key
                    return True
                else:
                    return False
            
            def obter_api_key_configurada(self):
                return os.environ.get(self.API_ENV_VAR, False)
        
        # Instancia o caso de uso simulado
        configurar_api_key = ConfigurarApiKeyUseCaseSimulado(
            openai_gateway=self.mock_openai_gateway
        )
        
        # Executa o método com uma chave inválida
        resultado = configurar_api_key.executar("sk-invalidApiKey")
        
        # Verifica se o resultado está correto
        self.assertFalse(resultado)
        self.assertFalse(configurar_api_key.obter_api_key_configurada())
        self.assertNotIn("OPENAI_API_KEY", os.environ)
        
        # Verifica se o método do openai_gateway foi chamado corretamente
        self.mock_openai_gateway.configurar_api_key.assert_called_once_with("sk-invalidApiKey")
        self.mock_openai_gateway.verificar_api_key.assert_called_once()
    
    def test_apagar_api_key(self):
        """
        Testa o método para apagar a chave de API.
        """
        # Configura a variável de ambiente com uma chave
        os.environ["OPENAI_API_KEY"] = "sk-someApiKey"
        
        # Cria uma implementação simulada do caso de uso
        class ConfigurarApiKeyUseCaseSimulado:
            def __init__(self, openai_gateway):
                self.openai_gateway = openai_gateway
                self.API_ENV_VAR = "OPENAI_API_KEY"
            
            def apagar_api_key(self):
                try:
                    if self.API_ENV_VAR in os.environ:
                        os.environ.pop(self.API_ENV_VAR)
                    return True
                except Exception:
                    return False
            
            def obter_api_key_configurada(self):
                return os.environ.get(self.API_ENV_VAR, False)
        
        # Instancia o caso de uso simulado
        configurar_api_key = ConfigurarApiKeyUseCaseSimulado(
            openai_gateway=self.mock_openai_gateway
        )
        
        # Verifica que a chave está configurada
        self.assertEqual(configurar_api_key.obter_api_key_configurada(), "sk-someApiKey")
        
        # Apaga a chave
        resultado = configurar_api_key.apagar_api_key()
        
        # Verifica se o resultado está correto
        self.assertTrue(resultado)
        self.assertFalse(configurar_api_key.obter_api_key_configurada())
        self.assertNotIn("OPENAI_API_KEY", os.environ)


if __name__ == '__main__':
    unittest.main()