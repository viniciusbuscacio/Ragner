#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
OpenAI Gateway: Fornece acesso à API da OpenAI para geração de embeddings e respostas.
"""

import os
import json
from openai import OpenAI


class OpenAIGateway:
    """
    Fornece acesso à API da OpenAI para geração de embeddings e respostas.
    
    Esta classe é responsável por gerenciar a comunicação com a API da OpenAI,
    incluindo a configuração da chave de API e a geração de embeddings e respostas.
    """
    
    def __init__(self, api_key=None):
        """
        Inicializa o gateway da OpenAI.
        
        Args:
            api_key: Chave de API da OpenAI (opcional, prioridade para variável de ambiente)
        """
        # Priorizar a variável de ambiente sobre o parâmetro api_key
        self.api_key = os.environ.get("OPENAI_API_KEY") or api_key
        self.client = None
        self.embedding_model = "text-embedding-3-small"
        self.chat_model = "gpt-3.5-turbo"
    
    def configurar_api_key(self, api_key):
        """
        Configura a chave de API da OpenAI.
        
        Args:
            api_key: Chave de API da OpenAI
            
        Returns:
            bool: True se a configuração foi bem-sucedida
        """
        self.api_key = api_key
        self.client = None  # Reseta o cliente para forçar a criação de um novo
        return True
    
    def obter_client(self):
        """
        Obtém o cliente da API da OpenAI.
        
        Returns:
            OpenAI: Cliente da API da OpenAI
        
        Raises:
            ValueError: Se a chave de API não estiver configurada
        """
        if not self.api_key:
            raise ValueError("A chave de API da OpenAI não está configurada.")
        
        if self.client is None:
            self.client = OpenAI(api_key=self.api_key)
        
        return self.client
    
    def gerar_embedding(self, texto):
        """
        Gera um embedding para o texto fornecido.
        
        Args:
            texto: Texto para o qual gerar o embedding
            
        Returns:
            list: Vetor de embedding
            
        Raises:
            Exception: Se ocorrer um erro na chamada da API
        """
        client = self.obter_client()
        
        try:
            response = client.embeddings.create(
                model=self.embedding_model,
                input=texto
            )
            
            embedding_vector = response.data[0].embedding
            return embedding_vector
        
        except Exception as e:
            # Registra o erro completo para fins de depuração, mas não o expõe
            error_message = str(e)
            print(f"Erro interno ao gerar embedding: {error_message}")
            
            # Lança uma exceção mais amigável sem detalhes sensíveis
            raise Exception("Não foi possível gerar embedding. Verifique sua chave de API ou conexão com a internet.")
    
    def gerar_resposta(self, pergunta, contexto=None, system_prompt=None):
        """
        Gera uma resposta para a pergunta fornecida, opcionalmente com contexto.
        
        Args:
            pergunta: Pergunta para a qual gerar uma resposta
            contexto: Contexto para melhorar a resposta (opcional)
            system_prompt: Prompt de sistema (opcional)
            
        Returns:
            str: Resposta gerada pelo modelo
            
        Raises:
            Exception: Se ocorrer um erro na chamada da API
        """
        client = self.obter_client()
        
        messages = []
        
        # Adiciona o prompt de sistema, se fornecido
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        else:
            messages.append({
                "role": "system",
                "content": "Você é um assistente útil e preciso que responde perguntas com base nas informações fornecidas."
            })
        
        # Adiciona o contexto, se fornecido
        if contexto:
            messages.append({
                "role": "system",
                "content": f"Use as seguintes informações para responder à pergunta do usuário:\n\n{contexto}"
            })
        
        # Adiciona a pergunta do usuário
        messages.append({"role": "user", "content": pergunta})
        
        try:
            response = client.chat.completions.create(
                model=self.chat_model,
                messages=messages,
                temperature=0.7,
                max_tokens=1000
            )
            
            resposta = response.choices[0].message.content
            return resposta
        
        except Exception as e:
            # Registra o erro completo para fins de depuração, mas não o expõe
            error_message = str(e)
            print(f"Erro interno ao gerar resposta: {error_message}")
            
            # Lança uma exceção mais amigável sem detalhes sensíveis
            raise Exception("Não foi possível gerar resposta. Verifique sua chave de API ou conexão com a internet.")
    
    def verificar_api_key(self):
        """
        Verifica se a chave de API da OpenAI está válida.
        
        Returns:
            bool: True se a chave é válida, False caso contrário
        """
        # Verifica se a chave existe e não é uma string vazia
        if not self.api_key or self.api_key.strip() == "":
            return False
        
        try:
            # Tenta fazer uma chamada simples para verificar se a chave é válida
            client = self.obter_client()
            response = client.embeddings.create(
                model=self.embedding_model,
                input="Teste de verificação de API"
            )
            
            return True
        
        except Exception as e:
            # Registra o erro completo para fins de depuração, mas não o exibe para o usuário
            # error_message = str(e)
            
            # Log mais detalhado em um arquivo de log se necessário (opcional)
            # with open("api_errors.log", "a") as log_file:
            #     log_file.write(f"[{datetime.now()}] API Key Error: {error_message}\n")
            
            return False