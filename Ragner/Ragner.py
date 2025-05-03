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


def main():
    """
    Função principal que inicializa o Ragner Chatbot.
    """
    print("\n" + "=" * 80)
    print(" " * 35 + Cores.AMARELO + " Ragner Chatbot " + Cores.RESET) 
    print("=" * 80)
   
    # Inicializa gateways
    db_gateway = SQLiteManagement()
    faiss_gateway = FaissVectorStore()
    openai_gateway = OpenAIGateway()
    
    # Inicializa repositórios
    chunk_repository = SQLiteChunkRepository(db_gateway)
    
    # Inicializa casos de uso
    configurar_api_key_usecase = ConfigurarApiKeyUseCase(openai_gateway)
    indexar_documentos_usecase = IndexarDocumentosUseCase(
        db_gateway=db_gateway, 
        vector_store=faiss_gateway, 
        language_model=openai_gateway,
        chunk_repository=chunk_repository
    )
    buscar_contexto_usecase = BuscarContextoUseCase(faiss_gateway, db_gateway)
    fazer_pergunta_usecase = FazerPerguntaUseCase()
    gerar_resposta_usecase = GerarRespostaUseCase(openai_gateway)
    
    # Inicializa presenter
    cli_presenter = ChatPresenter(db_gateway=db_gateway)
    
    # Inicializa controlador
    chat_controller = ChatController(
        configurar_api_key_usecase=configurar_api_key_usecase,
        indexar_documentos_usecase=indexar_documentos_usecase,
        buscar_contexto_usecase=buscar_contexto_usecase,
        fazer_pergunta_usecase=fazer_pergunta_usecase,
        gerar_resposta_usecase=gerar_resposta_usecase,
        presenter=cli_presenter
    )
    
    # Executa as verificações iniciais
    # Primeiro verifica a chave da OpenAI
    chat_controller.verificar_e_configurar_api_key()
    
    # Depois verifica o banco de dados
    verificar_criar_banco()
    
    # Por fim, carrega os arquivos da pasta
    chat_controller.recarregar_arquivos_da_pasta()
    print("------------------------------------------------------------")
    
    # Inicializa interface CLI
    cli_interface = CLI(chat_controller, cli_presenter)
    
    # Inicia a interface
    cli_interface.iniciar()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nEncerrando o Ragner Chatbot. Até logo!")
        sys.exit(0)
    except Exception as e:
        print(f"\nOcorreu um erro inesperado: {str(e)}")
        sys.exit(1)