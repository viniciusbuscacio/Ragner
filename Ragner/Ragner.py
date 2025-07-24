#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Ragner: O chatbot que aprende com seus documentos.
Desvendando o Retrieval-Augmented Generation (RAG)
"""

import os
import sys
import logging
import time
import hashlib
import uuid

# Adiciona o diretório do projeto ao PYTHONPATH
project_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_dir)

from infrastructure.database.sqlite_management import SQLiteManagement
from infrastructure.database.sqlite_check import verificar_criar_banco
from infrastructure.vector_store.faiss import FaissVectorStore
from infrastructure.language_model.openai_gateway import OpenAIGateway
from infrastructure.repositories.SQLiteChunkRepository import SQLiteChunkRepository

from usecases.configurar_api_key_usecase import ConfigurarApiKeyUseCase
from usecases.indexar_documentos_usecase import IndexarDocumentosUseCase
from usecases.buscar_contexto_usecase import BuscarContextoUseCase
from usecases.fazer_pergunta_usecase import FazerPerguntaUseCase
from usecases.gerar_resposta_usecase import GerarRespostaUseCase

from presentation.cli.cli_interface import CLI
from presentation.cli.controllers import ChatController
from presentation.cli.presenters import ChatPresenter
from presentation.cli.cli_cores import Cores
from presentation.cli.cli_logger import CLILogger
from presentation.cli.cli_sair  import MensagemSaida


# Inicializa o logger para a interface CLI
cli_logger = CLILogger()

def main():
    """
    Função principal que inicializa o Ragner Chatbot.
    """
    # Exibe o cabeçalho usando o logger
    cli_logger.registrar_info("\n" + "=" * 80)
    cli_logger.registrar_info(" " * 35 + Cores.AMARELO + " Ragner Chatbot " + Cores.RESET)
    cli_logger.registrar_info("=" * 80)
   
    # Inicializa apenas o gateway OpenAI para verificação da chave primeiro
    openai_gateway = OpenAIGateway()
    configurar_api_key_usecase = ConfigurarApiKeyUseCase(openai_gateway)
    
    # PRIMEIRA VERIFICAÇÃO: Chave da OpenAI (essencial para funcionamento)
    cli_logger.registrar_info(f"{Cores.CINZA}Verificando a chave da OpenAI...{Cores.RESET}")
    
    # Verifica se a chave de API já está configurada
    if not configurar_api_key_usecase.obter_api_key_configurada():
        cli_logger.registrar_info(f"{Cores.AMARELO}Chave da OpenAI não encontrada.{Cores.RESET}")
        
        while True:
            # Solicita a chave de API ao usuário
            api_key = input(f"{Cores.AMARELO}Digite sua chave da OpenAI (ou 'sair' para encerrar): {Cores.RESET}")
            
            if api_key.lower() == 'sair':
                cli_logger.registrar_info("Tchau!")
                sys.exit(0)
            
            # Configura a chave de API
            if configurar_api_key_usecase.executar(api_key):
                cli_logger.registrar_info(f"{Cores.CINZA}Chave da OpenAI validada com sucesso.{Cores.RESET}")
                break
            else:
                cli_logger.registrar_info(f"{Cores.VERMELHO}Chave da OpenAI inválida. Tente novamente.{Cores.RESET}")
    else:
        # Verifica se a chave configurada é válida
        if not openai_gateway.verificar_api_key():
            cli_logger.registrar_info(f"{Cores.AMARELO}Chave da OpenAI encontrada mas é inválida.{Cores.RESET}")
            
            while True:
                api_key = input(f"{Cores.AMARELO}Digite sua chave da OpenAI (ou 'sair' para encerrar): {Cores.RESET}")
                
                if api_key.lower() == 'sair':
                    cli_logger.registrar_info("Tchau!")
                    sys.exit(0)
                
                if configurar_api_key_usecase.executar(api_key):
                    cli_logger.registrar_info(f"{Cores.CINZA}Chave da OpenAI validada com sucesso.{Cores.RESET}")
                    break
                else:
                    cli_logger.registrar_info(f"{Cores.VERMELHO}Chave da OpenAI inválida. Tente novamente.{Cores.RESET}")
        else:
            cli_logger.registrar_info(f"{Cores.CINZA}Chave da OpenAI validada com sucesso.{Cores.RESET}")
   
    # Agora inicializa outros gateways
    db_gateway = SQLiteManagement(logger=cli_logger)
    faiss_gateway = FaissVectorStore()
    
    # Inicializa repositórios
    chunk_repository = SQLiteChunkRepository(db_gateway, logger=cli_logger)
    
    # Inicializa presenter
    cli_presenter = ChatPresenter(db_gateway=db_gateway)
    
    # Inicializa casos de uso
    indexar_documentos_usecase = IndexarDocumentosUseCase(
        db_gateway=db_gateway, 
        vector_store=faiss_gateway, 
        language_model=openai_gateway,
        chunk_repository=chunk_repository,
        logger=cli_logger  # Injetando o logger
    )
    buscar_contexto_usecase = BuscarContextoUseCase(faiss_gateway, db_gateway)
    fazer_pergunta_usecase = FazerPerguntaUseCase()
    gerar_resposta_usecase = GerarRespostaUseCase(openai_gateway)
    
    # Inicializa controlador
    chat_controller = ChatController(
        configurar_api_key_usecase=configurar_api_key_usecase,
        indexar_documentos_usecase=indexar_documentos_usecase,
        buscar_contexto_usecase=buscar_contexto_usecase,
        fazer_pergunta_usecase=fazer_pergunta_usecase,
        gerar_resposta_usecase=gerar_resposta_usecase,
        presenter=cli_presenter
    )
    
    # Executa as verificações restantes
    # A chave da OpenAI já foi verificada no início
    
    # Verifica o banco de dados
    verificar_criar_banco(logger=cli_logger)
    
    # Por fim, carrega os arquivos da pasta
    chat_controller.recarregar_arquivos_da_pasta()
    cli_logger.registrar_info("------------------------------------------------------------")
    
    # Inicializa interface CLI
    cli_interface = CLI(chat_controller, cli_presenter, logger=cli_logger)
    
    # Inicia a interface
    cli_interface.iniciar()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        MensagemSaida()
        sys.exit(0)
    except Exception as e:
        # Inicializamos um logger básico para este erro, já que o cli_logger
        # pode não estar disponível neste ponto
        error_logger = CLILogger()
        error_logger.registrar_erro(f"\nOcorreu um erro inesperado: {str(e)}")
        sys.exit(1)